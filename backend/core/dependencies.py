from core.interface.aws import AwsPhotoSaver
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

environment = os.getenv("PHOTO_STORAGE_TYPE", "AWS")

if environment == "AWS":
    AwsPhotoSaver()
else:
    # photo_repository = LocalPhotoSaver()
    # if we want to change later
    pass
