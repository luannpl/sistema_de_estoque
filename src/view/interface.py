import os
import msvcrt
from controller.produto_controller import cadastrar, listar, buscar_por_id, atualizar_produto, deletar_produto

class Interface:
    def cabeçalho(self, titulo):  
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        print(titulo)
        print("-" * 30)

    def voltar_para_main(self):
        print("Aperte qualquer tecla para voltar para o menu principal")
        msvcrt.getch()
        self.main()

    def main(self):
        self.cabeçalho("Sistema de Estoque")
        
        print("1. Cadastrar Produto")
        print("2. Listar produtos")
        print("3. Buscar um produto especifico")
        print("4. Atualizar Produto")
        print("5. Deletar produto")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")
        
        match opcao:
            case "1":
                self.cabeçalho("Página de cadastro de produto")
                cadastrar()
                self.voltar_para_main()

            case "2":
                self.cabeçalho("Página de listagem de produtos")
                listar()
                self.voltar_para_main()

            case "3":
                self.cabeçalho("Página de busca de produto")
                buscar_por_id()
                self.voltar_para_main()

            case "4":
                self.cabeçalho("Página de atualizar produto")
                atualizar_produto()
                self.voltar_para_main()

            case "5":
                self.cabeçalho("Página de deletar produto")
                deletar_produto()
                self.voltar_para_main()

            case "6":
                self.cabeçalho("Saindo do sistema")

            case _:
                self.cabeçalho("Opção inválida")