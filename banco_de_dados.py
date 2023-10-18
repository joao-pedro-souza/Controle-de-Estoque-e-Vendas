import sqlite3
import os

class BancoDeDados:
    def __init__(self):
        self.criar_conexao()
        self.criar_tabela_produtos()
        self.criar_tabela_vendas()
    

    def criar_pasta(self):
        if not os.path.exists('db'):
            os.makedirs('db')


    def criar_conexao(self):
        self.conexao = sqlite3.connect('db/estoque.db', check_same_thread=False)
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
            valor_compra REAL,
            valor_unitario REAL,
            unidades_vendidas INTEGER,
            valor_total REAL,
            data TEXT
            )"""
        )
        self.conexao.commit()
