import pygame
import socket
import threading

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


class Jogador():
    largura = altura = 50

    def __init__(self, InicioX, InicioY, cor):
        self.x = InicioX
        self.y = InicioY
        self.velocidade = 2
        self.cor = cor

    def draw(self, g):
        pygame.draw.circle(g, self.cor ,(self.x, self.y), self.largura // 5)

    def move(self, dirn):
        if dirn == 0:
            self.x += self.velocidade
        elif dirn == 1:
            self.x -= self.velocidade
        elif dirn == 2:
            self.y -= self.velocidade
        else:
            self.y += self.velocidade


class Jogo:
    def __init__(self, w, h):
        self.net = Network()
        self.largura = w
        self.altura = h
        self.Jogador = Jogador(15, 125, (0,0,255))
        self.Jogador2 = Jogador(50,125, (255, 0, 0))
        self.canvas = Canvas(self.largura, self.altura, "Jogo de Corrida")
        self.linha_chegada = (self.largura - 50, 0, 100, self.altura)
        self.linha_inicio = (self.largura - 100, 8, 98, self.altura)

        self.obstaculos = [
            pygame.Rect(200, 100, 100, 50),
            pygame.Rect(400, 200, 50, 150),
            pygame.Rect(600, 50, 80, 200)
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

            for obstaculo in self.obstaculos:
                margem = 10
                retangulo_colisao = obstaculo.inflate(-margem, -margem)
                pygame.draw.rect(self.canvas.get_canvas(), (255, 0, 0), obstaculo)
                
                if retangulo_colisao.colliderect(pygame.Rect(self.Jogador.x, self.Jogador.y, self.Jogador.largura, self.Jogador.altura)):
                    self.Jogador.x = 15  # Mova o jogador de volta à posição inicial
                    self.Jogador.y = 125


            #Enviar dados
            self.Jogador2.x, self.Jogador2.y = self.parse_dados(self.send_dados())

            #Atualizar Canvas
            self.canvas.draw_background()
            self.canvas.draw_linha_pontilhada((0, self.altura // 2), (self.largura, self.altura // 2), (0, 0, 0))
            self.draw_linha_chegada()
            self.draw_linha_inicio()
            self.Jogador.draw(self.canvas.get_canvas())
            self.Jogador2.draw(self.canvas.get_canvas())
            self.draw()
            self.canvas.update()
            
    
        pygame.quit()

    
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

    def draw_linha_inicio(self):
        iniciox, inicioy, largura, altura = 30, 0, 1, self.altura

        for x in range(iniciox, iniciox + largura, 10):
            pygame.draw.line(self.canvas.get_canvas(), (0,0,0), (x, inicioy), (x, inicioy + altura), 1)

    def draw(self):
        for obstaculo in self.obstaculos:
            pygame.draw.rect(self.canvas.get_canvas(), (0, 0, 0), obstaculo)

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

    def draw_linha_pontilhada(self, pos_comeco, pos_fim, cor, largura = 1, tam_pontilhado = 10):
        x1,y1 = pos_comeco
        x2,y2 = pos_fim
        dx = x2 - x1
        dy = y2 - y1
        distancia = max(abs(dx), abs(dy))
        dx_unidade = dx / distancia
        dy_unidade = dy / distancia
        for i in range(int(distancia / tam_pontilhado)):
            inicio = round(i * tam_pontilhado)
            fim = round((i + 0.5) * tam_pontilhado)
            iniciox = x1 + inicio * dx_unidade
            inicioy = y1 + inicio * dy_unidade
            fimx = x1 + fim * dx_unidade
            fimy = y1 + fim * dy_unidade
            pygame.draw.line(self.tela, cor, (iniciox, inicioy), (fimx, fimy), largura)


#Iniciar jogo
if __name__ == "__main__":
    jogo = Jogo(800,500)
    jogo.run()
