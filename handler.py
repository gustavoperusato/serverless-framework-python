import boto3
import os
import uuid
from urllib.parse import unquote_plus
from PIL import Image

s3_client = boto3.client('s3')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('sls-package-python-dev')

def extractMetadata(event, context):

    record = event['Records']
    s3_data = record[0]['s3']
    timestamp = record[0]['eventTime']
    bucket_name = s3_data['bucket']['name']
    obj_key = unquote_plus(s3_data['object']['key'])
    
    tmp_key = obj_key.replace('/', '')
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmp_key)
    s3_client.download_file(bucket_name, obj_key, download_path)
    
    img = Image.open(download_path)
    img_dimensions = img.size
    file_size = os.stat(download_path).st_size
    
    img_data = {
        'created_timestamp' : timestamp ,
        's3objectkey' : obj_key,
        'img_width' : img_dimensions[0],
        'img_heigth' : img_dimensions[1],
        'file_size' : file_size
        }

    print(img_data)

    table.put_item(Item=img_data)