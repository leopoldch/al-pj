import boto3
from botocore.exceptions import NoCredentialsError
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

def save_to_cloud(file, folder_album_id=-1) -> str:
    file_name = f"{uuid4()}_{file.name}"
    if DEBUG:
        file_name = f"debug_{file_name}"
    if folder_album_id != -1:
        file_key = f"{folder_album_id}/{file_name}"
    else:
        file_key = file_name

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )

    content_type, _ = mimetypes.guess_type(file.name)
    content_type = content_type or "application/octet-stream"

    try:
        s3.upload_fileobj(
            file,
            AWS_BUCKET_NAME,
            file_key,
            ExtraArgs={
                "ContentType": content_type,
                "ContentDisposition": "inline",
            },
        )

        url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
        return url

    except NoCredentialsError:
        print("Credentials invalides.")
        return ""


def delete_from_cloud(file_url: str) -> bool:
    if file_url is None or file_url == "":
        return True
    print("Deleting file from cloud:", file_url)
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )

    file_key = file_url.split("/")[-1]

    try:
        s3.delete_object(Bucket=AWS_BUCKET_NAME, Key=file_key)
        return True
    except Exception as e:
        print(f"Échec de la suppression du fichier : {e}")
        return False
