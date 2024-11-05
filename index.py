import mysql.connector
import os
import msvcrt
from dotenv import load_dotenv
from model.estoque import criar_tabelas;

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
        return conexao
    except Exception as erro:
        print('Erro ao conectar ao banco de dados', erro)
    
    

def cadastrar():
    try:
        conexao = conectar_com_banco()
        cursor = conexao.cursor()
        cursor.execute("START TRANSACTION")

        cursor.execute("USE estoque")
        criar_tabelas(cursor)

        nomeProduto = input("Digite o nome do Produto: ")
        preco = input("Digite o preço do produto: ")
        quantidade = input("Digite a quantidade desse produto: ")

        cursor.execute("""
            INSERT INTO produtos (nomeProduto, preco, quantidade)
            VALUES (%s, %s, %s)
        """, (nomeProduto, preco, quantidade))
        cursor.execute("COMMIT")
        print("Produto cadastrado com sucesso")

    except Exception as erro:
        print('Erro ao conectar ao banco de dados', erro)
        cursor.execute("ROLLBACK")

    finally: 
        cursor.close()
        conexao.close()

# cadastrar('Coca-Cola', '5.00', 10)


def listar():
    try:
        conexao = conectar_com_banco()
        cursor = conexao.cursor()
        cursor.execute("USE estoque")
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
        produtos = [f'|Código: {produto[0]}, Produto: {produto[1]}, Preço: R${produto[2]}, Quantidade: {produto[3]}|' for produto in produtos ]
        print(produtos)
        print("\nProdutos listados com sucesso")
        return produtos

    except Exception as erro:
        print('Erro ao conectar ao banco de dados', erro)

    finally:
        cursor.close()
        conexao.close() 
# print(listar()[0]['nomeProduto'])

def buscar_por_id():
    try:
        conexao = conectar_com_banco()
        cursor = conexao.cursor()
        cursor.execute("USE estoque")
        idProduto = input("Digite o código do produto: ")
        cursor.execute("SELECT COUNT(*) FROM produtos WHERE id = %s", (idProduto,))
        existe = cursor.fetchone()[0]
        
        if existe == 0:
            return f"Produto com id {idProduto} não encontrado."

        cursor.execute("SELECT * FROM produtos WHERE id = %s", (idProduto,))
        produto = cursor.fetchone()
        
        produto = f'id: {produto[0]}, nomeProduto: {produto[1]}, preco: {produto[2]}, quantidade: {produto[3]}'
        print(produto)
        print("Produto listado com sucesso")
        return produto
    except Exception as erro:
        print('Erro ao conectar ao banco de dados', erro)
    finally:
        cursor.close()
        conexao.close()

def atualizar_produto():
    try:
        conexao = conectar_com_banco()
        cursor = conexao.cursor()
        cursor.execute("START TRANSACTION")
        cursor.execute("USE estoque")
        idProdutoAtualizar = input("Digite o código do produto que deseja atualizar: ")
        cursor.execute("SELECT COUNT(*) FROM produtos WHERE id = %s", (idProdutoAtualizar,))
        existe = cursor.fetchone()[0]
        
        if existe == 0:
            print(f"Produto com id {idProdutoAtualizar} não encontrado.")
            return
        
        nomeProdutoAtualizado = input("Digite o novo nome do produto: ")
        precoAtualizado = input("Digite o novo preço do produto: ")
        quantidadeAtualizada = input("Digite a quantidade atualizada: ")
        cursor.execute(f"""
                       UPDATE produtos 
                       SET nomeProduto = '{nomeProdutoAtualizado}',
                       preco = '{precoAtualizado}',
                       quantidade = '{quantidadeAtualizada}'
                        WHERE id = {idProdutoAtualizar}
                       """)
        cursor.execute("COMMIT")
        print(f"Produto com id {idProdutoAtualizar} foi atualizado.")

    except Exception as erro:
        print(f"Erro ao conectar ao banco de dados {erro}")

    finally:
        cursor.close()
        conexao.close()

# atualizar_produto(1, 'Mouse Tubarão', '28.00', '1')

def deletar_produto():
    try:
        conexao = conectar_com_banco()
        cursor = conexao.cursor()
        cursor.execute("START TRANSACTION")
        cursor.execute("USE estoque")
        idDeletado = input("Digite o código do produto que deseja remover: ")
        cursor.execute("SELECT COUNT(*) FROM produtos WHERE id = %s", (idDeletado,))
        existe = cursor.fetchone()[0]

        if existe > 0:
            cursor.execute("DELETE FROM produtos WHERE id = %s", (idDeletado,))
            cursor.execute("COMMIT")
            print(f"Produto com id {idDeletado} foi deletado.")
        else:
            print(f"Produto com id {idDeletado} não encontrado.")

    except Exception as erro:
        print(f"Erro ao conectar ao banco de dados {erro}")
    
    finally:
        cursor.close()
        conexao.close()


def cabeçalho(titulo):
    os.system("cls")
    print(titulo)
    print("-" * 30)


def voltar_para_main():
    print("Aperte qualquer tecla para voltar para o menu principal")
    msvcrt.getch()
    main()


def main():
    cabeçalho("Sistema de Estoque")
    
    print("1. Cadastrar Produto")
    print("2. Listar produtos")
    print("3. Buscar um produto especifico")
    print("4. Atualizar Produto")
    print("5. Deletar produto")
    print("6. Sair")
    opcao = input("Escolha uma opção: ")
    
    match opcao:

        case '1':
            cabeçalho("Página de cadastro de produto")
            
            cadastrar()
            
            voltar_para_main()

        case '2':
            cabeçalho("Página de listagem de produtos")
            listar()
            
            voltar_para_main()

        case '3':
            cabeçalho("Página de busca de produto")
            
            buscar_por_id()
            voltar_para_main()

        case '4':
            cabeçalho("Página de atualizar produto")
            
            atualizar_produto()
            voltar_para_main()

        case '5':
            cabeçalho("Página de deletar produto")
            
            deletar_produto()
            voltar_para_main()

        case '6':
            cabeçalho("Saindo do sistema")

        case _:
            cabeçalho("Opção inválida")
        

    


if __name__ == '__main__':
    main()