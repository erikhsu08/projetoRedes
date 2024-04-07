import socket 
from _thread import * 
import sys

servidor = "192.168.74.1"
porta = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #usando TCP

try: 
    s.bind((servidor, porta))
except socket.error as e:
    str(e)

s.listen(2) #indica o número de conexões
print("Servidor iniciado: Esperando por uma conexão")

conexoes = []

def cria_pos(posX, posY):
    return str(posX) + "," + str(posY)

def pega_pos(posX, posY):
    return f"{posX}, {posY}"

def enviar_para_todos(dados, cliente_emissor):
    for conexao in conexoes:
        if conexao != cliente_emissor:
            conexao.sendall(dados)

def envia_p_cliente(conexao, dados):
    try: 
        conexao.sendall(dados)
        return True
    except socket.error as e:
        print("[ERRO]: Falha ao enviar dados para o cliente", str(e))
        return False
    
def threaded_client (conexao, jogador):
    global p1_x_pos, p1_y_pos, p2_x_pos, p2_y_pos
    conexao.send(str.encode("Conectado"))
 
    while True:
        try: 
            dados = conexao.recv(2048)
            posicao = dados.decode("utf-8").strip()
            if not dados:
                print("[INFO]:", endereco, "desconectado")
                break
            else:
                print("Posição do jogador ", jogador, ":", posicao)

            #Separar a posição por vírgula e remover espaços em branco
            posicoes = posicao.split(",")
            posicoes = [p.strip() for p in posicoes]

            if jogador == 1:
                p1_x_pos = int(posicoes[0])
                p1_y_pos = int(round(float(posicoes[1])))
            elif jogador == 2:
                p2_x_pos = int(posicoes[0])
                p2_y_pos = int(round(float(posicoes[1])))

                
            envia_p_cliente(conexao, b"Recebido")
            enviar_para_todos(dados,conexao)
        except socket.error as e:
            print("[ERRO]: ", str(e))
            break
        except ValueError as ve:
            print("[ERRO]: Valor inválido para conversão: ", ve)
            break

    print("Conexão perdida com o jogador")
    conexao.close()

jogadorAtual = 1

while True:
    conexao, endereco = s.accept()
    print("[INFO]:", endereco, "conectado")

    #adicionar conexao à lista de conexoes
    conexoes.append(conexao)

    start_new_thread(threaded_client, (conexao, jogadorAtual))
    jogadorAtual += 1
