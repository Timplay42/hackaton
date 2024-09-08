
from contextlib import asynccontextmanager
from utils.base.config import settings
from aiobotocore.session import get_session


class S3Client():
    def __init__(self):
        s3 = settings.s3
        self.config = {
            "aws_access_key_id": s3.access_key,
            "aws_secret_access_key": s3.secret_key,
            "endpoint_url": s3.endpoint_url,
        }
        self.bucket_name = s3.bucket_name
        self.session = get_session()


    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload(self, file, object_name):
        try:
            async with self.get_client() as client:
                await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=file,
                    )
        except Exception as e:
            raise e
        
    async def get_file(self, object_name):
        try:
            async with self.get_client() as client:
                await client.get_object(Bucket=self.bucket_name, Key=object_name)
        except Exception as e:
            raise e
        
S3 = S3Client()