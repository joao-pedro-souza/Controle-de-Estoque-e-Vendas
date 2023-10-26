from banco_de_dados import BancoDeDados
from interface import Interface
import flet as ft

db = BancoDeDados()


def main(page: ft.Page):
    interface = Interface(page)
    page.title = 'Controle de Estoque'
    page.scroll = 'auto'
    page.window_maximized = True
    page.add(interface.guias)


ft.app(target=main)
