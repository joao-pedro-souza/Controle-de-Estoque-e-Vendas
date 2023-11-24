from reportlab.pdfgen.canvas import Canvas
from datetime import datetime
import os
import win32print
import win32api


class CupomFiscal():
    def __init__(self, nome_loja=str, produtos=list):
        self.criar_pasta()
        self.nome_loja = nome_loja
        self.produtos = produtos
        self.data = datetime.now().strftime("%d/%m/%Y")
        self.hora_compra = datetime.now().strftime("%H:%M:%S")
        self.total_compra = 0

        self.largura_pagina = 80 * 2.83464567
        self.altura_pagina = 80 * 2.83464567
        self.margem = 2.5 * 2.83464567
        self.canvas = Canvas("pdf/cupom_fiscal.pdf", pagesize=(
            self.largura_pagina, self.altura_pagina))
        self.y = self.canvas._pagesize[1] - self.margem

        self.construir_pagina()
        self.imprimir_cupom_fiscal()

    def criar_pasta(self):
        if not os.path.exists('pdf'):
            os.makedirs('pdf')

    def construir_pagina(self):
        self.adicionar_cabecalho()
        self.adicionar_colunas()
        self.adicionar_produtos()
        self.adicionar_total_compra()
        self.canvas.save()

    def adicionar_cabecalho(self):
        self.canvas.setFont('Helvetica-Bold', 12)
        self.canvas.drawString(self.centralizar_texto(
            self.nome_loja, 12), self.calcular_y(12), self.nome_loja.upper())
        self.canvas.line(self.alinhar_esquerda(), y := self.calcular_y(
            0), (self.largura_pagina - self.alinhar_esquerda()), y)
        self.canvas.setFont('Helvetica', 12)
        self.pular_espaco(10)
        self.canvas.drawString(self.alinhar_esquerda(),
                               self.calcular_y(14), f'DATA: {self.data}')
        self.canvas.drawString(self.alinhar_esquerda(
        ), self.calcular_y(14), f'HORA: {self.hora_compra}')
        self.pular_espaco(10)

    def centralizar_texto(self, texto, fonte):
        largura_texto = len(texto) * fonte
        x = (self.largura_pagina - largura_texto) / 2
        return x

    def alinhar_esquerda(self):
        x = self.largura_pagina / 15
        return x

    def calcular_y(self, fonte):
        self.y -= fonte + 5
        return self.y

    def pular_espaco(self, espaco):
        self.y -= espaco
        return self.y

    def adicionar_colunas(self):
        self.canvas.setFont('Helvetica', 7)
        self.canvas.drawString(self.alinhar_esquerda(),
                               y_col := self.calcular_y(7), "Produto")
        self.canvas.drawString(self.largura_pagina / 1.65, y_col, "Preço")
        self.canvas.drawString(self.largura_pagina / 1.35, y_col, "Unid.")
        self.canvas.drawString(self.largura_pagina / 1.20, y_col, "Total")
        self.canvas.line(self.alinhar_esquerda(), y := self.calcular_y(
            0), (self.largura_pagina - self.alinhar_esquerda()), y)
        self.pular_espaco(2.5)

    def adicionar_produtos(self):
        for produto in self.produtos:
            if self.y < self.margem * 2:
                self.quebrar_pagina()
                self.adicionar_colunas()
            self.canvas.drawString(self.alinhar_esquerda(
            ), y_col := self.calcular_y(7), f'{produto[0]}')
            self.canvas.drawString(
                self.largura_pagina / 1.65, y_col, f'R${produto[1]}')
            self.canvas.drawString(
                self.largura_pagina / 1.30, y_col, f'{produto[2]}')
            self.canvas.drawString(
                self.largura_pagina / 1.20, y_col, f'R${produto[3]}')
            self.total_compra += produto[3]
        self.pular_espaco(10)

    def quebrar_pagina(self):
        self.canvas.showPage()
        self.canvas.setPageSize((self.largura_pagina, self.altura_pagina))
        self.y = self.canvas._pagesize[1] - self.margem

    def adicionar_total_compra(self):
        if self.y < self.margem * 4:
            self.quebrar_pagina()
        self.canvas.setFont('Helvetica-Bold', 12)
        self.canvas.drawString(self.alinhar_esquerda(), self.calcular_y(
            12), f'TOTAL: R${self.total_compra}')

    def imprimir_cupom_fiscal(self):
        arquivo = 'cupom_fiscal.pdf'
        caminho = os.getcwd()
        print(caminho)
        win32api.ShellExecute(0, "print", arquivo, None, caminho+'\pdf', 0)
