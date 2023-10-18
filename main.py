from banco_de_dados import BancoDeDados
from interface import Interface
import flet as ft

db = BancoDeDados()
interface = Interface()

def main(page: ft.Page):
    page.window_maximized=True
    page.add(interface.guias)
    

ft.app(target=main)