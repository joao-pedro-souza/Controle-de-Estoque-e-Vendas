import flet as ft
from banco_de_dados import BancoDeDados

db = BancoDeDados()

class TelaProdutos:
    def __init__(self, page):
        self.page = page

        self.barra_pesquisa = ft.TextField(
            label='Pesquisar Produto',
            suffix_icon='SEARCH'
        )
        
        # Campos Cadastrar Produto
        self.nome = ft.TextField(label='Nome')
        self.preco_compra = ft.TextField(label='Preço de Compra')
        self.preco_venda = ft.TextField(label='Preço de Venda')
        self.quantidade_estoque = ft.TextField(label='Quantidade em Estoque')
        self.limite_estoque = ft.TextField(label='Alertar Estoque Baixo')

        # Campo Deletar Produto
        self.id_produto_deletado = ''
        
        self.campos = ft.Row(
            controls=[
                self.nome,
                self.preco_compra,
                self.preco_venda,
                self.quantidade_estoque,
                self.limite_estoque
            ]
        )

        self.botao_cadastrar = ft.ElevatedButton(
            'Cadastrar',
            on_click=self.clicar_cadastrar
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

        self.alert_deletar = ft.AlertDialog(
            modal=True,
            title=ft.Text('Apagar Produto'),
            content=ft.Text('Deseja apagar o produto?'),
            actions=[
                ft.TextButton('Sim', on_click=self.confirmar_deletar),
                ft.TextButton('Não', on_click=self.fechar_delete)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.carregar_dados()


    def carregar_dados(self):
        dados = db.select_produtos()
        colunas = [coluna[0] for coluna in db.select_colunas()]
        linhas = [dict(zip(colunas, linha)) for linha in dados]

        for linha in linhas:
            cor_estoque = 'white'
            limite_estoque_numerico = isinstance(linha['limite_estoque'], int)

            if limite_estoque_numerico:
                if linha['quantidade_estoque'] <= linha['limite_estoque']:
                    cor_estoque = 'red'
            
            self.tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(linha['id'])),
                        ft.DataCell(ft.Text(linha['nome'])),
                        ft.DataCell(ft.Text(linha['preco_compra'])),
                        ft.DataCell(ft.Text(linha['quantidade_estoque'], color=cor_estoque)),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        ft.icons.DELETE,
                                        icon_color='RED',
                                        data=linha,
                                        on_click=self.abrir_delete
                                    ),
                                    ft.IconButton(
                                        ft.icons.EDIT,
                                        data=linha
                                    )
                                ]
                            )
                        )
                    ]
                )
            )


    def clicar_cadastrar(self, e):
        dados_preenchidos = self.nome.value and self.preco_compra.value and self.preco_venda.value and self.quantidade_estoque.value and self.limite_estoque.value

        if dados_preenchidos:
            db.cadastrar_produto(
                self.nome.value, 
                self.preco_compra.value, 
                self.preco_venda.value, 
                self.quantidade_estoque.value, 
                self.limite_estoque.value
            )
            self.tabela.rows.clear()
            self.carregar_dados()
            self.tabela.update()

    def abrir_delete(self, e):
        self.id_produto_deletado = str(e.control.data['id'])
        self.page.dialog = self.alert_deletar
        self.alert_deletar.open = True    
        self.page.update()

    def fechar_delete(self, e=False):
        self.alert_deletar.open = False
        self.page.update()
    
    def confirmar_deletar(self, e):
        if self.id_produto_deletado:
            db.deletar_produto(self.id_produto_deletado)
            self.tabela.rows.clear()
            self.carregar_dados()
            self.tabela.update()
            del self.id_produto_deletado
            self.fechar_delete()

