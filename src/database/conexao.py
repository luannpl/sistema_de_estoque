import mysql.connector
import os
from dotenv import load_dotenv
from model.produto_modal import criar_tabelas

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

def conectar_com_banco():
    try:
        conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE DATABASE IF NOT EXISTS estoque
                       """)
        
        cursor.execute("USE estoque")
        criar_tabelas(cursor)
        return conexao
    except Exception as erro:
        print("Erro ao conectar ao banco de dados", erro)