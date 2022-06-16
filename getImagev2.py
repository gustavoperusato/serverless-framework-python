import boto3
from os.path import exists

def getImage(bucket):
    '''    
    Esta função faz uma busca nos arquivos do bucket e possibilita o download.
    
    Estrutura:
    - Recebe o parâmetro "bucket" que refere-se ao bucket do AWS S3 a ser consultado;
    - Procura pelo bucket;
    - Caso não entre, retornará um erro 'Bucket not found!';
    - Caso encontre, lista todos os arquivos e possibilita o download, solicitando
    a key do arquivo.
    - Se uma key for passada, chama a função downloadImage() com os referidos parâmetros.
        
    '''
    
    s3_client = boto3.client('s3')

    try:
        response = s3_client.list_objects(Bucket=bucket)
        for item in response['Contents']:
            print(item['Key'])
        print('Total: ' + str(len(response['Contents'])) + ' files')
    except:
        raise Exception('Bucket not found!')
    
    if response:
        key = input('To download, paste the key:')
        downloadImage(bucket,key)
    
def downloadImage(bucket,s3objectkey):
    '''    
    Esta função faz o download do arquivo solicitado.
    
    Estrutura:
    - Recebe os parâmetros "bucket" e "s3objectkey" que referem-se,
    respectivamente, ao bucket do AWS S3 e a key do arquivo a ser baixado;
    - Converte a key para ser utilizada como nome do arquivo no download;
    - Caso já exista um arquivo com o mesmo nome na pasta raíz, retorna
    um erro de arquivo já existente;
    - Caso o arquivo não exista, efetua o download do mesmo na pasta raíz.
    '''
    s3 = boto3.resource('s3')

    filepath = s3objectkey.replace('/','_')
    
    if exists(filepath):
        raise Exception('File already exists in your root folder!')
        
    else:
        s3.meta.client.download_file(
                bucket,
                s3objectkey,
                filepath
            )
        print('File downloaded in your root folder')
        
