import flet as ft
from tela_produtos import TelaProdutos

tl = TelaProdutos()

class Interface:
    def __init__(self):
        self.guias = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text='Produtos',
                    content=tl.tela
                ),
                ft.Tab(
                    text='Vendas'
                )
            ],
            expand=1
        )
