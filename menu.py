import pygame
from pygame.locals import *
from sys import exit

pygame.init()

largura = 680
altura = 540
cor_menu = (0, 0, 0)
preto = (0, 0, 0)

relogio = pygame.time.Clock()
tela = pygame.display.set_mode((largura, altura))


class Botao:
    def __init__(self, x, y, largura, altura, texto, fonte, cor_fundo, cor_hover, cor_texto):
        self.retangulo = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.fonte = fonte
        self.cor_fundo = cor_fundo
        self.cor_hover = cor_hover
        self.cor_texto = cor_texto
    
    def desenhar(self, tela):
        cor_atual = self.cor_fundo
        if self.retangulo.collidepoint(pygame.mouse.get_pos()):
            cor_atual = self.cor_hover
            
        pygame.draw.rect(tela, cor_atual, self.retangulo)
        texto_renderizado = self.fonte.render(self.texto, True, self.cor_texto)
        pos_texto = texto_renderizado.get_rect(center=self.retangulo.center)
        tela.blit(texto_renderizado, pos_texto)

    def clicou(self):
        posicao_m = pygame.mouse.get_pos()
        botao_m = pygame.mouse.get_pressed()
        return self.retangulo.collidepoint(posicao_m) and botao_m[0]

class Cena:
    def __init__(self, fase):
        self.fase_atual = fase
    
    def pegar_fase(self):
        return self.fase_atual
    
    def muda_fase(self, fase):
        self.fase_atual = fase

class Menu:
    def __init__(self, display, objeto_cena): 
        self.tela = display
        self.cena = objeto_cena
        self.fonte = pygame.font.Font('PressStart2P.ttf', 16) 
        self.fonte_titulo = pygame.font.Font('PressStart2P.ttf', 22)
        
        largura_botao = 150
        altura_botao = 50
        x_centralizado = (largura / 2) - (largura_botao / 2)
        
        self.botao_jogar = Botao(x_centralizado, 250, largura_botao, altura_botao, 'Jogar', self.fonte, (0, 0, 0), (90, 90, 90), (255, 255, 255))
        self.botao_creditos = Botao(x_centralizado, 320, largura_botao, altura_botao, 'Creditos', self.fonte, (0, 0, 0), (90, 90, 90), (255, 255, 255))
        self.botao_sair = Botao(x_centralizado, 390, largura_botao, altura_botao, 'Sair', self.fonte, (0, 0, 0), (90, 90, 90), (255, 255, 255))
    
    def desenhar_botoes(self):
        self.botao_jogar.desenhar(self.tela)
        self.botao_creditos.desenhar(self.tela)
        self.botao_sair.desenhar(self.tela)
    
    def click(self):
        if self.botao_jogar.clicou():
            self.cena.muda_fase('Tela1')
        
        if self.botao_creditos.clicou():
            self.cena.muda_fase('Creditos')

        if self.botao_sair.clicou():
            pygame.quit()
            exit()
    
    def desenhar_titulo(self):
        nome_jogo = "Jogo massa"
        texto_titulo = f"Bem-vindo ao {nome_jogo}"
        titulo_renderizado = self.fonte_titulo.render(texto_titulo, True, (255, 255, 255))
        pos_titulo = titulo_renderizado.get_rect(center=(largura / 2, 130))
        self.tela.blit(titulo_renderizado, pos_titulo)

    def run(self):
        pygame.display.set_caption("Tela de menu")
        self.tela.fill((cor_menu))
        self.desenhar_titulo()
        self.desenhar_botoes()
        self.click()

class Construtor: 
    def __init__(self, display, cor, objeto_cena):
        self.tela = display
        self.cor = cor
        self.cena = objeto_cena
        self.fonte_principal = pygame.font.Font('PressStart2P.ttf', 16)
    
    def run(self):
        self.tela.fill((self.cor))
        mensagem = "Jogo massa ficará aqui em breve..."
        texto_renderizado = self.fonte_principal.render(mensagem, True, (255, 255, 255))
        pos_texto = texto_renderizado.get_rect(center=(largura / 2, altura / 2))
        self.tela.blit(texto_renderizado, pos_texto)

class Creditos:
    def __init__(self, display, objeto_cena):
        self.tela = display
        self.cena = objeto_cena
        self.cor = (0, 0, 0)
        self.fonte = pygame.font.Font('PressStart2P.ttf', 14)
        self.fonte_titulo = pygame.font.Font('PressStart2P.ttf', 20)
        self.botao_voltar = Botao(largura - 160, altura - 60, 150, 50, 'Voltar', self.fonte, (0, 0, 0), (90, 90, 90), (255, 255, 255))

    def desenhar_creditos(self):
        titulo = self.fonte_titulo.render("CREDITOS", True, (255, 255, 255))
        titulo_pos = titulo.get_rect(center=(largura / 2, 100))
        self.tela.blit(titulo, titulo_pos)

        creditos_texto = [
            "Desenvolvimento: Breno, Goat, Zuza,",
            "Manel, Cinhará e É rosa João?",
            "Arte: É rosa joão?, Cinhará",
            "Música: Ninguém",
            "Agradecimentos: Ricardo e Sergio pocas"
        ]
        
        y_pos = 180
        for linha in creditos_texto:
            texto_renderizado = self.fonte.render(linha, True, (255, 255, 255))
            pos = texto_renderizado.get_rect(center=(largura / 2, y_pos))
            self.tela.blit(texto_renderizado, pos)
            y_pos += 40

    def run(self):
        self.tela.fill((self.cor))
        self.desenhar_creditos()
        self.botao_voltar.desenhar(self.tela)
        
        if self.botao_voltar.clicou():
            self.cena.muda_fase('Menu')


cena = Cena('Menu')
menu = Menu(tela, cena)
tela1 = Construtor(tela, (preto), cena)
creditos = Creditos(tela, cena)

fases = {'Menu': menu, 'Tela1': tela1, 'Creditos': creditos}

while True:
    relogio.tick(60)
    tela.fill((0, 0, 0))
    
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()

    fases[cena.pegar_fase()].run()
    pygame.display.update()
