import pygame
import sys
import math

# --- CONFIGURAÇÕES GERAIS DO JOGO ---
NOME_JOGO = "Aventura de Plataforma"
CRIADOR_1 = "João Luiz da Silva Santos Araujo - jlssa"
CRIADOR_2 = "Leoncio Alves Ferreira Neto - lafn"
CRIADOR_3 = "Breno Jose Ramos da Silva- bjrs"
CRIADOR_4 = "Jonas Manoel Barbosa da Lima - jmbl2"
CRIADOR_5 = "Daniel Rodrigues Zuza - drz"
CRIADOR_6 = "Caio de Oliveira Daltro Gouté - codg"


# --- Constantes ---
LARGURA_TELA = 1200
ALTURA_TELA = 800
LARGURA_MUNDO = 10000
FPS = 60

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
VERMELHO_ESCURO = (139, 0, 0)
CINZA = (128, 128, 128)
LARANJA = (255, 165, 0)
ROXO = (128, 0, 128)
MARROM = (139, 69, 19)
AMARELO = (255, 255, 0)
ROSA = (255, 105, 180)
CIANO = (0, 255, 255)
AZUL_ESCURO = (0, 0, 139)


# Propriedades do Jogador
JOGADOR_ACELERACAO = 0.7
JOGADOR_ATRITO = -0.12
JOGADOR_GRAVIDADE = 0.8
JOGADOR_FORCA_PULO = -20
JOGADOR_VIDA_MAXIMA = 5
JOGADOR_DURACAO_INVENCIBILIDADE = 1000 # em milissegundos
JOGADOR_VIDAS_INICIAIS = 3

# --- Listas de Configuração do Nível ---

# Plataformas: (x, y, largura, altura)
LISTA_PLATAFORMAS = [
    (300, ALTURA_TELA - 200, 300, 25),
    (800, ALTURA_TELA - 350, 250, 25),
    (1150, ALTURA_TELA - 200, 300, 25),
    (1563, ALTURA_TELA - 500, 188, 25),
    (2000, ALTURA_TELA - 365, 188, 25),
    (2313, ALTURA_TELA - 250, 188, 25),
    (2358,313,188,25), (2779,430,100,25),
    (2679,580,200,25),(2979,580,100,25),(3107,394,200,25),(3439,394,450,25),(3968,260,200,25)
]

# Paredes: (x, y, largura, altura)
LISTA_PAREDES = [(2879,350,100,350),(4247,250,100,450)]

# Moedas: (x, y)
LISTA_MOEDAS = [
    (450, ALTURA_TELA - 250),
    (700, ALTURA_TELA - 300),
    (850, ALTURA_TELA - 400),
    (925, ALTURA_TELA - 400),
    (1700, ALTURA_TELA - 300),
    (1625, ALTURA_TELA - 125),
    (2080, ALTURA_TELA - 200),
    (2400, ALTURA_TELA - 150),(2803,523),(2818,373),(3364,213),(3480,260),(3569,260),(3680,260),(4038,197)
    
]

# Itens Especiais
# Corações: (x, y, 'id_unico_do_coracao')
LISTA_CORACOES = [(2463,242,'cora')]
# Botas: (x, y)
LISTA_BOTAS = []


# Inimigos Patrulha (Vermelho): (x, y, largura, altura, velocidade, alcance_patrulha, direcao_inicial)
LISTA_INIMIGOS_PATRULHA = [
    (200, ALTURA_TELA - 100 - 40, 40, 40, 1, 50, 'direita'), # Inimigo atrás do jogador
    (400, ALTURA_TELA - 100 - 40, 40, 40, 2, 250, 'direita'),
    (3053,660,40,40,2,200,'direita'),(3273,660,40,40,2,200,'direita'),(3493,660,40,40,2,200,'direita'),(3713,660,40,40,2,200,'direita')
]

# Inimigos Saltadores (Roxo): (x, y, largura, altura, altura_pulo)
LISTA_INIMIGOS_SALTADORES = [
    (1563, ALTURA_TELA - 100 - 40, 40, 40, 125),
    (1688, ALTURA_TELA - 100 - 40, 40, 40, 188),
    (2388,269,40,40,188),(3620,359,40,40,188),(3760,359,40,40,188)
]

# Inimigos Perseguidores (Marrom): (x, y, largura, altura, velocidade)
LISTA_INIMIGOS_PERSEGUIDORES = [(1992,650,40,40,1)]


# --- Classes ---

class Camera:
    def __init__(self, largura, altura):
        self.camera = pygame.Rect(0, 0, largura, altura)
        self.largura = largura
        self.altura = altura

    def aplicar(self, entidade):
        return entidade.rect.move(self.camera.topleft)

    def update(self, alvo):
        x = -alvo.rect.centerx + int(LARGURA_TELA / 2)
        x = min(0, x)
        x = max(-(self.largura - LARGURA_TELA), x)
        self.camera = pygame.Rect(x, 0, self.largura, self.altura)

class Jogador(pygame.sprite.Sprite):
    def __init__(self, jogo):
        super().__init__()
        self.jogo = jogo
        self.image = pygame.Surface((50, 50))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        # Posição inicial ajustada para o começo do nível
        self.pos = pygame.math.Vector2(150, ALTURA_TELA - 100)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.rect.midbottom = self.pos
        
        self.vida = JOGADOR_VIDA_MAXIMA
        self.momento_ultimo_dano = 0
        self.tem_pulo_duplo = False
        self.pulos_feitos = 0

    def pular(self):
        if self.jogo.modo_debug:
            return
        # Pulo normal
        if self.pulos_feitos == 0:
            self.rect.y += 1
            colisoes = pygame.sprite.spritecollide(self, self.jogo.plataformas, False)
            self.rect.y -= 1
            if colisoes:
                self.vel.y = JOGADOR_FORCA_PULO
                self.pulos_feitos = 1
        # Pulo duplo
        elif self.pulos_feitos == 1 and self.tem_pulo_duplo:
            self.vel.y = JOGADOR_FORCA_PULO * 0.8 # Pulo duplo um pouco mais fraco
            self.pulos_feitos = 2


    def sofrer_dano(self, quantidade):
        if self.jogo.modo_debug:
            return # Invencível em modo debug
        agora = pygame.time.get_ticks()
        if agora - self.momento_ultimo_dano > JOGADOR_DURACAO_INVENCIBILIDADE:
            self.vida -= quantidade
            self.momento_ultimo_dano = agora
            if self.vida < 0:
                self.vida = 0

    def update(self):
        if not self.jogo.modo_debug:
            # Física normal
            self.acc = pygame.math.Vector2(0, JOGADOR_GRAVIDADE)
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                self.acc.x = -JOGADOR_ACELERACAO
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                self.acc.x = JOGADOR_ACELERACAO
            self.acc.x += self.vel.x * JOGADOR_ATRITO
            self.vel += self.acc
            if self.vel.y > 15:
                self.vel.y = 15
        else:
            # Modo Debug (voo)
            self.vel = pygame.math.Vector2(0, 0)
            velocidade_debug = 7
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                self.vel.x = -velocidade_debug
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                self.vel.x = velocidade_debug
            if teclas[pygame.K_UP] or teclas[pygame.K_w]:
                self.vel.y = -velocidade_debug
            if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
                self.vel.y = velocidade_debug

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, cor):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill(cor)
        self.rect = self.image.get_rect(topleft=(x, y))

class Parede(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill(AZUL_ESCURO)
        self.rect = self.image.get_rect(topleft=(x, y))

# --- Classes de Itens ---

class Moeda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(AMARELO)
        self.rect = self.image.get_rect(topleft=(x, y))

class Coracao(pygame.sprite.Sprite):
    def __init__(self, x, y, id_item):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        pygame.draw.circle(self.image, ROSA, (15, 15), 15)
        self.image.set_colorkey(PRETO) # Torna o fundo do Surface transparente
        self.rect = self.image.get_rect(topleft=(x, y))
        self.id_item = id_item

class Botas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 25))
        self.image.fill(CIANO)
        self.rect = self.image.get_rect(topleft=(x, y))

# --- Classes de Inimigos ---

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, jogo, x, y, largura, altura):
        super().__init__()
        self.jogo = jogo
        self.image = pygame.Surface((largura, altura))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(x, y)

class InimigoPatrulha(Inimigo):
    def __init__(self, jogo, x, y, largura, altura, velocidade, alcance_patrulha, direcao_inicial):
        super().__init__(jogo, x, y, largura, altura)
        self.image.fill(VERMELHO)
        self.velocidade = velocidade
        self.alcance_patrulha = alcance_patrulha
        
        if direcao_inicial == 'direita':
            self.direcao = 1
            self.x_inicial = x
            self.x_final = x + alcance_patrulha
        else: # 'esquerda'
            self.direcao = -1
            self.x_inicial = x - alcance_patrulha
            self.x_final = x

    def update(self):
        self.pos.x += self.velocidade * self.direcao
        self.rect.x = self.pos.x
        
        if self.pos.x >= self.x_final or self.pos.x <= self.x_inicial:
            self.direcao *= -1
            
        colisoes = pygame.sprite.spritecollide(self, self.jogo.plataformas, False)
        for colisao in colisoes:
            if self.direcao > 0:
                self.rect.right = colisao.rect.left
                self.pos.x = self.rect.x
                self.direcao = -1
                self.x_final = self.pos.x
                self.x_inicial = self.pos.x - self.alcance_patrulha
            elif self.direcao < 0:
                self.rect.left = colisao.rect.right
                self.pos.x = self.rect.x
                self.direcao = 1
                self.x_inicial = self.pos.x
                self.x_final = self.pos.x + self.alcance_patrulha
            break

class InimigoSaltador(Inimigo):
    def __init__(self, jogo, x, y, largura, altura, altura_pulo):
        super().__init__(jogo, x, y, largura, altura)
        self.image.fill(ROXO)
        self.y_inicial = y
        self.vel_y = 0
        self.estado = 'esperando'
        self.ultima_atualizacao = pygame.time.get_ticks()
        self.tempo_espera = 500
        frames_ate_pico = (1500 / 1000) * FPS / 2
        self.gravidade = (2 * altura_pulo) / (frames_ate_pico ** 2)
        self.forca_pulo = -self.gravidade * frames_ate_pico

    def update(self):
        agora = pygame.time.get_ticks()
        if self.estado == 'esperando':
            if agora - self.ultima_atualizacao > self.tempo_espera:
                self.estado = 'pulando'
                self.vel_y = self.forca_pulo
                self.ultima_atualizacao = agora
        elif self.estado == 'pulando':
            self.vel_y += self.gravidade
            self.pos.y += self.vel_y
            self.rect.y = self.pos.y
            colisoes = pygame.sprite.spritecollide(self, self.jogo.plataformas, False)
            for colisao in colisoes:
                if self.vel_y > 0:
                    self.rect.bottom = colisao.rect.top
                    self.pos.y = self.rect.y
                    self.vel_y = 0
                    self.estado = 'esperando'
                    self.ultima_atualizacao = agora # CORREÇÃO: Reseta o timer ao aterrissar
                elif self.vel_y < 0:
                    self.rect.top = colisao.rect.bottom
                    self.pos.y = self.rect.y
                    self.vel_y = 0
            if self.pos.y >= self.y_inicial and self.vel_y > 0:
                self.pos.y = self.y_inicial
                self.vel_y = 0
                self.estado = 'esperando'
                self.ultima_atualizacao = agora # CORREÇÃO: Reseta o timer ao aterrissar
        self.rect.y = self.pos.y

class InimigoPerseguidor(Inimigo):
    def __init__(self, jogo, x, y, largura, altura, velocidade):
        super().__init__(jogo, x, y, largura, altura)
        self.image.fill(MARROM)
        self.velocidade_original = velocidade
        self.raio_perseguicao = 350
        self.vel = pygame.math.Vector2(0, 0)
        self.perseguindo = False
        self.inicio_perseguicao = 0

    def update(self):
        pos_jogador = self.jogo.jogador.pos
        vetor_distancia = pos_jogador - self.pos
        esta_no_alcance = vetor_distancia.length() < self.raio_perseguicao
        
        velocidade_atual = self.velocidade_original
        velocidade_maxima = self.velocidade_original * 1.5

        if esta_no_alcance:
            if not self.perseguindo:
                self.perseguindo = True
                self.inicio_perseguicao = pygame.time.get_ticks()

            duracao_perseguicao = pygame.time.get_ticks() - self.inicio_perseguicao
            if duracao_perseguicao > 3000:
                duracao_boost_segundos = (duracao_perseguicao - 3000) / 1000
                boost_velocidade = duracao_boost_segundos * 1
                velocidade_atual += boost_velocidade
            
            if velocidade_atual > velocidade_maxima:
                velocidade_atual = velocidade_maxima
            
            self.vel = vetor_distancia.normalize() * velocidade_atual

        else:
            if self.perseguindo:
                self.perseguindo = False
            self.vel = pygame.math.Vector2(0, 0)

        self.pos.x += self.vel.x
        self.rect.centerx = round(self.pos.x)
        self.checar_colisoes('horizontal')
        self.pos.y += self.vel.y
        self.rect.centery = round(self.pos.y)
        self.checar_colisoes('vertical')
    
    def checar_colisoes(self, direcao):
        colisoes = pygame.sprite.spritecollide(self, self.jogo.plataformas, False)
        if direcao == 'horizontal':
            for colisao in colisoes:
                if self.vel.x > 0: self.rect.right = colisao.rect.left
                elif self.vel.x < 0: self.rect.left = colisao.rect.right
                self.pos.x = self.rect.centerx
                self.vel.x = 0
        if direcao == 'vertical':
            for colisao in colisoes:
                if self.vel.y > 0: self.rect.bottom = colisao.rect.top
                elif self.vel.y < 0: self.rect.top = colisao.rect.bottom
                self.pos.y = self.rect.centery
                self.vel.y = 0

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(NOME_JOGO)
        self.relogio = pygame.time.Clock()
        self.rodando = True
        
        self.fonte_titulo = pygame.font.Font(None, 100)
        self.fonte_menu = pygame.font.Font(None, 74)
        self.fonte_hud = pygame.font.Font(None, 40)
        
        self.vidas_jogador = JOGADOR_VIDAS_INICIAIS
        self.moedas_coletadas_jogador = 0
        self.coracoes_coletados = set()
        
        self.estado_jogo = 'menu_principal'
        self.modo_debug = False

    def novo_nivel(self):
        self.todos_os_sprites = pygame.sprite.Group()
        self.plataformas = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.itens = pygame.sprite.Group()

        x_inicial_mundo = -(LARGURA_MUNDO - LARGURA_TELA) / 2
        
        chao = Plataforma(x_inicial_mundo, ALTURA_TELA - 100, LARGURA_MUNDO, 100, CINZA)
        self.plataformas.add(chao)
        self.todos_os_sprites.add(chao)
        
        for dados_plataforma in LISTA_PLATAFORMAS:
            p = Plataforma(*dados_plataforma, LARANJA)
            self.plataformas.add(p)
            self.todos_os_sprites.add(p)

        for dados_parede in LISTA_PAREDES:
            w = Parede(*dados_parede)
            self.plataformas.add(w)
            self.todos_os_sprites.add(w)

        for dados_moeda in LISTA_MOEDAS: self.adicionar_item(Moeda, dados_moeda)
        for dados_botas in LISTA_BOTAS: self.adicionar_item(Botas, dados_botas)
        for dados_coracao in LISTA_CORACOES:
            if dados_coracao[2] not in self.coracoes_coletados:
                self.adicionar_item(Coracao, dados_coracao)

        for dados in LISTA_INIMIGOS_PATRULHA: self.adicionar_inimigo(InimigoPatrulha, dados)
        for dados in LISTA_INIMIGOS_SALTADORES: self.adicionar_inimigo(InimigoSaltador, dados)
        for dados in LISTA_INIMIGOS_PERSEGUIDORES: self.adicionar_inimigo(InimigoPerseguidor, dados)

        self.jogador = Jogador(self)
        self.todos_os_sprites.add(self.jogador)
        self.camera = Camera(LARGURA_MUNDO, ALTURA_TELA)
        
        self.rodar_nivel()

    def adicionar_inimigo(self, classe_inimigo, dados):
        e = classe_inimigo(self, *dados)
        self.inimigos.add(e)
        self.todos_os_sprites.add(e)
    
    def adicionar_item(self, classe_item, dados):
        i = classe_item(*dados)
        self.itens.add(i)
        self.todos_os_sprites.add(i)

    def rodar_nivel(self):
        self.jogando = True
        while self.jogando:
            self.relogio.tick(FPS)
            self.eventos_jogo()
            self.update_jogo()
            self.desenhar_jogo()

    def update_jogo(self):
        self.todos_os_sprites.update()
        self.camera.update(self.jogador)

        self.jogador.pos.x += self.jogador.vel.x
        self.jogador.rect.centerx = round(self.jogador.pos.x)
        colisoes = pygame.sprite.spritecollide(self.jogador, self.plataformas, False)
        for colisao in colisoes:
            if self.jogador.vel.x > 0: self.jogador.rect.right = colisao.rect.left
            elif self.jogador.vel.x < 0: self.jogador.rect.left = colisao.rect.right
            self.jogador.pos.x = self.jogador.rect.centerx
            self.jogador.vel.x = 0

        self.jogador.pos.y += self.jogador.vel.y
        self.jogador.rect.midbottom = self.jogador.pos
        colisoes = pygame.sprite.spritecollide(self.jogador, self.plataformas, False)
        for colisao in colisoes:
            if self.jogador.vel.y > 0:
                 self.jogador.rect.bottom = colisao.rect.top
                 self.jogador.pos.y = self.jogador.rect.bottom
                 self.jogador.vel.y = 0
                 self.jogador.pulos_feitos = 0
            elif self.jogador.vel.y < 0:
                self.jogador.rect.top = colisao.rect.bottom
                self.jogador.pos.y = self.jogador.rect.bottom
                self.jogador.vel.y = 0
        
        colisoes_inimigos = pygame.sprite.spritecollide(self.jogador, self.inimigos, False)
        if colisoes_inimigos:
            self.jogador.sofrer_dano(1)
        
        # --- Colisão Jogador com Itens ---
        if not self.modo_debug:
            colisoes_itens = pygame.sprite.spritecollide(self.jogador, self.itens, True)
            for item in colisoes_itens:
                if isinstance(item, Moeda):
                    self.moedas_coletadas_jogador += 1
                if isinstance(item, Coracao):
                    self.jogador.vida = JOGADOR_VIDA_MAXIMA
                    self.vidas_jogador += 1
                    self.coracoes_coletados.add(item.id_item)
                if isinstance(item, Botas):
                    self.jogador.tem_pulo_duplo = True

        if self.jogador.vida <= 0:
            self.jogando = False
            self.vidas_jogador -= 1
            self.estado_jogo = 'tela_morte'

    def eventos_jogo(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if self.jogando: self.jogando = False
                self.rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]:
                    self.jogador.pular()
                if evento.key == pygame.K_F5:
                    self.jogando = False
                    self.resetar_jogo()
                    self.estado_jogo = 'menu_principal'
                if evento.key == pygame.K_F9:
                    self.modo_debug = not self.modo_debug

    def desenhar_hud(self):
        largura_barra_vida = 30
        altura_barra_vida = 25
        for i in range(JOGADOR_VIDA_MAXIMA):
            cor = VERDE if i < self.jogador.vida else VERMELHO
            rect = pygame.Rect(20 + i * (largura_barra_vida + 5), 20, largura_barra_vida, altura_barra_vida)
            pygame.draw.rect(self.tela, cor, rect)

        pos_y_icone_vida = 20 + altura_barra_vida + 10
        icone_vida = pygame.Rect(20, pos_y_icone_vida, 25, 25)
        pygame.draw.rect(self.tela, VERMELHO_ESCURO, icone_vida)
        
        texto_vidas = self.fonte_hud.render(f'x {self.vidas_jogador}', True, BRANCO)
        rect_texto_vidas = texto_vidas.get_rect(midleft=(icone_vida.right + 10, icone_vida.centery))
        self.tela.blit(texto_vidas, rect_texto_vidas)
        
        pos_icone_moeda = (LARGURA_TELA - 100, 35)
        pygame.draw.circle(self.tela, AMARELO, pos_icone_moeda, 15)
        
        texto_moedas = self.fonte_hud.render(f'x {self.moedas_coletadas_jogador}', True, BRANCO)
        rect_texto_moedas = texto_moedas.get_rect(midleft=(pos_icone_moeda[0] + 20, pos_icone_moeda[1]))
        self.tela.blit(texto_moedas, rect_texto_moedas)

        # Indicador de Pulo Duplo
        if self.jogador.tem_pulo_duplo:
            largura_bota_hud = int(30 * 1.5)
            altura_bota_hud = int(25 * 1.5)
            pos_x_bota = pos_icone_moeda[0] - (largura_bota_hud / 2)
            pos_y_bota = pos_icone_moeda[1] + 30
            rect_bota = pygame.Rect(pos_x_bota, pos_y_bota, largura_bota_hud, altura_bota_hud)
            pygame.draw.rect(self.tela, CIANO, rect_bota)
        
        # Coordenadas de Debug
        pos_texto = f"Pos: ({int(self.jogador.rect.x)}, {int(self.jogador.rect.y)})"
        texto_pos = self.fonte_hud.render(pos_texto, True, BRANCO)
        rect_pos = texto_pos.get_rect(bottomleft=(10, ALTURA_TELA - 10))
        self.tela.blit(texto_pos, rect_pos)
        
        # Indicador de Modo Debug
        if self.modo_debug:
            texto_debug = self.fonte_hud.render("MODO DEBUG", True, VERMELHO)
            rect_debug = texto_debug.get_rect(center=(LARGURA_TELA / 2, 25))
            self.tela.blit(texto_debug, rect_debug)


    def desenhar_jogo(self):
        self.tela.fill(PRETO)
        for sprite in self.todos_os_sprites:
            self.tela.blit(sprite.image, self.camera.aplicar(sprite))
        
        self.desenhar_hud()
        
        pygame.display.flip()

    def mostrar_menu_principal(self):
        self.tela.fill(PRETO)
        
        texto_titulo = self.fonte_titulo.render(NOME_JOGO, True, VERMELHO)
        rect_titulo = texto_titulo.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 4))
        self.tela.blit(texto_titulo, rect_titulo)

        botao_jogar = pygame.Rect(LARGURA_TELA/2 - 100, ALTURA_TELA * 0.5, 200, 50)
        botao_creditos = pygame.Rect(LARGURA_TELA/2 - 100, ALTURA_TELA * 0.6, 200, 50)
        botao_sair = pygame.Rect(LARGURA_TELA/2 - 100, ALTURA_TELA * 0.7, 200, 50)

        pygame.draw.rect(self.tela, CINZA, botao_jogar)
        pygame.draw.rect(self.tela, CINZA, botao_creditos)
        pygame.draw.rect(self.tela, CINZA, botao_sair)
        
        texto_jogar = self.fonte_menu.render("Jogar", True, PRETO)
        self.tela.blit(texto_jogar, texto_jogar.get_rect(center=botao_jogar.center))
        texto_creditos = self.fonte_menu.render("Créditos", True, PRETO)
        self.tela.blit(texto_creditos, texto_creditos.get_rect(center=botao_creditos.center))
        texto_sair = self.fonte_menu.render("Sair", True, PRETO)
        self.tela.blit(texto_sair, texto_sair.get_rect(center=botao_sair.center))
        
        pygame.display.flip()

        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    esperando = False
                    self.rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_jogar.collidepoint(evento.pos):
                        self.estado_jogo = 'jogando'
                        esperando = False
                    if botao_creditos.collidepoint(evento.pos):
                        self.estado_jogo = 'creditos'
                        esperando = False
                    if botao_sair.collidepoint(evento.pos):
                        esperando = False
                        self.rodando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_F5:
                        self.resetar_jogo()
                        # O loop vai terminar e o menu será redesenhado com os valores resetados
                        esperando = False


    def mostrar_creditos(self):
        self.tela.fill(PRETO)
        
        criadores = [CRIADOR_1, CRIADOR_2, CRIADOR_3, CRIADOR_4, CRIADOR_5, CRIADOR_6]
        for i, nome in enumerate(criadores):
            texto_criador = self.fonte_hud.render(nome, True, CINZA)
            rect_criador = texto_criador.get_rect(left=50, top=100 + i * 50)
            self.tela.blit(texto_criador, rect_criador)

        botao_jogar = pygame.Rect(LARGURA_TELA * 0.7, ALTURA_TELA * 0.5, 200, 50)
        botao_voltar = pygame.Rect(LARGURA_TELA * 0.7, ALTURA_TELA * 0.6, 200, 50)

        pygame.draw.rect(self.tela, AMARELO, botao_jogar)
        pygame.draw.rect(self.tela, VERMELHO, botao_voltar)

        texto_jogar = self.fonte_menu.render("Jogar", True, PRETO)
        self.tela.blit(texto_jogar, texto_jogar.get_rect(center=botao_jogar.center))
        texto_voltar = self.fonte_menu.render("Voltar", True, PRETO)
        self.tela.blit(texto_voltar, texto_voltar.get_rect(center=botao_voltar.center))

        pygame.display.flip()

        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    esperando = False
                    self.rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_jogar.collidepoint(evento.pos):
                        self.estado_jogo = 'jogando'
                        esperando = False
                    if botao_voltar.collidepoint(evento.pos):
                        self.estado_jogo = 'menu_principal'
                        esperando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_F5:
                        self.resetar_jogo()
                        self.estado_jogo = 'menu_principal'
                        esperando = False
    
    def mostrar_tela_morte(self):
        self.tela.fill(PRETO)
        
        texto_morte = self.fonte_titulo.render("Você morreu", True, VERMELHO)
        rect_morte = texto_morte.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 3))
        self.tela.blit(texto_morte, rect_morte)

        if self.vidas_jogador >= 0:
            texto_respawn = self.fonte_menu.render("Aperte R para renascer", True, AMARELO)
            rect_respawn = texto_respawn.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA * 0.6))
            self.tela.blit(texto_respawn, rect_respawn)
        else:
            texto_fim = self.fonte_titulo.render("Fim de Jogo", True, VERMELHO)
            rect_fim = texto_fim.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA * 0.6))
            self.tela.blit(texto_fim, rect_fim)
            
        pygame.display.flip()

        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    esperando = False
                    self.rodando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r and self.vidas_jogador >= 0:
                        self.estado_jogo = 'jogando'
                        esperando = False
                    if evento.key == pygame.K_F5:
                        self.resetar_jogo()
                        self.estado_jogo = 'menu_principal'
                        esperando = False
        
        if self.vidas_jogador < 0:
            pygame.time.wait(2000) # Espera 2 segundos na tela de Fim de Jogo
            self.resetar_jogo()
            self.estado_jogo = 'menu_principal'

    def resetar_jogo(self):
        """ Reseta as estatísticas para um novo jogo. """
        self.vidas_jogador = JOGADOR_VIDAS_INICIAIS
        self.moedas_coletadas_jogador = 0
        self.coracoes_coletados.clear()


# --- Execução do Jogo ---
g = Jogo()
while g.rodando:
    if g.estado_jogo == 'menu_principal':
        g.mostrar_menu_principal()
    elif g.estado_jogo == 'creditos':
        g.mostrar_creditos()
    elif g.estado_jogo == 'jogando':
        g.novo_nivel()
    elif g.estado_jogo == 'tela_morte':
        g.mostrar_tela_morte()

pygame.quit()
sys.exit()
