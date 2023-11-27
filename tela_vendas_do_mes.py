import flet as ft
import pandas as pd
import locale
from banco_de_dados import BancoDeDados
from datetime import datetime

locale.setlocale(locale.LC_ALL, '')

db = BancoDeDados()


def salvar_planilha_mes():
    mes = datetime.now().strftime('%B')
    colunas = [coluna[0] for coluna in db.select_colunas()]
    planilha = pd.DataFrame(db.select_vendas_mes(), columns=colunas)
    planilha.to_excel(f'vendas_mes_{mes}.xlsx', index=False)


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
        salvar_planilha_mes()

    def carregar_vendas(self):
        tabela_produtos = db.select_vendas_mes()
        self.colunas = [coluna[0] for coluna in db.select_colunas()]
        produtos = [dict(zip(self.colunas, produto))
                    for produto in tabela_produtos]

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
        salvar_planilha_mes()
