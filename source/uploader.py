import boto3
from botocore.config import Config as BotoConfig
from source import secrets


class Uploader:
    def __init__(self):
        self.bucket = secrets.R2_BUCKET_NAME
        self.client = boto3.client(
            "s3",
            endpoint_url=f"https://{secrets.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
            aws_access_key_id=secrets.R2_ACCESS_KEY_ID,
            aws_secret_access_key=secrets.R2_SECRET_ACCESS_KEY,
            config=BotoConfig(signature_version="s3v4", connect_timeout=5, read_timeout=15),
            region_name="auto",
        )

    def upload_and_get_link(self, local_path, key, expires_in):
        self.client.upload_file(local_path, self.bucket, key)

        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=expires_in,
        )
