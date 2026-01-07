import os
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME_STATIC", "lcshop-static-prod")
    location = "static"
    default_acl = "public-read"
