import boto3
from os.path import exists

def getImage(s3objectkey):
    '''    
    Esta função busca no bucket o arquivo solicitado e faz o download.
    
    Estrutura:
    - Recebe o parâmetro "s3objectkey" que referem-se à key do arquivo
    a ser baixado;
    - Converte a key para ser utilizada como nome do arquivo no download;
    - Caso já exista um arquivo com o mesmo nome na pasta raíz, retorna
    um erro de arquivo já existente;
    - Caso o arquivo não exista, efetua o download do mesmo na pasta raíz.
    '''

    s3 = boto3.resource('s3')
    
    obj_key = s3objectkey.replace('uploads_','uploads/').replace('_',' ')
    
    if exists(s3objectkey):
        raise Exception('File already exists in your root folder!')
        
    else:
        s3.meta.client.download_file(
                'store-imgs-gp',
                obj_key,
                s3objectkey
            )
        print('File downloaded in your root folder!')
        
