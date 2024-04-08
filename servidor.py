import socket
from _thread import *
import sys


servidor = '192.168.74.1'
porta = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor_ip = socket.gethostbyname(servidor)

try:
    s.bind((servidor, porta))

except socket.error as e:
    print(str(e))

s.listen(2)
print("[INFO]: Servidor iniciado, esperando por conexão")

ID_atual = "0"
pos = ["0:50,50", "1:100,100"]

def threaded_client(conexao):
    global ID_atual, pos
    conexao.send(str.encode(ID_atual))
    ID_atual = "1"
    resposta = ''
    while True:
        try:
            dados = conexao.recv(2048)
            resposta = dados.decode('utf-8')
            if not dados:
                conexao.send(str.encode("[INFO]: ", endereco, "desconectado."))
                break
            else:
                print("Recebido: " + resposta)
                vetor = resposta.split(":")
                id = int(vetor[0])
                pos[id] = resposta

                if id == 0: nid = 1
                if id == 1: nid = 0

                resposta = pos[nid][:]
                print("Enviando: " + resposta)

            conexao.sendall(str.encode(resposta))
        except:
            break

    print("Conexão perdida com o jogador")
    conexao.close()

while True:
    conexao, endereco = s.accept()
    print("[INFO]: ", endereco, "conectado.")

    start_new_thread(threaded_client, (conexao,))
