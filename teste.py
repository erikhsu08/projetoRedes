import pygame
import socket
import threading


#Trechos relacionado às configurações de rede
class Network:
    def __init__(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "192.168.15.30" 
        self.porta = 5555
        self.endereco = (self.host, self.porta)
        self.id = self.connect()


    def connect(self):
        self.cliente.connect(self.endereco)
        return self.cliente.recv(2048).decode()

    def send(self, dados):
        try:
            self.cliente.send(str.encode(dados))
            reposta = self.cliente.recv(2048).decode()
            return reposta
        except socket.error as e:
            return str(e)
        
    def send_victory(self, winner):
        try:
            self.cliente.send(str.encode("WINNER: " + winner))
        except socket.error as e:
            return str(e)
        

#Classe dos jogadores
class Jogador():
    largura = altura = 50

    def __init__(self, InicioX, InicioY, cor):
        self.x = InicioX
        self.y = InicioY
        self.velocidade = 2
        self.cor = cor

    def draw(self, g):
        pygame.draw.rect(g, self.cor, (self.x, self.y, self.largura, self.altura), 0)

    def move(self, dirn):
        if dirn == 0:
            self.x += self.velocidade
        elif dirn == 1:
            self.x -= self.velocidade
        elif dirn == 2:
            self.y -= self.velocidade
        else:
            self.y += self.velocidade

#Classe jogo
class Jogo:
    def __init__(self, w, h):
        self.net = Network()
        self.largura = w
        self.altura = h
        self.Jogador = Jogador(15, 100, (0,0,255))  #Posições iniciais e cores dos jogadores
        self.Jogador2 = Jogador(22,100, (255, 0, 0)) #Posições iniciais e cores dos jogadores
        self.canvas = Canvas(self.largura, self.altura, "Corrida no Labirinto")
        self.linha_chegada_atingida = False
        self.jogador_vencedor = None
        

        self.obstaculos = [
            #(X, Y, LARGURA, ALTURA)
            #Bordas da tela
            pygame.Rect(0, 0, 800, 20), # borda de cima
            pygame.Rect(0, 780, 800, 20), # borda de baixo
            pygame.Rect(0, 0, 15, 780), # borda da esquerda
            pygame.Rect(780, 0, 20, 580), #borda da direita 1
            pygame.Rect(780, 630, 20, 400),#borda da direita 2
            
            #Labirinto
            pygame.Rect(67, 80, 133, 20),
            pygame.Rect(180, 80, 20, 100),
            pygame.Rect(145, 180, 55, 20),
            pygame.Rect(67, 150, 20, 350),
            pygame.Rect(0, 380, 87, 20),
            pygame.Rect(67, 480, 98, 20),
            pygame.Rect(145, 180, 20, 150),
            pygame.Rect(145, 380, 20, 100),
            pygame.Rect(145, 310, 80, 20),
            pygame.Rect(220, 250, 20, 170),
            pygame.Rect(0, 600, 87, 20),
            pygame.Rect(67, 560, 20, 60),
            pygame.Rect(67, 560, 330, 20),
            pygame.Rect(300, 250, 20, 330),
            pygame.Rect(220, 480, 100, 20),
            pygame.Rect(300, 250, 120, 20),
            pygame.Rect(300, 200, 70, 20),
            pygame.Rect(350, 150, 20, 50),
            pygame.Rect(250, 0, 20, 120),
            pygame.Rect(200, 120, 70, 20),
            pygame.Rect(250, 60, 150, 20),
            pygame.Rect(620, 0, 20, 110),
            pygame.Rect(470 , 60, 170, 20),
            pygame.Rect(350, 140, 120, 20),
            pygame.Rect(470, 140, 20, 60),
            pygame.Rect(420, 200, 70, 20),
            pygame.Rect(420, 200, 20, 70),
            pygame.Rect(550, 170, 20, 160),
            pygame.Rect(300, 310, 250, 20),
            pygame.Rect(700, 100, 20, 400),
            pygame.Rect(700, 400, 80, 20),
            pygame.Rect(620, 170, 20, 230),
            pygame.Rect(550, 380, 170, 20),
            pygame.Rect(550, 380, 20, 80),
            pygame.Rect(470, 450, 100, 20),
            pygame.Rect(470, 310, 20, 70),
            pygame.Rect(380, 310, 20, 100),
            pygame.Rect(380, 480, 20, 150),
            pygame.Rect(470, 450, 20, 130),
            pygame.Rect(470, 620, 20, 80),
            pygame.Rect(490, 560, 80, 20),
            pygame.Rect(550, 560, 20, 120),
            pygame.Rect(280, 680, 290, 20),
            pygame.Rect(280, 650, 20, 40),
            pygame.Rect(190, 630, 110, 20),
            pygame.Rect(120, 580, 20, 70),
            pygame.Rect(190, 630, 20, 100),
            pygame.Rect(70, 710, 120, 20),
            pygame.Rect(280, 760, 20, 20),
            pygame.Rect(450, 760, 20, 20),
            pygame.Rect(360, 700, 20, 20),
            pygame.Rect(550, 700, 20, 20),
            pygame.Rect(620, 470, 20, 250),
            pygame.Rect(620, 700, 100, 20),
            pygame.Rect(700, 630, 20, 70),
            pygame.Rect(700, 630, 80, 20),
            pygame.Rect(700, 560, 80, 20)
            ]

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            tecla = pygame.key.get_pressed()

            if tecla[pygame.K_RIGHT]:
                if self.Jogador.x <= self.largura - self.Jogador.velocidade:
                    self.Jogador.move(0)

            if tecla[pygame.K_LEFT]:
                if self.Jogador.x >= self.Jogador.velocidade:
                    self.Jogador.move(1)

            if tecla[pygame.K_UP]:
                if self.Jogador.y >= self.Jogador.velocidade:
                    self.Jogador.move(2)

            if tecla[pygame.K_DOWN]:
                if self.Jogador.y <= self.altura - self.Jogador.velocidade:
                    self.Jogador.move(3)

            #Colisao com a linha de chegada
            if self.Jogador.x + self.Jogador.largura >= 778 and self.Jogador.y + self.Jogador.altura >= 580:
                if not self.linha_chegada_atingida:
                    self.linha_chegada_atingida = True
                    self.jogador_vencedor = self.Jogador
            
            #Colisao com o labirinto
            for obstaculo in self.obstaculos:
                margem = 10
                retangulo_colisao = obstaculo.inflate(-margem, -margem)
                pygame.draw.rect(self.canvas.get_canvas(), (255, 0, 0), obstaculo)
                
                if retangulo_colisao.colliderect(pygame.Rect(self.Jogador.x, self.Jogador.y, self.Jogador.largura, self.Jogador.altura)):
                    #Mova o jogador de volta à posição inicial
                    self.Jogador.x = 20 
                    self.Jogador.y = 100

            
            #Enviar dados
            self.Jogador2.x, self.Jogador2.y = self.parse_dados(self.send_dados())

            #Atualizar Canvas
            self.canvas.draw_background()
            self.Jogador.draw(self.canvas.get_canvas())
            self.Jogador2.draw(self.canvas.get_canvas())
            self.draw()


            if self.linha_chegada_atingida:
                self.mostrar_msg_vitoria(self.jogador_vencedor)
                self.net.send_victory(self.obter_cor_jogador(self.jogador_vencedor))

            self.canvas.update()

        pygame.quit()


    def mostrar_msg_vitoria(self, jogador):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", 50)
        mensagem = f"Jogador {self.obter_cor_jogador(jogador)} Venceu!"
        render = font.render(mensagem, True, (0, 255, 0))

        # Posicionar mensagem no centro da tela
        largura_texto = render.get_width()
        altura_texto = render.get_height()
        x_texto = (self.largura - largura_texto) // 2
        y_texto = (self.altura - altura_texto) // 2
        
        self.canvas.get_canvas().blit(render, (x_texto, y_texto))

    def obter_cor_jogador(self, jogador):
        if jogador == self.Jogador:
            return "1"
        elif jogador == self.Jogador2:
            return "2"
        else:
            return ""
        

    def send_dados(self):
        dados = str(self.net.id) + ":" + str(self.Jogador.x) + "," + str(self.Jogador.y)
        reposta = self.net.send(dados)
        return reposta

    @staticmethod
    def parse_dados(dados):
        try:
            d = dados.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0
        
    def draw_linha_chegada(self):
        pygame.draw.rect(self.canvas.get_canvas(), (0,0,0), self.linha_chegada)

    def draw(self):
        #Linha de Chegada
        pygame.draw.rect(self.canvas.get_canvas(), (0,255,0), (778, 580, 40, 50))

        for obstaculo in self.obstaculos:
            pygame.draw.rect(self.canvas.get_canvas(), (0, 0, 0), obstaculo)

#Classe canvas
class Canvas:
    def __init__(self, l, a, nome="None"):
        self.largura = l
        self.altura = a
        self.tela = pygame.display.set_mode((l,a))
        pygame.display.set_caption(nome)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_texto(self, texto, tam, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", tam)
        render = font.render(texto, 1, (0,0,0))

        self.tela.draw(render, (x,y))

    def get_canvas(self):
        return self.tela

    def draw_background(self):
        self.tela.fill((255,255,255))


#Iniciar jogo
if __name__ == "__main__":
    jogo = Jogo(800,800)
    jogo.run()
