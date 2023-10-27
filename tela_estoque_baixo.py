import flet as ft
from banco_de_dados import BancoDeDados

db = BancoDeDados()


class EstoqueBaixo:
    def __init__(self, page):
        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text('id')),
                ft.DataColumn(ft.Text('Nome')),
                ft.DataColumn(ft.Text('Preço Compra')),
                ft.DataColumn(ft.Text('Preço Venda')),
                ft.DataColumn(ft.Text('Quantidade Estoque')),
                ft.DataColumn(ft.Text('Estoque Ideal'))
            ],
            rows=[]
        )

        self.tela = ft.Column(
            controls=[
                ft.Row(
                    controls=[self.tabela],
                    alignment='CENTER'
                )
            ]
        )

        self.carregar_estoque_baixo()

    def carregar_estoque_baixo(self):
        tabela_produtos = db.select_estoque_baixo()
        colunas = [coluna[0] for coluna in db.select_colunas()]
        produtos = [dict(zip(colunas, produto)) for produto in tabela_produtos]

        for produto in produtos:

            self.tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(produto['id'])),
                        ft.DataCell(ft.Text(produto['nome'])),
                        ft.DataCell(ft.Text(produto['preco_compra'])),
                        ft.DataCell(ft.Text(produto['preco_venda'])),
                        ft.DataCell(ft.Text(produto['quantidade_estoque'])),
                        ft.DataCell(ft.Text(produto['limite_estoque']))
                    ]
                )
            )

    def atualizar_estoque_baixo(self):
        self.tabela.rows.clear()
        self.carregar_estoque_baixo()
        self.tabela.update()
