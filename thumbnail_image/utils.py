from io import BytesIO
from PIL import Image, ImageOps
import urllib.parse


class AWSUtils:

    @staticmethod
    def get_s3_data(event: dict) -> tuple:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        key = urllib.parse.unquote_plus(key)
        return (bucket, key)


    @staticmethod
    def download_s3_object(bucket: str, key: str, s3_client) -> BytesIO:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            content = response['Body'].read()
            return BytesIO(content)

    @staticmethod
    def upload_to_s3(bucket: str, key: str, file: BytesIO, s3_client) -> str:
        response = s3_client.put_object(
            # ACL='public-read',
            Body=file,
            Bucket=bucket,
            ContentType='image/png',
            Key=key
        )
        print(response)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True

    @staticmethod
    def s3_url(bucket: str, key: str, s3_client):
        return urllib.parse.quote(f'{s3_client.meta.endpoint_url}/{bucket}/{key}')


class ImageUtils:

    @staticmethod
    def bytes_to_image(bytes: BytesIO) -> Image:
        return Image.open(bytes)

    @staticmethod
    def image_to_thumbnail(image: Image, size: int = 128) -> Image:
        return ImageOps.fit(image, (size, size,), Image.ANTIALIAS)

    @staticmethod
    def image_to_bytes(image: Image) -> BytesIO:
        bytes = BytesIO()
        image.save(bytes, 'PNG')
        bytes.seek(0)
        return bytes


class FileUtils:

    @staticmethod
    def new_filename(key: str) -> str:
        key_split = key.rsplit('.', 1)
        return key_split[0] + '_thumbnail.png'
    