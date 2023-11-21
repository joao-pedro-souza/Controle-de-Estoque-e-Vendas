import flet as ft
from banco_de_dados import BancoDeDados

db = BancoDeDados()


class VendasDoMes:
    def __init__(self, page):
        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text('id')),
                ft.DataColumn(ft.Text('Nome')),
                ft.DataColumn(ft.Text('Cliente')),
                ft.DataColumn(ft.Text('Preço Unitário')),
                ft.DataColumn(ft.Text('Unidades Vendidas')),
                ft.DataColumn(ft.Text('Preço Total')),
                ft.DataColumn(ft.Text('Data')),
                ft.DataColumn(ft.Text('Hora'))
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

        self.carregar_vendas()

    def carregar_vendas(self):
        tabela_produtos = db.select_vendas_mes()
        colunas = [coluna[0] for coluna in db.select_colunas()]
        produtos = [dict(zip(colunas, produto)) for produto in tabela_produtos]

        for produto in produtos:

            self.tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(produto['id'])),
                        ft.DataCell(ft.Text(produto['nome'])),
                        ft.DataCell(ft.Text(produto['cliente'])),
                        ft.DataCell(ft.Text(produto['preco_unitario'])),
                        ft.DataCell(ft.Text(produto['unidades_vendidas'])),
                        ft.DataCell(ft.Text(produto['preco_total'])),
                        ft.DataCell(ft.Text(produto['data'])),
                        ft.DataCell(ft.Text(produto['hora']))

                    ]
                )
            )

    def atualizar_vendas(self):
        self.tabela.rows.clear()
        self.carregar_vendas()
        self.tabela.update()
