from PIL import Image
import pytest

from thumbnail_image.utils import AWSUtils, ImageUtils, FileUtils
from tests.fixtures import image, s3_event, s3_client, thumbnail_image, BUCKET, KEY, THUMBNAIL_KEY


def test_get_bucket_and_key(s3_event: dict):
    bucket, key = AWSUtils.get_s3_data(s3_event)
    assert bucket == BUCKET
    assert key == KEY


def test_get_s3_image(s3_client, image: Image):
    file = AWSUtils.download_s3_object(BUCKET, KEY, s3_client)
    img = ImageUtils.bytes_to_image(file)
    assert img == image


def test_image_to_thumbnail(image: Image, thumbnail_image: Image):    
    img = ImageUtils.image_to_thumbnail(image)
    assert img.size == thumbnail_image.size


def test_upload_image_to_s3(s3_client, thumbnail_image: Image):
    bytes = ImageUtils.image_to_bytes(thumbnail_image)
    ok = AWSUtils.upload_to_s3(BUCKET, THUMBNAIL_KEY, bytes, s3_client)
    assert ok == True


def test_s3_url(s3_client):
    url = AWSUtils.s3_url(BUCKET, THUMBNAIL_KEY, s3_client)
    assert url.endswith('_thumbnail.png')
    assert 's3' in url


def test_new_filename():
    filename = FileUtils.new_filename(KEY)
    assert filename == THUMBNAIL_KEY


def test_image_to_bytes(image: Image):
    bytes = ImageUtils.image_to_bytes(image)
    assert bytes is not None


def test_bytes_to_image(image: Image):
    bytes = ImageUtils.image_to_bytes(image)
    img = ImageUtils.bytes_to_image(bytes)
    assert img.size == image.size
