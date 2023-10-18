import flet as ft

class TelaProdutos:
    def __init__(self):
        self.barra_pesquisa = ft.TextField(
            label='Pesquisar Produto',
            suffix_icon='SEARCH'
        )
        
        self.nome = ft.TextField(label='Nome')
        self.preco = ft.TextField(label='Preço')
        self.quantidade = ft.TextField(label='Quantidade')
        self.alerta = ft.TextField(label='Alerta de Estoque Baixo')
        
        self.campos = ft.Row(
            controls=[
                self.nome,
                self.preco,
                self.quantidade,
                self.alerta
            ]
        )

        self.botao_cadastrar = ft.ElevatedButton(
            'Cadastrar'
        )

        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text('id')),
                ft.DataColumn(ft.Text('nome')),
                ft.DataColumn(ft.Text('preço')),
                ft.DataColumn(ft.Text('quantidade')),
                ft.DataColumn(ft.Text(''))
            ],
            rows=[]
        )

        self.tela = ft.Column(
            controls=[
                self.barra_pesquisa,
                self.campos,
                ft.Row(
                    [self.botao_cadastrar],
                    alignment=ft.MainAxisAlignment.END
                ),
                ft.Row(
                    [self.tabela],
                    alignment='CENTER'
                )
            ],
        )
