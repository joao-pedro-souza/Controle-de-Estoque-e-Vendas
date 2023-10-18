import flet as ft

class App(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.guias = ft.Tabs(
            tabs=[
                ft.Tab(
                    text='Produtos'
                ),
                ft.Tab(
                    text='Vendas'
                )
            ]
        )
    

    def build(self):
        return ft.Container(
            ft.Column(
                controls=[
                    self.guias
                ]
            ),
            alignment=ft.alignment.center
        )
        