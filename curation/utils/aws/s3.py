import re
from datetime import timezone

import boto3


class S3:
    def __init__(self):
        self.client = boto3.client("s3")

    def get_all_obj_keys(
        self,
        bucket,
        prefix,
        min_last_modified_date=None,
        regex_filter=None,
    ):
        """
        Retrieve all object keys from a specified S3 bucket and prefix with optional filtering.

        This function uses paginators to handle AWS S3's 1000 objects limit per response.

        Parameters:
        - bucket (str): The name of the S3 bucket.
        - prefix (str): The prefix (path) to filter objects in the S3 bucket.
        - regex_filter (str, optional): A regex pattern to further filter object keys. Defaults to None.
        - min_last_modified_date (datetime, optional): Filters objects based on their "LastModified" date.
            Only objects modified on and after this date will be returned.
            The specified date must be offset-aware. Defaults to None.

        Returns:
        - list: A list of object keys from the specified S3 bucket that match the provided filters.

        Notes:
        - Ensure that the AWS client has the necessary permissions to list objects in the specified bucket.
        """
        paginator = self.client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

        objects = [obj for page in pages for obj in page["Contents"]]

        if min_last_modified_date:
            objects = list(
                filter(
                    lambda obj: obj["LastModified"].astimezone(timezone.utc)
                    >= min_last_modified_date,
                    objects,
                )
            )

        if regex_filter:
            regex = re.compile(regex_filter)
            objects = list(filter(lambda obj: regex.search(obj["Key"]), objects))

        return [obj["Key"] for obj in objects]

    def move_object(self, old_bucket, new_bucket, old_key, new_key):
        copy_source = {"Bucket": old_bucket, "Key": old_key}
        self.client.copy(copy_source, new_bucket, new_key)

        # Delete the old object
        self.client.delete_object(Bucket=old_bucket, Key=old_key)


s3 = S3()
