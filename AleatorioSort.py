import numpy as np
import time 
import os
import random
import threading as th
#o 1 é o Robô
#O @ é a Saída

TemMapa = False

#INSIRA A COORDENADA DO PLAYER
#x: 0 Y: 0 É O CANTO SUPERIOR ESQUERDO
posicaoXInicio = 0
posicaoYInicio = 0


posicaoXMapa = 1
posicaoYMapa = 1

#Posicao Real time


Mapa =[ ["1",".",".",".",".","@"],
        [".",".",".",".",".","."],
        [".",".",".",".",".","@"],
        [".",".",".",".",".","."],
        [".",".",".",".",".","@"],
        [".",".",".",".",".","."]]

#Insira a coodenada da saída
#5 5 É O CANTO INFERIOR DIREITO
posicaoXFinal =  0
posicaoYFinal =  0

posicaoXArmadilha =  0
posicaoYArmadilha =  0





Historico = []
import random

def criar_mapa():
    global posicaoXFinal, posicaoYFinal, posicaoXArmadilha, posicaoYArmadilha,posicaoXMapa,posicaoYMapa
    
    DefinirBau = {
        "1": (5, 0), 
        "2": (5, 2), 
        "3": (5, 4)
    }
    
    objetos = ["Tesouro", "Armadilha", "Nada"]
    for bau in DefinirBau:
        objeto = random.choice(objetos)  
        DefinirBau[bau] = (DefinirBau[bau][0], DefinirBau[bau][1], objeto) 
        objetos.remove(objeto)
    
    for bau, (x, y, tipo) in DefinirBau.items():
        if tipo == "Tesouro":
            posicaoXFinal, posicaoYFinal = x, y
        elif tipo == "Armadilha":
            posicaoXArmadilha, posicaoYArmadilha = x, y

    # Adicionando pedras
    pedrapos = {}
    pedras = 0
    for i in range(len(Mapa) - 1):
        for j in range(len(Mapa[i]) - 1): 
            if pedras >= 3:  # Limitar a 3 pedras
                break
            
            if random.choice([1, 0]) == 1:  # Aleatoriamente decide se adiciona uma pedra
                chave = f"x{i}y{j}"
                valores = [i, j, i, j + 1, i + 1, j, i + 1, j + 1]  # bloco 2x2
                
                # Coordenadas do playerSpawn e baús
                posicoes_proibidas = {
                    (0, 0), (0, 1), (1, 0), (1, 1),  # playerSpawn
                    (4, 0), (4, 1), (5, 0), (5, 1),  # bau1
                    (4, 2), (4, 3), (5, 2), (5, 4),  # bau2
                    (4, 4), (4, 5), (5, 4), (5, 5)   # bau3
                }
                
                # Verificar se o bloco não está em cima das posições predefinidas
                if not any((valores[k], valores[k+1]) in posicoes_proibidas for k in range(0, len(valores), 2)):
                    pedrapos[chave] = valores
                    pedras += 1 

    # Atualiza o mapa com as pedras
    for valores in pedrapos.values():

        for k in range(0, len(valores), 2):
            x, y = valores[k], valores[k + 1]
            if 0 <= y < len(Mapa) and 0 <= x < len(Mapa[0]):
                Mapa[y][x] = "█"  # Adiciona a pedra ao mapa
    
    #adicionar mapa

    mapa_adicionado = False
    while not mapa_adicionado:
        posicaoXMapa = random.randint(0, len(Mapa) - 1)
        posicaoYMapa = random.randint(0, len(Mapa[0]) - 1)
        
        # Verifica se a posição está livre
        if Mapa[posicaoYMapa][ posicaoXMapa] == ".":
            Mapa[posicaoYMapa][ posicaoXMapa] = "8" 
            mapa_adicionado = True  

    #adicionar monstro
    monstro_adicionado = False
    monstros = 0
    while not monstro_adicionado:
        # Verifica se a posição está livre
        monstroX = random.randint(0, len(Mapa) - 1)
        monstroY = random.randint(0, len(Mapa[0]) - 1)
        
        if Mapa[monstroY][monstroX] == ".":
            Mapa[monstroY][monstroX] = "M"  # Adiciona o marcador
            monstros += 1
        if monstros == 3:
            monstro_adicionado = True  # Marca que o mapa foi adicionado
                



                        
                        

                

criar_mapa()

def adicionarPlayer():
    bau1X = 5
    bau1Y = 0

    bau2Y = 2
    bau2X = 5

    bau3Y = 4
    bau3X = 5

    posicaoX = posicaoXInicio
    posicaoY = posicaoYInicio

    Mapa[posicaoY][posicaoX]= 1
    Mapa[bau1Y ][bau1X]= "@"
    Mapa[bau2Y][bau2X]= "@"
    Mapa[bau3Y][bau3X]= "@"

    if TemMapa == False:
        Mapa[posicaoYMapa][posicaoXMapa]= "8"
    


    return posicaoX, posicaoY


posicaoX, posicaoY = adicionarPlayer()


'''
Mapa =[ ["█","█","█","█","█","█"],
        [".",".",".",".",".","█"],
        ["█",".","█",".","█","█"],
        [".",".","█",".",".","."],
        ["█","█","█",".","█","."],
        [".",".",".",".","█","."]]
'''

'''
Mapa = [[".",".",".",".",".","."],
        ["█","█","█","█","█","."],
        [".",".",".",".",".","."],
        [".","█",".","█","█","█"],
        [".","█",".",".",".","█"],
        [".","█",".","█",".","."]]
        
'''
'''
Mapa = [[".",".",".",".",".","."],
        [".",".",".",".",".","."],
        [".",".",".",".",".","."],
        [".",".",".",".",".","."],
        [".",".",".",".",".","."],
        [".",".",".",".",".","."]]
'''

'''
Mapa = [[".","█",".",".",".","."],
        [".",".",".",".",".","."],
        ["█","█",".",".","█","█"],
        [".",".",".",".",".","."],
        [".",".",".",".","█","."],
        [".",".",".",".","█","."]]
        
'''




tempo = 0
passos = 0

Morreu = False

def andar(direcao, posicaoX, posicaoY):
    global Morreu, TemMapa, posicaoXInicio, posicaoYInicio, posicaoXMapa, posicaoYMapa, posicaoXFinal, posicaoYFinal, posicaoXArmadilha, posicaoYArmadilha

    if direcao == "NaoAchei":
        # Apaga o caminho feito pelo player
        for y in range(len(Mapa)):
            for x in range(len(Mapa[y])):
                if Mapa[y][x] != "█" and Mapa[y][x] != "X" and Mapa[y][x] != "M":
                    Mapa[y][x] = "."
        
        # Guarda o local onde o player travou e torna intransitável
        Mapa[posicaoY][posicaoX] = "X"

        # Limpa o histórico e reinicia o player
        Historico.clear()
        posicaoX, posicaoY = adicionarPlayer()

    else:
        movimentos = {
            "D": (1, 0, "."), 
            "A": (-1, 0, "."), 
            "S": (0, 1, "."), 
            "W": (0, -1, ".")}

        for mov in direcao.split(","):
            mov = mov.upper()
            if mov in movimentos:
                dx, dy,Caminho = movimentos[mov]
                novoX, novoY = posicaoX + dx, posicaoY + dy
                if 0 <= novoX < len(Mapa[0]) and 0 <= novoY < len(Mapa):
                    if Mapa[novoY][novoX] == "@" and novoX == posicaoXFinal and novoY == posicaoYFinal:
                        return posicaoX, posicaoY, False,TemMapa
                    elif  Mapa[novoY][novoX] == "@" and novoX == posicaoXArmadilha and novoY == posicaoYArmadilha:
                        Morreu = True

                        return posicaoX, posicaoY, False,TemMapa
                        
                    if Mapa[novoY][novoX] == "8":
                        TemMapa = True
                        Mapa[posicaoY][posicaoX] = "."
                        posicaoX, posicaoY = novoX, novoY
                        Mapa[posicaoY][posicaoX] = 1


                        posicaoXInicio = posicaoXMapa
                        posicaoYInicio = posicaoYMapa

                        for y in range(len(Mapa)):
                            for x in range(len(Mapa[y])):
                                if Mapa[y][x] != "█" and Mapa[y][x] != "@" and Mapa[y][x] != "M":
                                    Mapa[y][x] = "."
                        posicaoX, posicaoY = adicionarPlayer()

                    if Mapa[novoY][novoX] in ["."]:
                        Mapa[posicaoY][posicaoX] = Caminho
                        posicaoX, posicaoY = novoX, novoY
                        Mapa[posicaoY][posicaoX] = 1

    return posicaoX, posicaoY, True, TemMapa


# path finding de verdade
def pathfinding():
    direcao = {}
    direcao[1] = "W,A"
    direcao[2] = "W"
    direcao[3] = "W,D"
    direcao[4] = "A"
    direcao[5] = "D"
    direcao[6] = "S,A"
    direcao[7] = "S"
    direcao[8] = "S,D"

    direcaoNUM = random.choice(range(1,8))
    return direcao[direcaoNUM]



def jogar():
    
    
    global tempo, passos, update
    update = True
    global posicaoX, posicaoY
    while update:
        os.system('cls' if os.name == 'nt' else 'clear')  
        
        print("Mapa:")
        print(np.matrix(Mapa))  
        direcao = pathfinding()
        
        
        print("X:", posicaoX)
        print("Y:", posicaoY)    
        print("Direcao: ", direcao)
        print("Tempo: ", tempo, "Segundos")
        print("Passos (teclas apertadas): ", passos)
        
        

        time.sleep(0.1)

        tempo += 0.1
        Historico.append(direcao)
        posicaoX, posicaoY, update,TemMapa = andar(direcao, posicaoX, posicaoY)  
        
        
        passos += 1


update = False
if update == False:
    
    jogar()
    
    if Morreu == True:
         print("VOCÊ MORREU!")
    else:
        print("Tempo: ", tempo)
        print("Você Achou o Tesouro!")


