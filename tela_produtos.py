import flet as ft

class TelaProdutos:
    def __init__(self):
        self.barra_pesquisa = ft.TextField(
            label='Pesquisar Produto',
            suffix_icon='SEARCH'
        )