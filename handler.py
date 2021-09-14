import boto3
from thumbnail_image.use_cases import UploadThumbnailImageToS3


s3_client = boto3.client('s3')


def hello(event, context):
    print(event)
    use_case = UploadThumbnailImageToS3(s3_client)
    return use_case.execute(event)
