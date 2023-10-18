from banco_de_dados import BancoDeDados
from interface import Interface
import flet as ft

db = BancoDeDados()
interface = Interface()

def main(page: ft.Page):
    page.add(interface.guias)
    page.update()


ft.app(target=main)