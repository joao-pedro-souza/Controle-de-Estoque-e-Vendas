import flet as ft
from banco_de_dados import BancoDeDados

db = BancoDeDados()


class TelaVendas:
    def __init__(self, page):
        self.page = page

        self.vendas = []

        self.selecao_produto = ft.Dropdown(
            width=200,
            options=[]
        )

        self.unidades_vendidas = ft.TextField(
            label='Unidades Vendidas'
        )

        self.cliente = ft.TextField(
            label='Cliente'
        )

        self.btn_adicionar_venda = ft.ElevatedButton(
            'Adicionar',
            on_click=self.adicionar_venda
        )

        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text('id')),
                ft.DataColumn(ft.Text('Nome')),
                ft.DataColumn(ft.Text('Cliente')),
                ft.DataColumn(ft.Text('Preço Unitário')),
                ft.DataColumn(ft.Text('Unidades Vendidas')),
                ft.DataColumn(ft.Text('Preço Total')),
                ft.DataColumn(ft.Text(''))
            ],
            rows=[]
        )

        self.tela = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.selecao_produto,
                        self.cliente,
                        self.unidades_vendidas,
                        self.btn_adicionar_venda
                    ]
                ),
                ft.Row(
                    controls=[self.tabela],
                    alignment='CENTER'
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
        cliente = self.cliente.value
        nome = produto[1]
        preco_venda = produto[3]
        unidades_vendidas = self.unidades_vendidas.value
        preco_total = int(unidades_vendidas) * float(preco_venda)

        self.tabela.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(id)),
                    ft.DataCell(ft.Text(nome)),
                    ft.DataCell(ft.Text(cliente)),
                    ft.DataCell(ft.Text(preco_venda)),
                    ft.DataCell(ft.Text(unidades_vendidas)),
                    ft.DataCell(ft.Text(preco_total)),
                    ft.DataCell(ft.Text(''))
                ]
            )
        )

        self.vendas.append([id, nome, cliente, preco_venda, unidades_vendidas, preco_total])
        db.cadastrar_venda(id, nome, cliente, preco_venda, unidades_vendidas, preco_total)

        self.page.update()

    