from database.conexao import conectar_com_banco
class ProdutoController:
    def cadastrar(self):
        try:
            conexao = conectar_com_banco()
            cursor = conexao.cursor()
            cursor.execute("START TRANSACTION")

            cursor.execute("USE estoque")
            

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
            print("Erro ao conectar ao banco de dados", erro)
            cursor.execute("ROLLBACK")

        finally: 
            cursor.close()
            conexao.close()



    def listar(self):
        try:
            conexao = conectar_com_banco()
            cursor = conexao.cursor()
            cursor.execute("USE estoque")
            cursor.execute("SELECT * FROM produtos")
            produtos = cursor.fetchall()
            produtos = [f"|Código: {produto[0]}, Produto: {produto[1]}, Preço: R${produto[2]}, Quantidade: {produto[3]}|" for produto in produtos ]
            print(produtos)
            print("\nProdutos listados com sucesso")
            return produtos

        except Exception as erro:
            print("Erro ao conectar ao banco de dados", erro)

        finally:
            cursor.close()
            conexao.close() 


    def buscar_por_id(self):
        try:
            conexao = conectar_com_banco()
            cursor = conexao.cursor()
            cursor.execute("USE estoque")
            idProduto = input("Digite o código do produto: ")
            cursor.execute("SELECT COUNT(*) FROM produtos WHERE id = %s", (idProduto,))
            existe = cursor.fetchone()[0]
            
            if existe == 0:
                sem_produto = f"Produto com id {idProduto} não encontrado."
                print(sem_produto)
                return sem_produto

            cursor.execute("SELECT * FROM produtos WHERE id = %s", (idProduto,))
            produto = cursor.fetchone()
            
            produto = f"id: {produto[0]}, nomeProduto: {produto[1]}, preco: {produto[2]}, quantidade: {produto[3]}"
            print(produto)
            print("Produto listado com sucesso")
            return produto
        except Exception as erro:
            print("Erro ao conectar ao banco de dados", erro)
        finally:
            cursor.close()
            conexao.close()

    def atualizar_produto(self):
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
                        SET nomeProduto = %s,
                        preco = %s,
                        quantidade = %s
                            WHERE id = %s
                        """, (nomeProdutoAtualizado, precoAtualizado, quantidadeAtualizada, idProdutoAtualizar))
            cursor.execute("COMMIT")
            print(f"Produto com id {idProdutoAtualizar} foi atualizado.")

        except Exception as erro:
            print(f"Erro ao conectar ao banco de dados {erro}")

        finally:
            cursor.close()
            conexao.close()


    def deletar_produto(self):
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