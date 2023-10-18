from banco_de_dados import BancoDeDados
from interface import Interface
from tela_produtos import TelaProdutos
import flet as ft

db = BancoDeDados()

def main(page: ft.Page):
    tela_produtos = TelaProdutos(page)
    interface = Interface(page)
    page.window_maximized=True
    page.add(interface.guias)
    

ft.app(target=main)