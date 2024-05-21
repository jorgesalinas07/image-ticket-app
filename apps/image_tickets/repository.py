from abc import ABC
from dotenv import load_dotenv

load_dotenv()

from cloudinary import uploader, config


class CloudStorageRepository(ABC):
    def upload_image(self, image_url):
        raise NotImplementedError

    def upload_video(self, video_url):
        raise NotImplementedError

    def upload_voice_record(self, rec_url):
        raise NotImplementedError


class CloudinaryRepository(CloudStorageRepository):
    def __init__(self):
        config(secure=True)

    def upload_image(self, image_url):
        uploader.upload(
            image_url,
            unique_filename=False,
            overwrite=True,
        )
