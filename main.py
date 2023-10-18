from banco_de_dados import BancoDeDados
from interface import App
import flet as ft

db = BancoDeDados()

def main(page: ft.Page):
    page.add(App())


ft.app(target=main)