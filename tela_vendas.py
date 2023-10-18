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

        self.adicionar_venda = ft.ElevatedButton(
            'Adicionar',
            on_click=self.adicionar_venda
        )

        self.tela = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.selecao_produto,
                        self.adicionar_venda
                    ]
                )
            ]
        )

        self.carregar_produtos_dropdown()

    def carregar_produtos_dropdown(self):
        tabela_produtos = db.select_todos_produtos()
        colunas = [coluna[0] for coluna in db.select_colunas()]
        produtos = [dict(zip(colunas, produto)) for produto in tabela_produtos]

        for produto in produtos:
            self.selecao_produto.options.append(
                ft.dropdown.Option(produto['nome'])
            )

    def atualizar_produtos(self, e):
        self.selecao_produto.options.clear()
        self.carregar_produtos_dropdown()
        self.page.update()

    def adicionar_venda(self, e):
        produto = db.select_produto(self.selecao_produto.value)
        
        id = produto[0]
        nome = produto[1]
        preco_compra = produto[2]
        preco_venda = produto[3]
        quantidade_estoque = produto[4]
        limite_estoque = produto[5]

        self.tela.controls.append(
            ft.Row(
                controls=[
                    ft.Text(id),
                    ft.Text(nome),
                    ft.Text(preco_compra),
                    ft.Text(preco_venda),
                    ft.Text(quantidade_estoque),
                    ft.Text(limite_estoque)
                ]
            )
        )
        
        self.page.update()