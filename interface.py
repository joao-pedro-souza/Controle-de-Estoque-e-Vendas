import flet as ft
from tela_produtos import TelaProdutos
from tela_vendas import TelaVendas


class Interface:
    def __init__(self, page):
        self.page = page
        tp = TelaProdutos(page)
        tv = TelaVendas(page)

        self.guias = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text='Produtos',
                    content=tp.tela
                ),
                ft.Tab(
                    text='Vendas',
                    content=tv.tela
                ),
                ft.Tab(
                    text='Vendas do Dia'
                )
            ],
            expand=1,
            on_change=tv.atualizar_produtos
        )
