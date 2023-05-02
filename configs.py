import os

#secret key para colocar uma camada de criptografia, para os cookies
SECRET_KEY = 'senhamuitoultasecreta'

infos_de_conexao = {
    'SGBD': 'mysql+mysqlconnector',
    'usuario': 'admin',
    'senha': '123456789',
    'servidor': 'bancoaws.cwk0wcobxxss.us-east-1.rds.amazonaws.com',
    'database': 'Jogoteca'
}

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = infos_de_conexao["SGBD"],
    usuario = infos_de_conexao["usuario"],
    senha = infos_de_conexao["senha"],
    servidor = infos_de_conexao["servidor"],
    database = infos_de_conexao["database"],
    )

'''
essa variavel é para especificar o caminho absoluto para o diretório uploads, para salvar os arquivos
que são enviados para o servidor
Para entender melhor essa linha:
print(os.path.abspath(__file__)) -> retorna o caminho absoluto deste arquivo
print(os.path.dirname(os.path.abspath(__file__))+ '/uploads') -> aqui ele retorna o
diretorio onde esta esse arquivo concatenado com o /uploads, que é o nome da pasta para salvar os uploads
'''
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'