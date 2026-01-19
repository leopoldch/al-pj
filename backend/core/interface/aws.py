from core.exceptions.exceptions import CloudUploadError
from core.interface.photo_saver_repository import PhotoSaverRepository
import boto3
from botocore.exceptions import NoCredentialsError, ClientError, BotoCoreError
import os
import mimetypes
from uuid import uuid4
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_ACCESS_SECRET")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

DEBUG = os.getenv("DEBUG", "False") == "True"


class AwsPhotoSaver(PhotoSaverRepository):

    def _generate_unique_name(self, file_name: str):
        return f"{uuid4()}_{file_name}"

    def _get_s3_client(self):
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION,
        )
        return s3

    def _get_content_type(self, file_name: str):
        content_type, _ = mimetypes.guess_type(file_name)
        content_type = content_type or "application/octet-stream"
        return content_type

    def _get_s3_resource_url(self, file_key):
        return f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"

    def _upload_to_s3(self, file, file_key):
        s3 = self._get_s3_client()
        try:
            s3.upload_fileobj(
                file,
                AWS_BUCKET_NAME,
                file_key,
                ExtraArgs={
                    "ContentType": self._get_content_type(file.name),
                    "ContentDisposition": "inline",
                },
            )
        except (NoCredentialsError, ClientError, BotoCoreError) as e:
            print(f"Erreur Upload S3: {e}")
            raise CloudUploadError("Échec de l'upload vers S3")

    def _delete_from_s3(self, file_key):
        s3 = self._get_s3_client()
        try:
            s3.delete_object(Bucket=AWS_BUCKET_NAME, Key=file_key)
            return True
        except Exception as e:
            print(f"Erreur Upload S3: {e}")
            raise CloudUploadError("Échec de la suppression depuis S3")

    def save_within_folder(self, file, folder_album_id) -> str:
        file_name = self._generate_unique_name(file.name)

        file_key = f"{folder_album_id}/{file_name}"

        if DEBUG:
            file_key = f"debug_{file_key}"

        self._upload_to_s3(file, file_key)
        return self._get_s3_resource_url(file_key)

    def save(self, file) -> str:
        file_key = self._generate_unique_name(file.name)

        if DEBUG:
            file_key = f"debug_{file_key}"

        self._upload_to_s3(file, file_key)

        return self._get_s3_resource_url(file_key)

    def delete(self, file_url: str) -> bool:
        if file_url is None or file_url == "":
            return True

        print("Deleting file from cloud:", file_url)

        file_key = file_url.split("/")[-1]

        return self._delete_from_s3(file_key)
