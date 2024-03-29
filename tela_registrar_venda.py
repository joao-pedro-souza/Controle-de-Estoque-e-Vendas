import flet as ft
from banco_de_dados import BancoDeDados
from cupom_fiscal import CupomFiscal
from tela_vendas_do_dia import salvar_planilha_dia
from tela_vendas_do_mes import salvar_planilha_mes

db = BancoDeDados()


class TelaVendas:
    def __init__(self, page):
        self.page = page

        self.vendas = []

        self.soma = 0
        self.troco = 0

        self.unidades_vendidas = ft.TextField(
            label='Unidades Vendidas'
        )

        self.campo_troco = ft.TextField(
            label='Calcular troco'
        )

        self.btn_adicionar_venda = ft.ElevatedButton(
            'Adicionar Produto',
            on_click=self.adicionar_venda
        )

        self.btn_salvar_venda = ft.ElevatedButton(
            'Salvar Venda',
            on_click=self.abrir_alert_cupom
        )

        self.nome_do_produto = ft.TextField(
            label='Nome do Produto'
        )

        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text('id')),
                ft.DataColumn(ft.Text('Nome')),
                ft.DataColumn(ft.Text('Preço Unitário')),
                ft.DataColumn(ft.Text('Unidades Vendidas')),
                ft.DataColumn(ft.Text('Preço Total')),
                ft.DataColumn(ft.Text(''))
            ],
            rows=[]
        )

        self.preco_venda = ft.Text(
            f'Preço Total: R$ {self.soma}',
            size=80
        )

        self.texto_troco = ft.Text(
            f'Troco: R$ {self.troco}',
            size=80
        )

        self.tela = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.nome_do_produto,
                        self.unidades_vendidas,
                        self.campo_troco,
                        self.btn_adicionar_venda,
                        self.btn_salvar_venda
                    ]
                ),
                ft.Row(
                    controls=[self.tabela],
                    alignment='CENTER'
                ),
                ft.Row(
                    controls=[
                        self.preco_venda,
                    ],
                    alignment='CENTER'
                ),
                ft.Row(
                    controls=[
                        self.texto_troco
                    ],
                    alignment='CENTER'
                )
            ]
        )

        self.alert_cupom = ft.AlertDialog(
            modal=True,
            title=ft.Text('Cupom Fiscal'),
            content=ft.Text(
                'Venda realizada.\nDeseja imprimir o cupom fiscal?'),
            actions=[
                ft.TextButton('Sim', on_click=self.imprimir_cupom),
                ft.TextButton('Não', on_click=self.fechar_alert_cupom)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

    def adicionar_venda(self, e):
        produto = db.select_produto(self.nome_do_produto.value)

        id = produto[0]
        nome = produto[1]
        preco_venda = produto[3]
        unidades_vendidas = self.unidades_vendidas.value
        quantidade_estoque = int(
            produto[4]) - int(self.unidades_vendidas.value)
        limite_estoque = int(produto[5])
        self.preco_total = int(unidades_vendidas) * float(preco_venda)

        self.tabela.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(id)),
                    ft.DataCell(ft.Text(nome)),
                    ft.DataCell(ft.Text(preco_venda)),
                    ft.DataCell(ft.Text(unidades_vendidas)),
                    ft.DataCell(ft.Text(self.preco_total)),
                    ft.DataCell(ft.Text(''))
                ]
            )
        )

        self.page.snack_bar = ft.SnackBar(
            ft.Text(f"Venda registrada com sucesso!", color='WHITE'),
            bgcolor='GREEN'
        )
        self.page.snack_bar.open = True

        self.vendas.append(
            [nome, preco_venda, unidades_vendidas, self.preco_total])

        db.cadastrar_venda(id, nome, preco_venda,
                           unidades_vendidas, self.preco_total)

        db.diminuir_estoque(id, quantidade_estoque)

        if quantidade_estoque <= limite_estoque:
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"{nome} está com estoque baixo!", color='WHITE'),
                bgcolor='RED'
            )
            self.page.snack_bar.open = True

        self.mostrar_preco_venda(self.preco_total)
        self.calcular_troco(self.preco_total, self.campo_troco.value)
        
        self.nome_do_produto.value = ""

        salvar_planilha_dia()
        salvar_planilha_mes()

        self.page.update()

    def abrir_alert_cupom(self, e):
        self.page.dialog = self.alert_cupom
        self.alert_cupom.open = True
        self.page.update()

    def fechar_alert_cupom(self, e=False):
        self.alert_cupom.open = False
        self.limpar_vendas()
        self.page.update()

    def imprimir_cupom(self, e):
        self.page.snack_bar = ft.SnackBar(
            ft.Text(f"Imprimindo Nota Fiscal...", color='WHITE'),
            bgcolor='GREEN'
        )
        self.page.snack_bar.open = True
        cupom = CupomFiscal('Loja', self.vendas, 'CNPJ')
        self.fechar_alert_cupom()
        self.limpar_vendas()

    def limpar_vendas(self):
        self.vendas.clear()
        self.tabela.rows.clear()
        self.preco_total = 0
        self.troco = 0
        self.soma = 0
        self.preco_venda.value = f'Preço Total: R$ {self.soma}'
        self.tabela.update()

    def mostrar_preco_venda(self, preco_total):
        self.soma += preco_total
        self.preco_venda.value = f'Preço Total: R$ {self.soma}'

    def calcular_troco(self, preco_total, campo_troco):
        self.troco = float(campo_troco) - preco_total
        self.texto_troco.value = f'Troco: R$ {self.troco}'


