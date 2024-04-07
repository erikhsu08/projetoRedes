import pygame
import socket


#Constantes e variáveis
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)

LARGURA = 600
ALTURA = 600

pygame.init()
fonte_jogo = pygame.font.SysFont('Arial', 40)

delay = 30

velocidade_raquete = 20
largura_raquete = 10
altura_raquete = 100

#Posição incial de P1
p1_x_pos = 10
p1_y_pos = ALTURA / 2 - altura_raquete / 2

#Posição incial de P2
p2_x_pos = LARGURA - largura_raquete - 10
p2_y_pos = ALTURA / 2 - altura_raquete / 2

p1_pontos = 0
p2_pontos = 0

p1_up = False
p1_down = False
p2_up = False
p2_down = False

bola_x_pos = LARGURA / 2
bola_y_pos = ALTURA / 2
largura_bola =  8
bola_x_velocidade  = -10
bola_y_velocidade = 0

tela = pygame.display.set_mode((LARGURA, ALTURA))

class Network:
    def __init__(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor = "192.168.74.1"
        self.porta = 5555
        self.endereco = (self.servidor, self.porta)
        self.pos = self.conectado()

    def getPos(self):
        return self.pos
    
    def conectado(self):
        try:
            self.cliente.connect(self.endereco)
            return self.cliente.recv(2048).decode()
        except:
            pass
    
    def send(self, dados):
        try:
            self.cliente.send(str.encode(dados))
            return self.cliente.recv(2048).decode()
        except socket.error as e:
            print(e)

def desenha_objetos():
    pygame.draw.rect(tela, VERMELHO, (int(p1_x_pos), int(p1_y_pos), largura_raquete, altura_raquete))
    pygame.draw.rect(tela, AZUL, (int(p2_x_pos), int(p2_y_pos), largura_raquete, altura_raquete))
    pygame.draw.circle(tela, BRANCO,  (bola_x_pos, bola_y_pos), largura_bola)
    pontos = fonte_jogo.render(f"{str(p1_pontos)} - {str(p2_pontos)}", False, BRANCO)
    tela.blit(pontos, (260, 50))


def mov_player(jogador):
    global p1_y_pos
    global p2_y_pos

    if jogador == 1:
        if p1_up and p1_y_pos > 0:
            p1_y_pos = max(p1_y_pos - velocidade_raquete, 0)
        elif p1_down and p1_y_pos < ALTURA - altura_raquete:
            p1_y_pos = min(p1_y_pos + velocidade_raquete, ALTURA - altura_raquete)
    elif jogador == 2:
        if p2_up and p2_y_pos > 0:
            p2_y_pos = max(p2_y_pos - velocidade_raquete, 0)
        elif p2_down and p2_y_pos < ALTURA - altura_raquete:
            p2_y_pos = min(p2_y_pos + velocidade_raquete, ALTURA - altura_raquete)    

def mov_bola(): 
    global bola_x_pos
    global bola_y_pos
    global bola_x_velocidade 
    global bola_y_velocidade
    global p1_pontos
    global p2_pontos

    if (bola_x_pos + bola_x_velocidade  < p1_x_pos + largura_raquete) and (p1_y_pos < bola_y_pos + bola_y_velocidade + largura_bola < p1_y_pos + altura_raquete):
        bola_x_velocidade  = -bola_x_velocidade 
        bola_y_velocidade = (p1_y_pos + altura_raquete / 2 - bola_y_pos) / 15
        bola_y_velocidade = -bola_y_velocidade
    
    elif bola_x_pos + bola_x_velocidade < 0:
        p2_pontos += 1
        bola_x_pos = LARGURA / 2
        bola_y_pos = ALTURA / 2
        bola_x_velocidade = 10
        bola_y_velocidade = 0
    
    if (bola_x_pos + bola_x_velocidade > p2_x_pos - largura_raquete) and (p2_y_pos < bola_y_pos + bola_y_velocidade + largura_bola < p2_y_pos + altura_raquete):
        bola_x_velocidade = -bola_x_velocidade
        bola_y_velocidade = (p2_y_pos + altura_raquete / 2 - bola_y_pos) / 15
        bola_y_velocidade = -bola_y_velocidade

    elif bola_x_pos + bola_x_velocidade > ALTURA:
        p1_pontos += 1
        bola_x_pos = LARGURA / 2
        bola_y_pos = ALTURA / 2
        bola_x_velocidade = -10
        bola_y_velocidade = 0

    if (bola_y_pos + bola_y_velocidade > ALTURA or bola_y_pos + bola_y_velocidade < 0):
        bola_y_velocidade = -bola_y_velocidade

    bola_x_pos += bola_x_velocidade
    bola_y_pos += bola_y_velocidade


def pega_pos(posX, posY):
    return f"{posX}, {posY}"

pygame.display.set_caption("Jogo Ping Pong")
tela.fill(PRETO)
pygame.display.flip()

running = True
n = Network()

last_sent_p1_pos = None
last_sent_p2_pos = None

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:
                p1_up = True
            if event.key == pygame.K_s:
                p1_down = True
            if event.key == pygame.K_UP:
                p2_up = True
            if event.key == pygame.K_DOWN:
                p2_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                p1_up = False
            if event.key == pygame.K_s:
                p1_down = False
            if event.key == pygame.K_UP:
                p2_up = False
            if event.key == pygame.K_DOWN:
                p2_down = False

    
    tela.fill(PRETO)
    mov_player(1)
    mov_player(2)
    mov_bola()

    #Obter as pos dos jogadores
    new_p1_pos = pega_pos(p1_x_pos, p1_y_pos)
    if new_p1_pos != last_sent_p1_pos:
        n.send(new_p1_pos)
        last_sent_p1_pos = new_p1_pos
    
    new_p2_pos = pega_pos(p2_x_pos, p2_y_pos)
    if new_p2_pos != last_sent_p2_pos:
        n.send(new_p2_pos)
        last_sent_p2_pos = new_p2_pos
 


    desenha_objetos()
    pygame.display.flip()
    pygame.time.wait(delay)
