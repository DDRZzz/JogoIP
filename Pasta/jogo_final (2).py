import pygame
import sys
import math

# --- CONFIGURAÇÕES GERAIS DO JOGO ---
NOME_JOGO = "Android 25"
CRIADOR_1 = "João Luiz da Silva Santos Araujo - jlssa"
CRIADOR_2 = "Leoncio Alves Ferreira Neto - lafn"
CRIADOR_3 = "Breno Jose Ramos da Silva- bjrs"
CRIADOR_4 = "Jonas Manoel Barbosa da Lima - jmbl2"
CRIADOR_5 = "Daniel Rodrigues Zuza - drz"
CRIADOR_6 = "Caio de Oliveira Daltro Gouté - codg"


# --- Constantes ---
LARGURA_TELA = 1200
ALTURA_TELA = 800
LARGURA_MUNDO = 15000 # Aumentado em 5000
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
    (2358, 313, 188, 25), 
    (2779, 430, 100, 25),
    (2679, 580, 200, 25),
    (2979, 580, 100, 25),
    (3107, 394, 200, 25),
    (3439, 394, 450, 25),
    (3968, 260, 200, 25),
    (4402, 454, 100, 25),
    (4668, 272, 350, 40),
    (5347, 272, 350, 40),
    (6000, 450, 200, 25),
    (6346, 285, 350, 40)
]

# Paredes: (x, y, largura, altura)
LISTA_PAREDES = [
    (2879, 350, 100, 350),
    (4247, 250, 150, 450),
    (7130, 284, 300, 600),
    (7400, -400, 100, 1600)
]

# Moedas: (x, y)
LISTA_MOEDAS = [
    (1558, 172),
    (1663, 172),
    (1614, 65),
    (450, ALTURA_TELA - 250),
    (700, ALTURA_TELA - 300),
    (850, ALTURA_TELA - 400),
    (925, ALTURA_TELA - 400),
    (1700, ALTURA_TELA - 300),
    (1625, ALTURA_TELA - 125),
    (2080, ALTURA_TELA - 200),
    (2400, ALTURA_TELA - 150),
    (2803, 523),
    (2818, 373),
    (3364, 213),
    (3480, 260),
    (3569, 260),
    (3680, 260),
    (4038, 197),
    (4422, 380),
    (4849, 488),
    (5395, 187),
    (5710, 460),
    (6186, 600),
    (6400, 360),
    (7025, 614),
    (7000, 614),
    (6975, 614),
    (6950, 614),
    (6925, 614)
]

# Itens Especiais
# Corações: (x, y, 'id_unico_do_coracao')
LISTA_CORACOES = [
    (2463, 242, 'cora1'),
    (4155, 635, 'cora2'),
    (6457, 550, 'cora3')
]
# Botas: (x, y)
LISTA_BOTAS = [(4298, 158)]
# Baú: (x, y)
LISTA_BAU = [(7222, 184)]


# Inimigos Patrulha (Vermelho): (x, y, largura, altura, velocidade, alcance_patrulha, direcao_inicial)
LISTA_INIMIGOS_PATRULHA = [
    (200, ALTURA_TELA - 100 - 40, 40, 40, 1, 50, 'direita'), # Inimigo atrás do jogador
    (400, ALTURA_TELA - 100 - 40, 40, 40, 2, 250, 'direita'),
    (3053, 660, 40, 40, 2, 200, 'direita'),
    (3273, 660, 40, 40, 2, 200, 'direita'),
    (3493, 660, 40, 40, 2, 200, 'direita'),
    (3713, 660, 40, 40, 2, 200, 'direita'),
    (4598, 660, 40, 40, 4, 150, 'direita'),
    (5415, 660, 40, 40, 4, 200, 'direita'),
    (4748, 222, 50, 50, 3, 200, 'direita'),
    (6360, 235, 50, 50, 4, 200, 'direita'),
    (6500, 660, 75, 75, 5, 300, 'direita'),
    (6280, 660, 80, 80, 4, 250, 'direita')
]

# Inimigos Saltadores (Roxo): (x, y, largura, altura, altura_pulo)
LISTA_INIMIGOS_SALTADORES = [
    (1563, ALTURA_TELA - 100 - 40, 40, 40, 125),
    (1688, ALTURA_TELA - 100 - 40, 40, 40, 188),
    (2388, 269, 40, 40, 188),
    (3620, 359, 40, 40, 188),
    (3760, 359, 40, 40, 188),
    (5125, 660, 40, 40, 200),
    (5888, 660, 50, 50, 350)
]

# Inimigos Perseguidores (Marrom): (x, y, largura, altura, velocidade)
LISTA_INIMIGOS_PERSEGUIDORES = [
    (1992, 650, 40, 40, 1), 
    (5214, 181, 40, 40, 2), 
    (5605, 450, 30, 30, 3), 
    (6018, 120, 50, 50, 2), 
    (6854, 320, 20, 20, 1)
]


# --- Classes ---

class Camera:
    def __init__(self, largura, altura):
        self.camera = pygame.Rect(0, 0, largura, altura)
        self.largura = largura
        self.altura = altura

    def aplicar(self, entidade):
        return entidade.rect.move(self.camera.topleft)

    def update(self, alvo):
        pos_alvo_x = alvo.rect.centerx
        if pos_alvo_x > 6800:
            pos_alvo_x = 6800
        x = -pos_alvo_x + int(LARGURA_TELA / 2)
        x = min(0, x)
        x = max(-(self.largura - LARGURA_TELA), x)
        self.camera = pygame.Rect(x, 0, self.largura, self.altura)

class Jogador(pygame.sprite.Sprite):
    def __init__(self, jogo):
        super().__init__()
        self.jogo = jogo
        self.frames_idle = self.jogo.frames_jogador_idle
        self.frames_run = self.jogo.frames_jogador_run
        self.frames_jump = self.jogo.frames_jogador_jump
        self.current_frame = 0
        self.last_update = 0
        self.image = self.frames_idle[0]
        self.rect = self.image.get_rect()
        self.rect.size = (50, 50)
        
        self.pos = pygame.math.Vector2(150, ALTURA_TELA - 100)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.rect.midbottom = self.pos
        
        self.vida = JOGADOR_VIDA_MAXIMA
        self.momento_ultimo_dano = 0
        self.tem_pulo_duplo = False
        self.pulos_feitos = 0
        self.direcao = 'direita'
        self.morrendo = False
        self.andando = False
        self.pulando = False

    def pular(self):
        if self.jogo.modo_debug or self.morrendo:
            return
        if self.pulos_feitos == 0:
            self.rect.y += 1
            colisoes = pygame.sprite.spritecollide(self, self.jogo.plataformas, False)
            self.rect.y -= 1
            if colisoes:
                self.vel.y = JOGADOR_FORCA_PULO
                self.pulos_feitos = 1
        elif self.pulos_feitos == 1 and self.tem_pulo_duplo:
            self.vel.y = JOGADOR_FORCA_PULO * 0.8
            self.pulos_feitos = 2

    def sofrer_dano(self, quantidade):
        if self.jogo.modo_debug or self.morrendo:
            return
        agora = pygame.time.get_ticks()
        if agora - self.momento_ultimo_dano > JOGADOR_DURACAO_INVENCIBILIDADE:
            self.vida -= quantidade
            self.momento_ultimo_dano = agora
            if self.vida < 0:
                self.vida = 0

    def animar(self):
        agora = pygame.time.get_ticks()
        
        if self.morrendo:
            if agora - self.last_update > 100:
                self.last_update = agora
                self.current_frame += 1
                if self.current_frame >= len(self.jogo.frames_jogador_morte):
                    self.current_frame = len(self.jogo.frames_jogador_morte) - 1
                imagem_original = self.jogo.frames_jogador_morte[self.current_frame]
                centro_antigo = self.rect.center
                if self.direcao == 'direita':
                    self.image = imagem_original
                else:
                    self.image = pygame.transform.flip(imagem_original, True, False)
                self.rect = self.image.get_rect()
                self.rect.size = (50, 50)
                self.rect.center = centro_antigo
            return

        frames_atuais = self.frames_idle
        if self.pulando:
            frames_atuais = self.frames_jump
        elif self.andando:
            frames_atuais = self.frames_run

        if agora - self.last_update > 100:
            self.last_update = agora
            self.current_frame = (self.current_frame + 1) % len(frames_atuais)
            imagem_original = frames_atuais[self.current_frame]
            centro_antigo = self.rect.center
            if self.direcao == 'direita':
                self.image = imagem_original
            else:
                self.image = pygame.transform.flip(imagem_original, True, False)
            self.rect = self.image.get_rect()
            self.rect.size = (50, 50)
            self.rect.center = centro_antigo

    def update(self):
        self.animar()

        if self.morrendo:
            return

        if not self.jogo.modo_debug:
            self.acc = pygame.math.Vector2(0, JOGADOR_GRAVIDADE)
            aceleracao_atual = JOGADOR_ACELERACAO
            if self.tem_pulo_duplo:
                aceleracao_atual *= 1.2
            
            self.andando = False
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                self.acc.x = -aceleracao_atual
                self.direcao = 'esquerda'
                self.andando = True
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                self.acc.x = aceleracao_atual
                self.direcao = 'direita'
                self.andando = True
            
            self.acc.x += self.vel.x * JOGADOR_ATRITO
            self.vel += self.acc
            if self.vel.y > 15:
                self.vel.y = 15
        else:
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
    def __init__(self, jogo, x, y, largura, altura):
        super().__init__()
        self.jogo = jogo
        self.image = pygame.Surface((largura, altura))
        for i in range(0, largura, self.jogo.imagem_chao.get_width()):
            for j in range(0, altura, self.jogo.imagem_chao.get_height()):
                self.image.blit(self.jogo.imagem_chao, (i, j))
        self.rect = self.image.get_rect(topleft=(x, y))

class Parede(pygame.sprite.Sprite):
    def __init__(self, jogo, x, y, largura, altura):
        super().__init__()
        self.jogo = jogo
        self.image = pygame.Surface((largura, altura))
        for i in range(0, largura, self.jogo.imagem_chao.get_width()):
            for j in range(0, altura, self.jogo.imagem_chao.get_height()):
                self.image.blit(self.jogo.imagem_chao, (i, j))
        self.rect = self.image.get_rect(topleft=(x, y))

class Moeda(pygame.sprite.Sprite):
    def __init__(self, jogo, x, y):
        super().__init__()
        self.jogo = jogo
        self.image = self.jogo.imagem_moeda
        self.rect = self.image.get_rect(topleft=(x, y))

class Coracao(pygame.sprite.Sprite):
    def __init__(self, jogo, x, y, id_item):
        super().__init__()
        self.jogo = jogo
        self.image = self.jogo.imagem_coracao
        self.rect = self.image.get_rect(topleft=(x, y))
        self.id_item = id_item

class Botas(pygame.sprite.Sprite):
    def __init__(self, jogo, x, y):
        super().__init__()
        self.jogo = jogo
        self.image = self.jogo.imagem_bota
        self.rect = self.image.get_rect(topleft=(x, y))

class Bau(pygame.sprite.Sprite):
    def __init__(self, jogo, x, y):
        super().__init__()
        self.jogo = jogo
        self.image = self.jogo.imagem_bau
        self.rect = self.image.get_rect(topleft=(x, y))

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
        
        # --- Lógica de Animação ---
        self.load_animation_sprites(largura, altura)
        self.current_animation = 'walk' # Este inimigo está sempre andando
        self.frame_index = 0
        self.animation_speed = 0.15 # Uma boa velocidade para a animação de caminhada
        self.image = self.animations[self.current_animation][self.frame_index]
        # O rect é criado com base na imagem, mas centrado na posição inicial
        self.rect = self.image.get_rect(center=self.pos)

        # --- Lógica de Comportamento (Original) ---
        self.velocidade = velocidade
        self.alcance_patrulha = alcance_patrulha
        if direcao_inicial == 'direita':
            self.direcao = 1 # 1 para direita
            self.x_inicial = x
            self.x_final = x + alcance_patrulha
        else:
            self.direcao = -1 # -1 para esquerda
            self.x_inicial = x - alcance_patrulha
            self.x_final = x

    def load_animation_sprites(self, largura, altura):
        frame_size = (128, 128) # Tamanho do frame original da spritesheet do esqueleto
        path = "sprites_inimigos/Skeleton/"
        new_size = (largura, altura) # Tamanho final desejado, vindo da lista de inimigos
        
        self.animations = {
            "idle": self.load_spritesheet(f"{path}Idle.png", frame_size, new_size),
            "walk": self.load_spritesheet(f"{path}Walk.png", frame_size, new_size),
            "attack": self.load_spritesheet(f"{path}Attack.png", frame_size, new_size),
            "hurt": self.load_spritesheet(f"{path}Hurt.png", frame_size, new_size),
            "dead": self.load_spritesheet(f"{path}Dead.png", frame_size, new_size)
        }

    def load_spritesheet(self, file, frame_size, new_size=None):
        frames = []
        try:
            sheet = pygame.image.load(file).convert_alpha()
            sheet_width, sheet_height = sheet.get_size()
            frame_width, frame_height = frame_size
            num_frames = sheet_width // frame_width
            
            for i in range(num_frames):
                frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                if new_size:
                    frame = pygame.transform.scale(frame, new_size)
                frames.append(frame)
        except pygame.error as e:
            print(f"Erro ao carregar a spritesheet: {file} - {e}")
            fallback_frame = pygame.Surface(new_size if new_size else frame_size)
            fallback_frame.fill(VERMELHO) # Cor de fallback caso a imagem não seja encontrada
            frames.append(fallback_frame)
        return frames

    def animate(self):
        # Avança o frame da animação
        self.frame_index += self.animation_speed
        animation_list = self.animations[self.current_animation]
        
        if self.frame_index >= len(animation_list):
            self.frame_index = 0
            
        original_image = animation_list[int(self.frame_index)]
        
        # Vira a imagem para a esquerda se a direção for -1
        if self.direcao == -1: 
            self.image = pygame.transform.flip(original_image, True, False)
        else: # Mantém a imagem original para a direita
            self.image = original_image
            
        # Atualiza o centro do rect para a posição de física
        self.rect.center = self.pos

    def update(self):
        # --- A SUA LÓGICA DE PATRULHA ORIGINAL E INTACTA ---
        self.pos.x += self.velocidade * self.direcao
        self.rect.x = self.pos.x # Sincroniza o rect com a posição
        
        # Inverte direção nos limites da patrulha
        if self.pos.x >= self.x_final or self.pos.x <= self.x_inicial:
            self.direcao *= -1
            
        # Checa colisão e redefine a patrulha se necessário
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
        # --- FIM DA SUA LÓGICA ORIGINAL ---

        # --- Chamada para a nova Lógica de Animação ---
        self.animate()

class InimigoSaltador(Inimigo):
    def __init__(self, jogo, x, y, largura, altura, altura_pulo):
        super().__init__(jogo, x, y, largura, altura)
        
        # --- Lógica de Animação ---
        self.load_animation_sprites(largura, altura)
        self.current_animation = "idle" # Sempre 'idle' neste caso
        self.frame_index = 0
        self.animation_speed = 0.2
        self.image = self.animations[self.current_animation][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        # --- Lógica de Comportamento (Original) ---
        self.y_inicial = self.pos.y # Usar self.pos.y para mais precisão
        self.vel_y = 0
        self.estado = 'esperando'
        self.ultima_atualizacao = pygame.time.get_ticks()
        self.tempo_espera = 500 # Tempo em ms que ele espera no chão
        
        # Cálculo da física do pulo (Original)
        frames_ate_pico = (1500 / 1000) * FPS / 2
        # Previne divisão por zero se frames_ate_pico for 0
        if frames_ate_pico > 0:
            self.gravidade = (2 * altura_pulo) / (frames_ate_pico ** 2)
            self.forca_pulo = -self.gravidade * frames_ate_pico
        else:
            self.gravidade = JOGADOR_GRAVIDADE # Usa uma gravidade padrão como fallback
            self.forca_pulo = -20

    def load_animation_sprites(self, largura, altura):
        frame_size = (128, 128)
        path = "sprites_inimigos/Plent/"
        new_size = (largura, altura)
        
        # Carregamos apenas a animação 'idle', como solicitado
        self.animations = {
            "idle": self.load_spritesheet(f"{path}Idle.png", frame_size, new_size)
        }

    def load_spritesheet(self, file, frame_size, new_size=None):
        frames = []
        try:
            sheet = pygame.image.load(file).convert_alpha()
            sheet_width, sheet_height = sheet.get_size()
            frame_width, frame_height = frame_size
            num_frames = sheet_width // frame_width
            
            for i in range(num_frames):
                frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                if new_size:
                    frame = pygame.transform.scale(frame, new_size)
                frames.append(frame)
        except pygame.error as e:
            print(f"Erro ao carregar a spritesheet: {file} - {e}")
            fallback_frame = pygame.Surface(new_size if new_size else frame_size)
            fallback_frame.fill(ROXO) # Usa a cor ROXA original como fallback
            frames.append(fallback_frame)
        return frames

    def animate(self):
        # Como só temos 'idle', não precisamos de set_animation
        self.frame_index += self.animation_speed
        animation_list = self.animations[self.current_animation]
        
        if self.frame_index >= len(animation_list):
            self.frame_index = 0
            
        self.image = animation_list[int(self.frame_index)]
        # Garante que o centro do rect esteja sempre na posição correta
        self.rect.center = self.pos

    def update(self):
        # --- Lógica de Pulo (Original) ---
        agora = pygame.time.get_ticks()
        if self.estado == 'esperando':
            if agora - self.ultima_atualizacao > self.tempo_espera:
                self.estado = 'pulando'
                self.vel_y = self.forca_pulo
                self.ultima_atualizacao = agora
        elif self.estado == 'pulando':
            self.vel_y += self.gravidade
            self.pos.y += self.vel_y
            
            # Atualiza o rect para a nova posição ANTES de checar colisão
            self.rect.centery = round(self.pos.y)

            # Checa colisão com o chão original (y_inicial)
            if self.pos.y >= self.y_inicial and self.vel_y > 0:
                self.pos.y = self.y_inicial
                self.vel_y = 0
                self.estado = 'esperando'
                self.ultima_atualizacao = agora
            
            # Checa colisão com plataformas
            colisoes = pygame.sprite.spritecollide(self, self.jogo.plataformas, False)
            for colisao in colisoes:
                # Se está caindo e colide
                if self.vel_y > 0:
                    self.rect.bottom = colisao.rect.top
                    self.pos.y = self.rect.centery
                    self.vel_y = 0
                    self.estado = 'esperando'
                    self.ultima_atualizacao = agora
                # Se está subindo e colide
                elif self.vel_y < 0:
                    self.rect.top = colisao.rect.bottom
                    self.pos.y = self.rect.centery
                    self.vel_y = 0 # Interrompe o pulo se bate a cabeça
        
        # Sincroniza a posição final do rect com a posição de física
        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)

        # --- Lógica de Animação (Nova) ---
        self.animate() # Anima o sprite no final de cada update

class InimigoPerseguidor(Inimigo):
    def __init__(self, jogo, x, y, largura, altura, velocidade):
        super().__init__(jogo, x, y, largura, altura)
        
        # --- Lógica de Animação ---
        self.load_animation_sprites(largura, altura)
        self.current_animation = "idle"
        self.frame_index = 0
        self.animation_speed = 0.2  # Ajuste para controlar a velocidade da animação
        self.image = self.animations[self.current_animation][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        
        # --- Lógica de Comportamento ---
        self.velocidade_original = velocidade
        self.raio_perseguicao = 350
        self.vel = pygame.math.Vector2(0, 0)
        self.perseguindo = False
        self.inicio_perseguicao = 0
        self.direcao_visual = 1 # 1 para direita, -1 para esquerda

    def load_animation_sprites(self, largura, altura):
        frame_size = (128, 128)
        # Caminho relativo correto, baseado na Etapa 0
        path = "sprites_inimigos/Fire_Spirit/"
        # O tamanho do inimigo (largura, altura) será usado para redimensionar as imagens
        new_size = (largura, altura)
        
        self.animations = {
            "idle": self.load_spritesheet(f"{path}Idle.png", frame_size, new_size),
            "run": self.load_spritesheet(f"{path}Run.png", frame_size, new_size),
            "attack": self.load_spritesheet(f"{path}Attack.png", frame_size, new_size),
            "explosion": self.load_spritesheet(f"{path}Explosion.png", frame_size, new_size),
        }

    def load_spritesheet(self, file, frame_size, new_size=None):
        frames = []
        try:
            sheet = pygame.image.load(file).convert_alpha()
            sheet_width, sheet_height = sheet.get_size()
            frame_width, frame_height = frame_size
            num_frames = sheet_width // frame_width
            
            for i in range(num_frames):
                frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                if new_size:
                    # Redimensiona o frame para o tamanho definido na lista de inimigos
                    frame = pygame.transform.scale(frame, new_size)
                frames.append(frame)
        except pygame.error as e:
            print(f"Erro ao carregar a spritesheet: {file} - {e}")
            fallback_frame = pygame.Surface(new_size if new_size else frame_size)
            fallback_frame.fill(MARROM) # Usa a cor MARROM original como fallback
            frames.append(fallback_frame)
        return frames

    def set_animation(self, name):
        if name in self.animations and name != self.current_animation:
            self.current_animation = name
            self.frame_index = 0

    def animate(self):
        self.frame_index += self.animation_speed
        animation_list = self.animations[self.current_animation]
        
        if self.frame_index >= len(animation_list):
            self.frame_index = 0
            
        original_image = animation_list[int(self.frame_index)]
        
        # Vira a imagem se a direção for para a esquerda
        if self.direcao_visual == -1:
            self.image = pygame.transform.flip(original_image, True, False)
        else:
            self.image = original_image
            
        self.rect.center = self.pos 

    def update(self):
        pos_jogador = self.jogo.jogador.pos
        vetor_distancia = pos_jogador - self.pos
        
        if vetor_distancia.length_squared() > 0: # Evita erro de normalização com vetor zero
            self.direcao_visual = 1 if vetor_distancia.x > 0 else -1

        esta_no_alcance = vetor_distancia.length_squared() < self.raio_perseguicao**2
        velocidade_atual = self.velocidade_original
        velocidade_maxima = self.velocidade_original * 1.5

        if esta_no_alcance:
            if not self.perseguindo:
                self.perseguindo = True
                self.inicio_perseguicao = pygame.time.get_ticks()
            
            self.set_animation('run')
            
            duracao_perseguicao = pygame.time.get_ticks() - self.inicio_perseguicao
            if duracao_perseguicao > 3000:
                duracao_boost_segundos = (duracao_perseguicao - 3000) / 1000
                boost_velocidade = duracao_boost_segundos * 1
                velocidade_atual = min(velocidade_atual + boost_velocidade, velocidade_maxima)
            
            if vetor_distancia.length() > 0:
                self.vel = vetor_distancia.normalize() * velocidade_atual
        else:
            if self.perseguindo:
                self.perseguindo = False
            self.set_animation('idle')
            self.vel = pygame.math.Vector2(0, 0)
        
        self.animate()

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
        pygame.mixer.init()
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
        self.carregar_dados()

    def carregar_dados(self):
        self.imagem_chao = pygame.image.load("chao_pedra.png").convert()
        self.imagem_fundo = pygame.image.load("cena_fundo.png").convert()
        self.imagem_moeda_original = pygame.image.load("Gold_21.png").convert_alpha()
        self.imagem_moeda = pygame.transform.scale(self.imagem_moeda_original, (30, 30))
        self.imagem_moeda_hud = pygame.transform.scale(self.imagem_moeda_original, (40, 40))
        self.imagem_bota_original = pygame.image.load("bota_jump.png").convert_alpha()
        self.imagem_bota = pygame.transform.scale(self.imagem_bota_original, (40, 40))
        self.imagem_bota_hud = pygame.transform.scale(self.imagem_bota_original, (int(40 * 1.5), int(40 * 1.5)))
        self.imagem_coracao_original = pygame.image.load("cuore2.png").convert_alpha()
        self.imagem_coracao = pygame.transform.scale(self.imagem_coracao_original, (30, 30))
        self.imagem_coracao_hud = pygame.transform.scale(self.imagem_coracao_original, (35, 35))
        self.imagem_bau_original = pygame.image.load("bau_tesouro.png").convert_alpha()
        self.imagem_bau = pygame.transform.scale(self.imagem_bau_original, (100, 100))
        
        # Carregar frames do jogador
        self.frames_jogador_idle = []
        for i in range(1, 11):
            filename = f"Idle ({i}).png"
            img = pygame.image.load(filename).convert_alpha()
            self.frames_jogador_idle.append(pygame.transform.scale(img, (75, 75)))
        
        self.frames_jogador_run = []
        for i in range(1, 9):
            filename = f"Run ({i}).png"
            img = pygame.image.load(filename).convert_alpha()
            self.frames_jogador_run.append(pygame.transform.scale(img, (75, 75)))

        self.frames_jogador_jump = []
        for i in range(1, 11):
            filename = f"Jump ({i}).png"
            img = pygame.image.load(filename).convert_alpha()
            self.frames_jogador_jump.append(pygame.transform.scale(img, (75, 75)))

        self.frames_jogador_morte = []
        for i in range(1, 11):
            filename = f"Dead ({i}).png"
            img = pygame.image.load(filename).convert_alpha()
            self.frames_jogador_morte.append(pygame.transform.scale(img, (75, 75)))

        


        try:
            pygame.mixer.music.load('Zelda.mp3')
            self.som_moeda = pygame.mixer.Sound('coin.wav')
            self.som_bota = pygame.mixer.Sound('bota.wav')
            self.som_vida = pygame.mixer.Sound('uplife.wav')
        except pygame.error as e:
            print(f"Não foi possível carregar um arquivo de som: {e}")
            self.som_moeda = pygame.mixer.Sound(buffer=b'')
            self.som_bota = pygame.mixer.Sound(buffer=b'')
            self.som_vida = pygame.mixer.Sound(buffer=b'')

    def novo_nivel(self):
        self.todos_os_sprites = pygame.sprite.Group()
        self.plataformas = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.itens = pygame.sprite.Group()
        self.momento_morte_animada = 0

        x_inicial_mundo = -(LARGURA_MUNDO - LARGURA_TELA) / 2
        chao = Plataforma(self, x_inicial_mundo, ALTURA_TELA - 100, LARGURA_MUNDO, 100)
        self.plataformas.add(chao)
        self.todos_os_sprites.add(chao)
        
        for dados_plataforma in LISTA_PLATAFORMAS:
            p = Plataforma(self, *dados_plataforma)
            self.plataformas.add(p)
            self.todos_os_sprites.add(p)
        for dados_parede in LISTA_PAREDES:
            w = Parede(self, *dados_parede)
            self.plataformas.add(w)
            self.todos_os_sprites.add(w)
        for dados_moeda in LISTA_MOEDAS: self.adicionar_item(Moeda, (self, *dados_moeda))
        for dados_botas in LISTA_BOTAS: self.adicionar_item(Botas, (self, *dados_botas))
        for dados_coracao in LISTA_CORACOES:
            if dados_coracao[2] not in self.coracoes_coletados:
                self.adicionar_item(Coracao, (self, *dados_coracao))
        for dados_bau in LISTA_BAU: self.adicionar_item(Bau, (self, *dados_bau))
        for dados in LISTA_INIMIGOS_PATRULHA: self.adicionar_inimigo(InimigoPatrulha, dados)
        for dados in LISTA_INIMIGOS_SALTADORES: self.adicionar_inimigo(InimigoSaltador, dados)
        for dados in LISTA_INIMIGOS_PERSEGUIDORES: self.adicionar_inimigo(InimigoPerseguidor, dados)
        self.jogador = Jogador(self)
        self.todos_os_sprites.add(self.jogador)
        self.camera = Camera(LARGURA_MUNDO, ALTURA_TELA)
        
        pygame.mixer.music.play(loops=-1)
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
        pygame.mixer.music.stop()

    def update_jogo(self):
        if self.jogador.morrendo:
            if self.momento_morte_animada == 0:
                self.momento_morte_animada = pygame.time.get_ticks()
            
            if pygame.time.get_ticks() - self.momento_morte_animada > 2000: # 1s anim + 1s espera
                self.jogando = False
                self.estado_jogo = 'tela_morte'
            self.todos_os_sprites.update()
            self.camera.update(self.jogador)
            return

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
        self.jogador.pulando = True
        for colisao in colisoes:
            if self.jogador.vel.y > 0:
                 self.jogador.rect.bottom = colisao.rect.top
                 self.jogador.pos.y = self.jogador.rect.bottom
                 self.jogador.vel.y = 0
                 self.jogador.pulos_feitos = 0
                 self.jogador.pulando = False
            elif self.jogador.vel.y < 0:
                self.jogador.rect.top = colisao.rect.bottom
                self.jogador.pos.y = self.jogador.rect.bottom
                self.jogador.vel.y = 0
        
        colisoes_inimigos = pygame.sprite.spritecollide(self.jogador, self.inimigos, False)
        if colisoes_inimigos:
            self.jogador.sofrer_dano(1)
        if not self.modo_debug:
            colisoes_itens = pygame.sprite.spritecollide(self.jogador, self.itens, True)
            for item in colisoes_itens:
                if isinstance(item, Moeda):
                    self.som_moeda.play()
                    self.moedas_coletadas_jogador += 1
                if isinstance(item, Coracao):
                    self.som_vida.play()
                    self.jogador.vida = JOGADOR_VIDA_MAXIMA
                    self.vidas_jogador += 1
                    self.coracoes_coletados.add(item.id_item)
                if isinstance(item, Botas):
                    self.som_bota.play()
                    self.jogador.tem_pulo_duplo = True
                if isinstance(item, Bau):
                    self.jogando = False
                    self.estado_jogo = 'tela_final'
        if self.jogador.vida <= 0 and not self.jogador.morrendo:
            self.jogador.morrendo = True
            self.vidas_jogador -= 1
            self.momento_morte_animada = pygame.time.get_ticks()

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
        if hasattr(self, 'imagem_coracao_hud'):
            rect_icone_vida = self.imagem_coracao_hud.get_rect(topleft=(20, pos_y_icone_vida))
            self.tela.blit(self.imagem_coracao_hud, rect_icone_vida)
        else:
            rect_icone_vida = pygame.Rect(20, pos_y_icone_vida, 25, 25)
            pygame.draw.rect(self.tela, VERMELHO_ESCURO, rect_icone_vida)
        texto_vidas = self.fonte_hud.render(f'x {self.vidas_jogador}', True, BRANCO)
        rect_texto_vidas = texto_vidas.get_rect(midleft=(rect_icone_vida.right + 10, rect_icone_vida.centery))
        self.tela.blit(texto_vidas, rect_texto_vidas)
        pos_icone_moeda = (LARGURA_TELA - 100, 35)
        rect_icone_moeda = self.imagem_moeda_hud.get_rect(center=pos_icone_moeda)
        self.tela.blit(self.imagem_moeda_hud, rect_icone_moeda)
        texto_moedas = self.fonte_hud.render(f'x {self.moedas_coletadas_jogador}', True, BRANCO)
        rect_texto_moedas = texto_moedas.get_rect(midleft=(rect_icone_moeda.right + 10, rect_icone_moeda.centery))
        self.tela.blit(texto_moedas, rect_texto_moedas)
        if self.jogador.tem_pulo_duplo:
            rect_bota = self.imagem_bota_hud.get_rect(center=(pos_icone_moeda[0], pos_icone_moeda[1] + 50))
            self.tela.blit(self.imagem_bota_hud, rect_bota)
        if self.modo_debug:
            pos_texto = f"Pos: ({int(self.jogador.rect.x)}, {int(self.jogador.rect.y)})"
            texto_pos = self.fonte_hud.render(pos_texto, True, BRANCO)
            rect_pos = texto_pos.get_rect(bottomleft=(10, ALTURA_TELA - 10))
            self.tela.blit(texto_pos, rect_pos)
            texto_debug = self.fonte_hud.render("MODO DEBUG", True, VERMELHO)
            rect_debug = texto_debug.get_rect(center=(LARGURA_TELA / 2, 25))
            self.tela.blit(texto_debug, rect_debug)

    def desenhar_jogo(self):
        self.tela.blit(self.imagem_fundo, (0,0))
        for sprite in self.todos_os_sprites:
            self.tela.blit(sprite.image, self.camera.aplicar(sprite))
        self.desenhar_hud()
        pygame.display.flip()

    def mostrar_menu_principal(self):
        self.tela.fill(PRETO)
        texto_titulo = self.fonte_titulo.render(NOME_JOGO, True, VERMELHO)
        rect_titulo = texto_titulo.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 4))
        self.tela.blit(texto_titulo, rect_titulo)
        
        largura_botao = 200 * 1.2
        altura_botao = 50 * 1.2
        espacamento = 20

        botao_jogar = pygame.Rect(LARGURA_TELA/2 - largura_botao/2, ALTURA_TELA * 0.5, largura_botao, altura_botao)
        botao_creditos = pygame.Rect(LARGURA_TELA/2 - largura_botao/2, botao_jogar.bottom + espacamento, largura_botao, altura_botao)
        botao_sair = pygame.Rect(LARGURA_TELA/2 - largura_botao/2, botao_creditos.bottom + espacamento, largura_botao, altura_botao)

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
                        esperando = False

    def mostrar_creditos(self):
        self.tela.fill(PRETO)
        criadores = [CRIADOR_1, CRIADOR_2, CRIADOR_3, CRIADOR_4, CRIADOR_5, CRIADOR_6]
        for i, nome in enumerate(criadores):
            texto_criador = self.fonte_hud.render(nome, True, CINZA)
            rect_criador = texto_criador.get_rect(left=50, top=100 + i * 50)
            self.tela.blit(texto_criador, rect_criador)
        
        largura_botao = 200 * 1.2
        altura_botao = 50 * 1.2
        espacamento = 20
        
        botao_jogar = pygame.Rect(LARGURA_TELA * 0.7 - largura_botao/2, ALTURA_TELA * 0.5, largura_botao, altura_botao)
        botao_voltar = pygame.Rect(LARGURA_TELA * 0.7 - largura_botao/2, botao_jogar.bottom + espacamento, largura_botao, altura_botao)

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
            pygame.time.wait(2000)
            self.resetar_jogo()
            self.estado_jogo = 'menu_principal'

    def mostrar_tela_final(self):
        self.tela.fill(PRETO)
        pontuacao = (self.vidas_jogador * 1250) + (self.moedas_coletadas_jogador * 120)
        
        texto_parabens = self.fonte_titulo.render("Parabéns por terminar o jogo!", True, AMARELO)
        rect_parabens = texto_parabens.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA * 0.3))
        self.tela.blit(texto_parabens, rect_parabens)
        
        texto_pontuacao = self.fonte_menu.render(f"Sua pontuação foi: {pontuacao}", True, VERMELHO)
        rect_pontuacao = texto_pontuacao.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA * 0.5))
        self.tela.blit(texto_pontuacao, rect_pontuacao)
        
        texto_agradecimento = self.fonte_hud.render("Esperamos que tenha gostado desse joguinho, fizemos com nosso amor e suor!", True, VERDE)
        rect_agradecimento = texto_agradecimento.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA * 0.7))
        self.tela.blit(texto_agradecimento, rect_agradecimento)

        pygame.display.flip()
        pygame.time.wait(10000) # Espera 1 minuto
        self.resetar_jogo()
        self.estado_jogo = 'menu_principal'

    def resetar_jogo(self):
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
    elif g.estado_jogo == 'tela_final':
        g.mostrar_tela_final()

pygame.quit()
sys.exit()