import boto3
import utils


s3 = boto3.client('s3')


def hello(event, context):
    print(event)
    bucket, key = utils.get_bucket_and_key(event)

    if not key.endswith('_thumbnail.png'):
        bytes = utils.get_s3_file(bucket, key, s3)
        image = utils.bytes_to_image(bytes)
        thumbnail = utils.image_to_thumbnail(image)
        thumbnail_key = utils.new_filename(key)
        url = utils.upload_to_s3(bucket, thumbnail_key, thumbnail, s3)

        return url
