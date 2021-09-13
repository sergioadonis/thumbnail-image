import os
import json
from PIL import Image
import boto3
from botocore.stub import Stubber
from botocore.response import StreamingBody
import pytest

import utils


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
BUCKET = 'lacuracaoonline-data'
KEY = 'pictures/Screenshot (1).png'
THUMBNAIL_KEY = 'pictures/Screenshot (1)_thumbnail.png'


@pytest.fixture()
def image():
    path = os.path.join(BASE_DIR, 'fixtures', 'Screenshot (1).png')
    return Image.open(path)


@pytest.fixture()
def thumbnail_image():
    path = os.path.join(BASE_DIR, 'fixtures', 'Screenshot (1)_thumbnail.png')
    return Image.open(path)


@pytest.fixture()
def s3_event():
    path = os.path.join(BASE_DIR, 'fixtures', 'S3TestEvent.json')
    with open(path, 'r') as data:
        return json.load(data)
        

@pytest.fixture()
def s3_client(image: Image, thumbnail_image: Image):
    s3 = boto3.client('s3')
    stubber = Stubber(s3)

    path  = os.path.join('tests', 'fixtures', 'S3GetObjectResponse.json')
    with open(path, 'r') as data:
        response = json.load(data)
        expected = {
            'Bucket': BUCKET,
            'Key': KEY
        }
        response['Body'] = StreamingBody(image, image.size)
        stubber.add_response('get_object', response, expected_params=expected)

    path  = os.path.join('tests', 'fixtures', 'S3PutObjectResponse.json')
    with open(path, 'r') as data:        
        response = json.load(data)
         
        expected = {
            'Body': StreamingBody(thumbnail_image, thumbnail_image.size),
            'ContentType': 'image/png',
            'Bucket': BUCKET,
            'Key': THUMBNAIL_KEY
        }
        stubber.add_response('put_object', response, expected)
    
    return s3


def test_get_bucket_and_key(s3_event: dict):
    event_bucket, event_key = utils.get_bucket_and_key(s3_event)
    assert event_bucket == BUCKET
    assert event_key == KEY


def test_get_s3_image(s3_client, image: Image):
    file = utils.get_s3_file(BUCKET, KEY, s3_client)
    img = utils.bytes_to_image(file)
    assert img == image


def test_image_to_thumbnail(image: Image, thumbnail_image: Image):    
    img = utils.image_to_thumbnail(image)
    assert img.size == thumbnail_image.size


def test_upload_image_to_s3(s3_client, thumbnail_image: Image):
    bytes = utils.image_to_bytes(thumbnail_image)
    url = utils.upload_to_s3(BUCKET, THUMBNAIL_KEY, bytes, s3_client)
    assert url.endswith(THUMBNAIL_KEY)


def test_new_filename():
    filename = utils.new_filename(KEY)
    assert filename == THUMBNAIL_KEY
