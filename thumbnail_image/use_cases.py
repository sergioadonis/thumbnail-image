from botocore.utils import S3_ACCELERATE_WHITELIST
from thumbnail_image.utils import AWSUtils, ImageUtils, FileUtils


class UploadThumbnailImageToS3:

    _s3_client = None

    def __init__(self, s3_client) -> None:
        self._s3_client = s3_client
    
    def execute(self, bucket: str, key: str) -> str:
        if not key.endswith('_thumbnail.png'):
            bytes = AWSUtils.download_s3_object(bucket, key, self._s3_client)
            image = ImageUtils.bytes_to_image(bytes)
            thumbnail_image = ImageUtils.image_to_thumbnail(image)
            thumbnail_bytes = ImageUtils.image_to_bytes(thumbnail_image)
            thumbnail_key = FileUtils.new_filename(key)
            if AWSUtils.upload_to_s3(bucket, thumbnail_key, thumbnail_bytes, self._s3_client):
                return AWSUtils.s3_url(bucket, thumbnail_key, self._s3_client)
