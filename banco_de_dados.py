import sqlite3
import os
from datetime import datetime


class BancoDeDados:
    def __init__(self):
        self.criar_pasta()
        self.criar_conexao()
        self.criar_tabela_produtos()
        self.criar_tabela_vendas()
        self.data = datetime.now().strftime("%d/%m/%Y")
        self.mes = datetime.now().month
        self.ano = datetime.now().year

    def criar_pasta(self):
        if not os.path.exists('db'):
            os.makedirs('db')

    def criar_conexao(self):
        self.conexao = sqlite3.connect(
            'db/estoque.db', check_same_thread=False)
        self.cursor = self.conexao.cursor()

    def criar_tabela_produtos(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            preco_compra REAL,
            preco_venda REAL,
            quantidade_estoque INTEGER,
            limite_estoque INTEGER
            )"""
        )
        self.conexao.commit()

    def criar_tabela_vendas(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produto,
            nome TEXT,
            preco_unitario REAL,
            unidades_vendidas INTEGER,
            preco_total REAL,
            data TEXT,
            hora TEXT
            )"""
        )
        self.conexao.commit()

    def select_todos_produtos(self):
        self.cursor.execute('SELECT * FROM produtos ORDER BY nome')
        return self.cursor.fetchall()

    def select_colunas(self):
        return self.cursor.description

    def cadastrar_produto(self, nome, preco_compra, preco_venda, quantidade_estoque, limite_estoque):
        preco_compra = preco_compra.replace(',', '.')
        preco_venda = preco_venda.replace(',', '.')

        self.cursor.execute('INSERT INTO produtos (nome, preco_compra, preco_venda, quantidade_estoque, limite_estoque) VALUES (?, ?, ?, ?, ?)',
                            [nome, preco_compra, preco_venda,
                                quantidade_estoque, limite_estoque]
                            )
        self.conexao.commit()

    def deletar_produto(self, id):
        self.cursor.execute('DELETE FROM produtos WHERE id = (?)', [id])
        self.conexao.commit()

    def editar_produto(self, id, nome, preco_compra, preco_venda, quantidade_estoque, limite_estoque):
        self.cursor.execute("""UPDATE produtos SET
                    nome = (?),
                    preco_compra = (?),
                    preco_venda = (?),
                    quantidade_estoque = (?),
                    limite_estoque = (?)
                    WHERE id = (?)
                    """, [nome, preco_compra, preco_venda, quantidade_estoque, limite_estoque, id])
        self.conexao.commit()

    def select_produto(self, nome):
        self.cursor.execute('SELECT * FROM produtos WHERE nome = (?)', [nome])
        return self.cursor.fetchone()

    def cadastrar_venda(self, id, nome, preco_venda, unidades_vendidas, preco_total):
        self.hora = datetime.now().strftime("%H:%M:%S")
        self.cursor.execute("""INSERT INTO vendas (
                            id_produto,
                            nome,
                            preco_unitario,
                            unidades_vendidas,
                            preco_total,
                            data,
                            hora) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)""",
                            [id, nome, preco_venda, unidades_vendidas, preco_total, self.data, self.hora])
        self.conexao.commit()
        

    def select_vendas_dia(self):
        self.cursor.execute(
            'SELECT * FROM vendas WHERE data = (?)', [self.data])
        return self.cursor.fetchall()

    def select_vendas_mes(self):
        self.cursor.execute(
            'SELECT * FROM vendas WHERE data LIKE (?)', [f'%/{self.mes}/{self.ano}'])
        return self.cursor.fetchall()

    def select_estoque_baixo(self):
        self.cursor.execute(
            'SELECT * FROM produtos WHERE quantidade_estoque <= limite_estoque')
        return self.cursor.fetchall()

    def diminuir_estoque(self, id, quantidade_estoque):
        self.cursor.execute('UPDATE produtos SET quantidade_estoque = (?) WHERE id = (?)', [
                            quantidade_estoque, id])
        self.conexao.commit()
