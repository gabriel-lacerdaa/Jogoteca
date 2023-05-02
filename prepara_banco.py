import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash


print('Conectando...')
try:
    conn = mysql.connector.connect(
        host='bancoaws.cwk0wcobxxss.us-east-1.rds.amazonaws.com',
        user='admin',
        password='123456789'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuario ou senha')
    else:
        print(err)


cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `Jogoteca`;")

cursor.execute("CREATE DATABASE `Jogoteca`;")

cursor.execute("USE `Jogoteca`;")

TABLES = {}

TABLES["Jogos"] = ('''
    CREATE TABLE `jogos` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `nome` VARCHAR(50) NOT NULL,
        `categoria` VARCHAR(40) NOT NULL,
        `console` VARCHAR(20) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

TABLES["Usuarios"] = ('''
    CREATE TABLE `usuarios` (
        `nome` VARCHAR(50) NOT NULL,
        `nickname` VARCHAR(8) NOT NULL,
        `senha` VARCHAR(100) NOT NULL,
        PRIMARY KEY (`nickname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print(f"Criando tabela {tabela_nome}", end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Ja existe")
        else:
            print(err.msg)
    else:
        print("OK")


usuarios_sql = "INSERT INTO usuarios(nome, nickname, senha) VALUES (%s, %s, %s)"

#Aqui ao inves de salvar a senha direto no bancos, estou salvando um hash, para criptografar a senha do usuario
usuarios = [
    ("Gabriel", "admin", generate_password_hash("admin").decode('utf-8')),
    ("usuarioTeste", 'Teste', generate_password_hash("senhateste").decode('utf-8'))
]

cursor.executemany(usuarios_sql, usuarios)

conn.commit()

cursor.execute("SELECT * FROM Jogoteca.usuarios")
print("-"*10+' Usuarios '+'-'*10)
for user in cursor.fetchall():
    print(user[1])


# inserindo jogos
jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
jogos = [
      ('Tetris', 'Puzzle', 'Atari'),
      ('God of War', 'Hack n Slash', 'PS2'),
      ('Mortal Kombat', 'Luta', 'PS2'),
      ('Valorant', 'FPS', 'PC'),
      ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
      ('Need for Speed', 'Corrida', 'PS2'),
]
cursor.executemany(jogos_sql, jogos)

cursor.execute('select * from Jogoteca.jogos')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
