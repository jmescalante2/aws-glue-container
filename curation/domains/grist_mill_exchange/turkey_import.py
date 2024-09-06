from curation.domains.grist_mill_exchange.helper import curate
from curation.domains.grist_mill_exchange.mapping.columns import COLUMNS

DATA_SET = "turkey_import"
OBJECT_KEY_FILTER = r".*\.parquet"
FILE_NAME_FORMAT = f"{DATA_SET}_{{file_year_month}}.csv"
OUTPUT_CONFIGURATION = {
    "encoding": "UTF-8",
    "header": True,
    "sep": ",",
    "lineSep": "\n",
    "multiLine": True,
    "quote": '"',
    "escape": '"',
}

WRITE_MODE = "overwrite"
PARTITION_COLUMNS = ["file_year_month"]
PARTITION_LEVEL = 1


def start(
    spark,
    s3_src_bucket,
    s3_src_prefix,
    start_modify_date_time,
    s3_dest_bucket,
    s3_dest_prefix,
):
    curate_config = {
        "spark": spark,
        "s3_src_bucket": s3_src_bucket,
        "s3_src_prefix": s3_src_prefix,
        "start_modify_date_time": start_modify_date_time,
        "s3_dest_bucket": s3_dest_bucket,
        "s3_dest_prefix": s3_dest_prefix,
        "object_key_filter": OBJECT_KEY_FILTER,
        "partition_level": PARTITION_LEVEL,
        "columns": COLUMNS[DATA_SET],
        "write_mode": WRITE_MODE,
        "partition_columns": PARTITION_COLUMNS,
        "file_name_format": FILE_NAME_FORMAT,
        "output_options": OUTPUT_CONFIGURATION,
    }

    curate(**curate_config)
