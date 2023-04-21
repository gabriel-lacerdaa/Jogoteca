import mysql.connector
from mysql.connector import errorcode


print('Conectando...')
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin'
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
    CREATE TABLE `Jogos` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `nome` VARCHAR(50) NOT NULL,
        `categoria` VARCHAR(40) NOT NULL,
        `console` VARCHAR(20) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

TABLES["Usuarios"] = ('''
    CREATE TABLE `Usuarios` (
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


usuarios_sql = "INSERT INTO Usuarios(nome, nickname, senha) VALUES (%s, %s, %s)"

usuarios = [
    ("Gabriel", "Lacierda", "senha"),
    ("usuarioTeste", 'Teste', 'senhateste')
]

cursor.executemany(usuarios_sql, usuarios)

conn.commit()

cursor.execute("SELECT * FROM Jogoteca.Usuarios")
print("-"*10+' Usuarios '+'-'*10)
for user in cursor.fetchall():
    print(user[1])


conn.close()