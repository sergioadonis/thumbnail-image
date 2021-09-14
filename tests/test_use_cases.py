import pytest
from tests.fixtures import s3_event, s3_client, image, thumbnail_image
from thumbnail_image.use_cases import UploadThumbnailImageToS3


def test_upload_thumbnail_to_s3(s3_client, s3_event):
    use_case = UploadThumbnailImageToS3(s3_client)
    response = use_case.execute(s3_event)

    assert response is not None
