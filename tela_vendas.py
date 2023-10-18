import flet as ft
from banco_de_dados import BancoDeDados

db = BancoDeDados()


class TelaVendas:
    def __init__(self, page):
        self.page = page

        self.selecao_produto = ft.Dropdown(
            width=200,
            options=[]
        )

        self.tela = ft.Column(
            controls=[
                self.selecao_produto
            ]
        )

        self.carregar_produtos()

    def carregar_produtos(self):
        tabela_produtos = db.select_produtos()
        colunas = [coluna[0] for coluna in db.select_colunas()]
        produtos = [dict(zip(colunas, produto)) for produto in tabela_produtos]

        for produto in produtos:

            self.selecao_produto.options.append(
                ft.dropdown.Option(produto['nome'])
            )

    def atualizar_produtos(self, e):
        self.selecao_produto.options.clear()
        self.carregar_produtos()
        self.page.update()
