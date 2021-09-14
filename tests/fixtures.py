import json, os
import pytest
from PIL import Image
import boto3
from botocore.stub import Stubber
from botocore.response import StreamingBody


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
BUCKET = 'lacuracaoonline-data'
KEY = 'pictures/Screenshot (1).png'
THUMBNAIL_KEY = 'pictures/Screenshot (1)_thumbnail.png'


@pytest.fixture()
def s3_event():
    path = os.path.join(BASE_DIR, 'payloads', 'S3TestEvent.json')
    with open(path, 'r') as data:
        return json.load(data)


@pytest.fixture()
def image():
    path = os.path.join(BASE_DIR, 'images', 'Screenshot (1).png')
    return Image.open(path)


@pytest.fixture()
def thumbnail_image():
    path = os.path.join(BASE_DIR, 'images', 'Screenshot (1)_thumbnail.png')
    return Image.open(path)


@pytest.fixture()
def s3_client(image: Image, thumbnail_image: Image):
    s3 = boto3.client('s3')
    stubber = Stubber(s3)

    path  = os.path.join(BASE_DIR, 'payloads', 'S3GetObjectResponse.json')
    with open(path, 'r') as data:
        response = json.load(data)
        expected = {
            'Bucket': BUCKET,
            'Key': KEY
        }
        response['Body'] = StreamingBody(image, image.size)
        stubber.add_response('get_object', response, expected_params=expected)

    path  = os.path.join(BASE_DIR, 'payloads', 'S3PutObjectResponse.json')
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
