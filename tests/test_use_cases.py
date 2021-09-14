import pytest
from tests.fixtures import image, s3_event, s3_client, thumbnail_image, BUCKET, KEY, THUMBNAIL_KEY
from thumbnail_image.use_cases import UploadThumbnailImageToS3
from thumbnail_image.utils import FileUtils


def test_upload_thumbnail_to_s3(s3_client):
    use_case = UploadThumbnailImageToS3(s3_client)
    url = use_case.execute(BUCKET, KEY)

    assert url.endswith('_thumbnail.png')
