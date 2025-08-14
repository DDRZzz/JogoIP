import pygame 
from pygame.locals import *
from sys import exit

pygame.init()
largura = 640
altura = 480
x = 0
y = 0

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo massa')
clock = pygame.time.Clock()

#LOOP PRINCIPAL:
while True:
    tela.fill((255, 255, 255))
    clock.tick(60)
    for event in pygame.event.get():
        if(event.type == QUIT):
            pygame.quit()
            exit()
    if(pygame.key.get_pressed()[K_a]):
        x -= 20
    if(pygame.key.get_pressed()[K_d]):
        x += 20
    if(pygame.key.get_pressed()[K_w]):
        y -= 20
    if(pygame.key.get_pressed()[K_s]):
        y += 20

    pygame.draw.rect(tela, (255, 100, 60), (x, y, 40 , 40))
    pygame.display.update()
