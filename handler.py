import boto3
from thumbnail_image.utils import AWSUtils
from thumbnail_image.use_cases import UploadThumbnailImageToS3


s3_client = boto3.client('s3')


def hello(event, context):
    print(event)
    bucket, key = AWSUtils.get_s3_data(event)
    use_case = UploadThumbnailImageToS3(s3_client)
    return use_case.execute(bucket, key)
