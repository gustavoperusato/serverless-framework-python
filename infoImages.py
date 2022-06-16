import boto3
import pandas as pd
import json

def infoImages():
    '''    
    Esta função faz uma busca nos items armazenados no DynamoDB e retorna as infomações:
    - 'largestImage': Que refere-se a key da imagem de maior tamanho;
    - 'smallestImage': Que refere-se a key da imagem de menor tamanho;
    - 'quantityByTypes': Que informa os tipos de imagens armazenados e suas respectivas
    quantidades.
    
    Estrutura:
    - Não recebe nenhum parâmetro;
    - Consulta os itens na table prestabelecida;
    - Retorna as informações já citadas ou um erro, caso a table esteja vazia
        
    '''
    dynamodb = boto3.client("dynamodb")
    response = dynamodb.scan(TableName='sls-package-python-dev')
    items = []

    for item in response['Items']:
        items.append({
        'file_type' : item['file_type']['S'],
        's3objectkey' : item['s3objectkey']['S'],
        'file_size' : int(item['file_size']['N'])
        })

    df = pd.DataFrame(items)

    try:
        filetype_filter = df.groupby('file_type').nunique().to_json()

        info = {
            'largestImage': df.nlargest(1,'file_size')['s3objectkey'].values[0],
            'smallestImage': df.nsmallest(1,'file_size')['s3objectkey'].values[0],
            'quantityByTypes' : json.loads(filetype_filter)['s3objectkey']
        }
        
        return info

    except:
        raise Exception('Your table is empty!')