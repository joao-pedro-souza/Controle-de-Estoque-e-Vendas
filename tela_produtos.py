import flet as ft
from banco_de_dados import BancoDeDados

db = BancoDeDados()


class TelaProdutos:
    def __init__(self, page):
        self.page = page

        self.barra_pesquisa = ft.TextField(
            label='Pesquisar Produto',
            suffix_icon='SEARCH',
            on_change=self.filtrar_tabela
        )

        # Campos Cadastrar Produto
        self.nome = ft.TextField(label='Nome')
        self.preco_compra = ft.TextField(label='Preço de Compra')
        self.preco_venda = ft.TextField(label='Preço de Venda')
        self.quantidade_estoque = ft.TextField(label='Quantidade em Estoque')
        self.limite_estoque = ft.TextField(label='Alertar Estoque Baixo')

        # Campos Editar Produto
        self.editar_id = ft.Text()
        self.editar_nome = ft.TextField(label='Nome')
        self.editar_preco_compra = ft.TextField(label='Preço de Compra')
        self.editar_preco_venda = ft.TextField(label='Preço de Venda')
        self.editar_quantidade_estoque = ft.TextField(
            label='Quantidade em Estoque')
        self.editar_limite_estoque = ft.TextField(
            label='Alertar Estoque Baixo')

        # Guarda id do produto a ser deletado
        self.id_produto_deletado = None

        self.campos = ft.Row(
            controls=[
                self.nome,
                self.preco_compra,
                self.preco_venda,
                self.quantidade_estoque,
                self.limite_estoque
            ]
        )

        self.btn_cadastrar = ft.ElevatedButton(
            'Cadastrar',
            on_click=self.clicar_cadastrar
        )

        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text('id')),
                ft.DataColumn(ft.Text('Nome')),
                ft.DataColumn(ft.Text('Preço')),
                ft.DataColumn(ft.Text('Quantidade em Estoque')),
                ft.DataColumn(ft.Text(''))
            ],
            rows=[]
        )

        self.tela = ft.Column(
            controls=[
                self.barra_pesquisa,
                self.campos,
                ft.Row(
                    [self.btn_cadastrar],
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

        self.alert_editar = ft.AlertDialog(
            title=ft.Text('Editar Produto'),
            content=ft.Column(
                [
                    self.editar_nome,
                    self.editar_preco_compra,
                    self.editar_preco_venda,
                    self.editar_quantidade_estoque,
                    self.editar_limite_estoque
                ]
            ),
            actions=[
                ft.TextButton('Salvar', on_click=self.confirmar_edit)
            ]
        )

        self.carregar_produtos()

    def carregar_produtos(self):
        tabela_produtos = db.select_todos_produtos()
        colunas = [coluna[0] for coluna in db.select_colunas()]
        produtos = [dict(zip(colunas, produto)) for produto in tabela_produtos]

        for produto in produtos:
            cor_estoque = 'white'
            limite_estoque_numerico = isinstance(
                produto['limite_estoque'], int)

            if limite_estoque_numerico:
                if produto['quantidade_estoque'] <= produto['limite_estoque']:
                    cor_estoque = 'red'

            self.tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(produto['id'])),
                        ft.DataCell(ft.Text(produto['nome'])),
                        ft.DataCell(ft.Text(produto['preco_venda'])),
                        ft.DataCell(
                            ft.Text(produto['quantidade_estoque'], color=cor_estoque)),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        ft.icons.DELETE,
                                        icon_color='RED',
                                        data=produto,
                                        on_click=self.abrir_delete
                                    ),
                                    ft.IconButton(
                                        ft.icons.EDIT,
                                        data=produto,
                                        on_click=self.abrir_edit
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

    def atualizar_tabela(self):
        self.tabela.rows.clear()
        self.carregar_produtos()
        self.tabela.update()

    def clicar_cadastrar(self, e):
        db.cadastrar_produto(
            self.nome.value,
            self.preco_compra.value,
            self.preco_venda.value,
            self.quantidade_estoque.value,
            self.limite_estoque.value
        )
        self.page.snack_bar = ft.SnackBar(
            ft.Text(f"Produto cadastrado com sucesso!", color='WHITE'),
            bgcolor='GREEN'
        )
        self.page.snack_bar.open = True
        self.page.update()
        self.atualizar_tabela()
        self.limpar_campos()

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
            self.atualizar_tabela()
            del self.id_produto_deletado
            self.fechar_delete()

    def abrir_edit(self, e):
        self.editar_id.value = e.control.data['id']
        self.editar_nome.value = e.control.data['nome']
        self.editar_preco_compra.value = e.control.data['preco_compra']
        self.editar_preco_venda.value = e.control.data['preco_venda']
        self.editar_quantidade_estoque.value = e.control.data['quantidade_estoque']
        self.editar_limite_estoque.value = e.control.data['limite_estoque']

        self.page.dialog = self.alert_editar
        self.alert_editar.open = True
        self.page.update()

    def confirmar_edit(self, e):
        db.editar_produto(
            self.editar_id.value,
            self.editar_nome.value,
            self.editar_preco_compra.value,
            self.editar_preco_venda.value,
            self.editar_quantidade_estoque.value,
            self.editar_limite_estoque.value
        )

        self.alert_editar.open = False
        self.page.update()
        self.atualizar_tabela()

    def filtrar_tabela(self, e):
        pesquisa = self.barra_pesquisa.value.lower()
        tabela_produtos = db.select_todos_produtos()
        colunas = [coluna[0] for coluna in db.select_colunas()]
        produtos = [dict(zip(colunas, produto)) for produto in tabela_produtos]
        produtos_filtrados = [
            produto for produto in produtos if pesquisa in produto['nome'].lower()]

        self.tabela.rows.clear()

        for produto in produtos_filtrados:
            self.tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(produto['id'])),
                        ft.DataCell(ft.Text(produto['nome'])),
                        ft.DataCell(ft.Text(produto['preco_venda'])),
                        ft.DataCell(ft.Text(produto['quantidade_estoque'])),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        ft.icons.DELETE,
                                        icon_color='RED',
                                        data=produto,
                                        on_click=self.abrir_delete
                                    ),
                                    ft.IconButton(
                                        ft.icons.EDIT,
                                        data=produto,
                                        on_click=self.abrir_edit
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

        self.tabela.update()

    def limpar_campos(self):
        self.nome.value = ""
        self.nome.update()
        self.preco_compra.value = ""
        self.preco_compra.update()
        self.preco_venda.value = ""
        self.preco_venda.update()
        self.quantidade_estoque.value = ""
        self.quantidade_estoque.update()
        self.limite_estoque.value = ""
        self.limite_estoque.update()
