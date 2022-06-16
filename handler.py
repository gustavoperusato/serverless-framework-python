import os
import boto3
import uuid
import json
from PIL import Image
from urllib.parse import unquote_plus

table_name = 'sls-package-python-dev'

def extractMetadata(event, context):
    '''
    Esta função extrai os metadados das imagens automaticamente quando
    essas são carregadas no bucket do AWS S3.
    
    Estrutura:
    - Recebe os parâmetros "event" e "context" - apesar de este último não
    ser utilizado, mantém-se no código respeitando o padrão AWS Lambda;
    - Efetua o download temporário da imagem para extrair os metadados,
    através da biblioteca Pillow;
    - Converte a s3objectkey, substituindo a '/' e os espaços por '_' 
    para evitar problemas futuros no consumo da API;
    - Cria um dicionário com os dados e envia o item à table no DynamoDB;
    - Imprime os dados enviados para fins de log.
        
    '''
    
    s3_client = boto3.client('s3')
    table = boto3.resource("dynamodb").Table(table_name)
    record = event['Records']
    
    timestamp = record[0]['eventTime']
    s3_data = record[0]['s3']
    bucket_name = s3_data['bucket']['name']
    obj_key = unquote_plus(s3_data['object']['key'])
    tmp_key = obj_key.replace('/', '')
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmp_key)
    
    s3_client.download_file(
        bucket_name,
        obj_key,
        download_path
        )
    
    img = Image.open(download_path)
    img_dimensions = img.size
    file_size = os.stat(download_path).st_size
    
    s3objectkey = obj_key.replace('/', '_').replace(' ','_')
    
    img_metadata = {
        'created_timestamp' : timestamp ,
        's3objectkey' : s3objectkey,
        'img_width' : img_dimensions[0],
        'img_heigth' : img_dimensions[1],
        'file_size' : file_size,
        'file_type' : img.format
        }

    table.put_item(Item=img_metadata)
    
    print(img_metadata)
    
def getMetadata(event,context):
    '''    
    Esta função é chamada por meio de endpoint e busca os metadados
    armazenados no DynamoDB, retornando as informações conforme a key
    passada no caminho da requisição.
    
    Estrutura:
    - Recebe os parâmetros "event" e "context" - apesar de este último não
    ser utilizado, mantém-se no código respeitando o padrão AWS Lambda;
    - Busca pela key passada no final da requisição na table do DynamoDB;
    - Ao passar a s3objectkey da imagem no s3, deve-se substituir a '/' e
    os espaçoes por '_';
    - Retorna os metadados armazenadados, caso algum item seja encontrado.
    Do contrário, retorna um "Internal Server Error", statusCode: 503.
    - Caso o caminho passado na requisição não encontre um endpoint válido,
    retornará um erro "Missing Authentication Token", status code: 403.
        
    '''
    
    dynamodb = boto3.client("dynamodb")
    
    s3objectkey = event['pathParameters']['s3objectkey']

    img_metadata = dynamodb.get_item(
        TableName=table_name,
        Key={'s3objectkey': {
            'S': s3objectkey
            }})
        
    if img_metadata['Item']:
        return {
            'statusCode': 200,
            'body': json.dumps(img_metadata)
        }