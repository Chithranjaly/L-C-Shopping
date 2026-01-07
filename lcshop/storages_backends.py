from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = "static"
    default_acl = None
    file_overwrite = True

class MediaStorage(S3Boto3Storage):
    bucket_name = "lcshop-media-prod"   # or rely on settings
    location = "media"
    default_acl = None
    file_overwrite = False
    querystring_auth = True   # ✅ this makes .url() produce signed URLs

