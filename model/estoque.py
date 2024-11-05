def criar_tabelas(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos(
        id INT auto_increment PRIMARY KEY,
        nomeProduto VARCHAR(50) NOT NULL,
        preco VARCHAR(50) NOT NULL,
        quantidade VARCHAR(50) NOT NULL)
    """)