import flet as ft
from tela_produtos import TelaProdutos
from tela_registrar_venda import TelaVendas
from tela_vendas_do_dia import VendasDoDia
from tela_estoque_baixo import EstoqueBaixo


class Interface:
    def __init__(self, page):
        self.page = page
        self.produtos = TelaProdutos(page)
        self.vendas = TelaVendas(page)
        self.vendas_do_dia = VendasDoDia(page)
        self.estoque_baixo = EstoqueBaixo(page)

        self.nome_loja = ft.Text(
            'Loja',
            size=40,
            text_align=ft.TextAlign.END
        )

        self.titulo = ft.Row(
            controls=[
                self.nome_loja
            ],
            alignment='CENTER'
        )

        self.guias = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text='Produtos',
                    content=self.produtos.tela
                ),
                ft.Tab(
                    text='Registrar Venda',
                    content=self.vendas.tela
                ),
                ft.Tab(
                    text='Vendas do Dia',
                    content=self.vendas_do_dia.tela
                ),
                ft.Tab(
                    text='Produtos com Estoque Baixo',
                    content=self.estoque_baixo.tela
                )
            ],
            expand=1,
            on_change=self.atualizar_guias
        )

    def atualizar_guias(self, e):
        self.vendas.atualizar_produtos(e)
        self.produtos.atualizar_tabela()
        self.vendas_do_dia.atualizar_vendas()
        self.estoque_baixo.atualizar_estoque_baixo()
        self.page.update()
