<h2> Desafio Técnico </h2>

<hr></hr>

<h3>Dependências adicionais:</h3>

  ##
  - <b>Plugin Serverless Python Requirements</b>
    <p><b>Descrição:</b></p>
    <p>Este plugin cria uma imagem docker com as dependências necessárias para rodar os imports do código python, nas diferentes instâncias em que a lambda rodar</p>
    <p><b>Instalação:</b></p>
    <code>sls plugin install -n serverless-python-requirements</code>

<ol></ol>


  ##
  - <b>Docker</b>
    <p><b>Descrição:</b></p>
    <p>É necessário que o Docker esteja instalado e aberto no momento do deploy para o funcionamento do plugin citado acima</p>
    <p><b>Instalação:</b></p>
    <p>Efetuar download através do link https://www.docker.com/products/docker-desktop/ e instalar.</p>
  
  <h4>Versões utilizadas:</h4>
  
  - <b>Docker: </b>20.10.16
  - <b>Node: </b> 16.15.1
  - <b>AWS CLI: </b>2.7.7 Python/3.9.11 Windows/10 exe/AMD64 prompt/off
  - <b>Serverless Framework: </b>
  - Core: 3.19.0
  - Plugin: 6.2.2
  - SDK: 4.3.2

  <hr></hr>

<h3>Alterações <i>serverless.yml</i></h3>
<p>Abaixo estão comentadas as alterações a serem feitas no arquivo <b><i>serverless.yml</b></i></p>
  
  ![image](https://user-images.githubusercontent.com/96849188/173989403-7d6634cc-0929-4994-ae34-c08e7d4ee268.png)
  ![image](https://user-images.githubusercontent.com/96849188/173989470-a7010962-6ebd-4365-9e63-f36298017c61.png)
  ![image](https://user-images.githubusercontent.com/96849188/174170909-90252d8d-d91c-49bc-9b3c-b57a4eee0ef9.png) 
  
<hr></hr>

<h3> Observações </h3>

  <p> As documentações de cada função encontram-se nos arquivos <b></i>handler.py</b></i>, <b><i>getImagev1.py</b></i>, <b><i>getImagev2.py</b></i> e <b><i>infoImages.py</b></i> e podem ser consultadas chamando a função python nativa <b><i>help(function)</b></i>.</p>
  

  <p> Abaixo estão listadas algumas observações referentes as funções:</p>

  ##
  - <b><i>extractMetadata()</b></i>

Devido as imagens estarem salvas na pasta <b><i>'upload/'</i></b> no bucket, tive que efetuar uma mudança na <i>s3objectkey</i> antes de passar ao DynamoDB, pois a chave que é gerada contém o nome da pasta em conjunto ao nome do arquivo, o que causa erro na requisição GET (elucidada na próxima função abaixo) pois a '/' leva à busca por um domínio inexistente.

  Por exemplo, ao subir uma imagem com o nome <b><i>'my image.png'</b></i>, a mesma receberá a <b><i>s3objectkey: 'upload/my image.png'</i></b> e, caso a chave subisse desta forma ao DynamoDB, não seria possível encontrá-la via GET. Desta forma, antes de subir, as barras e espaços são substituídos por '_' <i>(underline)</i>. Também inseri uma <i><b>print()</b></i> ao final do código para fins de log.

  ##
  - <b><i>getMetadata()</b></i>

Como já citado acima, ao utilizar essa função deve-se atentar as barras e espaços ao efetuar a requisição para que o item seja encontrado corretamente.
  
  ##
  - <b><i>getImage()</b></i>

Optei por fazer duas versões desta função (arquivos <b><i>getImagev1.py</i></b> e <b><i>getImagev2.py</i></b>, sendo que a versão 1 é uma forma mais "enxuta" e de acordo ao proposto e a versão 2 é uma forma mais elaborada e informativa.

  ##
  - <b><i>infoImages()</b></i>

Nesta função, optei por retornar as informações solicitadas em um dicionário. Há a possibilidade de, caso seja interessante, criar uma endpoint <b><i>'/infoimages'</i></b> para esta função, adicionando a linha de código: <code>return { 'statusCode': 200, 'body': json.dumps(info) }</code> ao final da função e os parâmetros <i>"event"</i> e <i>"context"</i>

<hr></hr>













