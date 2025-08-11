import pygame
from pygame.locals import *
from sys import exit

pygame.init()

largura = 680
altura = 540
cor_menu = (0,0,0)
azul = (0, 0, 200)

relogio = pygame.time.Clock()
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Tela de menu")

#Classe para mudar de tela:
class Cena:
    def __init__(self, fase):
        self.fase_atual = fase
    
    def pegar_fase(self):
        return self.fase_atual
    
    def muda_fase(self, fase):
        self.fase_atual = fase

#Tela de menu:
class Menu:
    def __init__(self, display, objeto_cena): 
        self.tela = display
        self.cena = objeto_cena
        self.fonte = pygame.font.SysFont('Arial', 30)

    def botoes(self):
        self.play = pygame.draw.rect(self.tela, (0,0,0), (340 - 50, 300, 100, 50))
        self.sair = pygame.draw.rect(self.tela, (0,0,0), (340 - 50, 390, 100, 50))
        texto_jogar = self.fonte.render('Jogar', True, (255, 255, 255))
        pos_texto_jogar = texto_jogar.get_rect(center=self.play.center)
        self.tela.blit(texto_jogar, pos_texto_jogar)
        texto_sair = self.fonte.render('Sair', True, (255, 255, 255))
        pos_texto_sair = texto_sair.get_rect(center=self.sair.center)
        self.tela.blit(texto_sair, pos_texto_sair)


    def click(self):
        posicao_m = pygame.mouse.get_pos()
        botao_m = pygame.mouse.get_pressed()

        if(self.play.collidepoint(posicao_m)):
            self.play = pygame.draw.rect(self.tela, (90,90,90), (340 - 50, 300, 100, 50))
            texto_jogar = self.fonte.render('Jogar', True, (255, 255, 255))
            pos_texto_jogar = texto_jogar.get_rect(center=self.play.center)
            self.tela.blit(texto_jogar, pos_texto_jogar)
            if(botao_m[0] == True):
                cena.muda_fase('Tela1')
        if(self.sair.collidepoint(posicao_m)):
            self.sair = pygame.draw.rect(self.tela, (90,90,90), (340 - 50, 390, 100, 50))
            texto_sair = self.fonte.render('Sair', True, (255, 255, 255))
            pos_texto_sair = texto_sair.get_rect(center=self.sair.center)
            self.tela.blit(texto_sair, pos_texto_sair)
            if(botao_m[0] == True):
                pygame.quit()
                exit()

    def run(self):
        self.tela.fill((cor_menu))
        self.botoes()
        self.click()

#Construtor para outras telas:
class Construtor: 
    def __init__(self, display, cor, objeto_cena):
        self.tela = display
        self.cor = cor
        self.cena = objeto_cena
    
    def run(self):
        self.tela.fill((self.cor))

cena = Cena('Menu')
menu = Menu(tela, cena)
tela1 = Construtor(tela, (azul), cena)

#Dicionário que armazena as fases do jogo:
fases = {'Menu': menu, 'Tela1': tela1}

while True:
    #60 FPS
    relogio.tick(60)
    #Tela preta
    tela.fill((0,0,0))
    for evento in pygame.event.get():
        if(evento.type == QUIT):
            pygame.quit()
            exit()

    fases[cena.pegar_fase()].run()
    pygame.display.update()