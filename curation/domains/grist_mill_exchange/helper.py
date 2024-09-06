from pyspark.sql.functions import col

from curation.utils.aws.s3 import s3


def get_modified_objects(s3_bucket, s3_prefix, start_modify_date_time, regex_filter):
    return s3.get_all_obj_keys(
        s3_bucket, s3_prefix, start_modify_date_time, regex_filter
    )


def get_modified_partitions(s3_bucket, s3_prefix, object_keys, partition_level=1):
    parts = len(s3_prefix.split("/"))
    partition_depth = parts + partition_level - 1
    partition_prefixes = set(
        "/".join(key.split("/", partition_depth)[:partition_depth])
        for key in object_keys
    )
    partition_paths = [f"s3://{s3_bucket}/{prefix}/" for prefix in partition_prefixes]
    return partition_paths


def read_partitions(s3_bucket, s3_prefix, spark, partitions):
    df = spark.read.option(
        "basePath",
        f"s3://{s3_bucket}/{s3_prefix}",
    ).parquet(*partitions)
    return df


def save_partitions(
    df,
    s3_dest_bucket,
    s3_dest_prefix,
    write_mode,
    partition_columns,
    file_name_format,
    options,
    columns,
):
    parent_partition_column = partition_columns[0]
    partitions = (
        df.select(parent_partition_column).distinct().rdd.flatMap(lambda x: x).collect()
    )
    for partition in partitions:
        df_filtered = df.where(col(parent_partition_column) == partition)
        df_repartitioned = df_filtered.repartition(1)
        temp_prefix = f"{s3_dest_prefix}temp/{parent_partition_column}={partition}/"
        temp_path = f"s3://{s3_dest_bucket}/{temp_prefix}"

        df_repartitioned = resolve_dataframe_columns(df_repartitioned, columns)

        df_repartitioned.write.options(**options).mode(write_mode).csv(temp_path)

        for object_key in s3.get_all_obj_keys(
            s3_dest_bucket, temp_prefix, regex_filter=r".*\.csv"
        ):
            target_file_name = file_name_format.format(
                **{parent_partition_column: partition}
            )
            new_key = f"{s3_dest_prefix}{target_file_name}"
            s3.move_object(s3_dest_bucket, s3_dest_bucket, object_key, new_key)


def resolve_dataframe_columns(df, columns):
    df = df.select(*[column["source_name"] for column in columns])

    for column in columns:
        df = df.withColumnRenamed(column["source_name"], column["display_name"])

    return df


def curate(
    spark,
    s3_src_bucket,
    s3_src_prefix,
    start_modify_date_time,
    s3_dest_bucket,
    s3_dest_prefix,
    object_key_filter,
    partition_level,
    columns,
    write_mode,
    partition_columns,
    file_name_format,
    output_options,
    verbose=True,
):
    objects = get_modified_objects(
        s3_src_bucket, s3_src_prefix, start_modify_date_time, object_key_filter
    )

    partitions = []

    if objects:
        partitions = get_modified_partitions(
            s3_src_bucket, s3_src_prefix, objects, partition_level
        )
        df = read_partitions(s3_src_bucket, s3_src_prefix, spark, partitions)

        if verbose:
            print("Data Frame Schema:")
            df.printSchema()
            print(f"Number of Updated Records: {df.count()}")
            print("Data Frame Preview Before Partitioning and Column Renaming")
            df.show(vertical=True, n=5)

        save_partitions(
            df,
            s3_dest_bucket,
            s3_dest_prefix,
            write_mode,
            partition_columns,
            file_name_format,
            output_options,
            columns,
        )

    if verbose:
        print(f"Number of Updated Partitions: {len(partitions)}")
        print(f"Updated Partitions:", *partitions, sep="\n")
