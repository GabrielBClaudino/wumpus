import numpy as np
import time 
import os
import random
import threading as th

# O 1 é o Robô
# O @ é a Saída

TemMapa = False

# INSIRA A COORDENADA DO PLAYER
# x: 0 Y: 0 É O CANTO SUPERIOR ESQUERDO
posicaoXInicio = 0
posicaoYInicio = 0

posicaoXMapa = 1
posicaoYMapa = 1

Mapa = [
    ["1", ".", ".", ".", ".", ".", ".", "@"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "@"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "@"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."]
]

# Insira a coordenada da saída
posicaoXFinal = 7
posicaoYFinal = 7

posicaoXArmadilha = 0
posicaoYArmadilha = 0

Historico = []

def criar_mapa():
    global posicaoXFinal, posicaoYFinal, posicaoXArmadilha, posicaoYArmadilha, posicaoXMapa, posicaoYMapa
    
    DefinirBau = {
        "1": (7, 0), 
        "2": (7, 2),  
        "3": (7, 4)
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
            if pedras == 3:  # Limitar a 3 pedras
                break
            
            if random.choice([1, 0]) == 1:  # Aleatoriamente decide se adiciona uma pedra
                chave = f"x{i}y{j}"
                valores = [i, j, i, j + 1, i + 1, j, i + 1, j + 1]  # bloco 2x2
                
                # Coordenadas do playerSpawn e baús
                posicoes_proibidas = {
                    (0, 0), (0, 1), (1, 0), (1, 1),  # playerSpawn
                    (6, 0), (6, 1), (7, 0), (7, 1),  # bau1
                    (6, 2), (6, 3), (7, 2), (7, 4),  # bau2
                    (6, 4), (6, 5), (7, 4), (7, 5)   # bau3
                }
                for pedra in pedrapos.values():
                    for k in range(0, len(pedra), 2):
                        posicoes_proibidas.add((pedra[k], pedra[k + 1]))
                
                # Verificar se o bloco não está em cima das posições predefinidas
                if not any((valores[k], valores[k + 1]) in posicoes_proibidas for k in range(0, len(valores), 2)):
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
        if Mapa[posicaoYMapa][posicaoXMapa] == ".":
            Mapa[posicaoYMapa][posicaoXMapa] = "8" 
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


    bau1X = 7  
    bau1Y = 0

    bau2X = 7  
    bau2Y = 2

    bau3X = 7 
    bau3Y = 4
    posicaoX = posicaoXInicio
    posicaoY = posicaoYInicio

    Mapa[posicaoY][posicaoX] = 1
    Mapa[bau1Y][bau1X] = "@"
    Mapa[bau2Y][bau2X] = "@"
    Mapa[bau3Y][bau3X] = "@"

    if TemMapa == False:
        Mapa[posicaoYMapa][posicaoXMapa] = "8"

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
            "D": (1, 0, ">"), 
            "A": (-1, 0, "<"), 
            "S": (0, 1, "V"), 
            "W": (0, -1, "^")}

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
                    elif Mapa[novoY][novoX] == "@":
                        Mapa[posicaoY][posicaoX] = Caminho
                        posicaoX, posicaoY = novoX, novoY
                        Mapa[posicaoY][posicaoX] = 1
                        
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
    global posicaoX, posicaoY, posicaoXFinal, posicaoYFinal, posicaoXMapa, posicaoYMapa, Mapa
    
    # Distância do node Principal para o final
    print("Mapa:", posicaoXMapa, "y:", posicaoYMapa)
    if TemMapa == True:
        print("Com Mapa")
        hx = abs(posicaoXFinal - posicaoX)
        hy = abs(posicaoYFinal - posicaoY)
        h = hx + hy
    else:
        print("Sem Mapa")
        hx = abs(posicaoXMapa - posicaoX)
        hy = abs(posicaoYMapa - posicaoY)
        h = hx + hy
    
    '''
    Esse algoritmo usa como base o A* porém não com todas as funcionalidades
    pois não temos o valor de G.
    
    O valor que usamos é a soma da distância do node vizinho com o player até o final do labirinto.
    e.g:

    DISTANCIA = DISTANCIA_ATÉ_FINAL + NODE_DISTANCIA_ATÉ_FINAL

    O código então, escolhe o node com menor F pois a distância até o final teoricamente iria levar até o final do labirinto pela menor distância possível.
    
    Algumas regras extras foram adicionadas para melhorar como o algoritmo funciona:
            
            °- Paredes ou borda do mapa ou qualquer coisa que não seja "." setam o F = 99999999 assim o código considera esse NODE um obstáculo.

            °- O caminho passado pelo player, no caso o rastro "0", é considerado 9999999 assim evitando que o algoritmo considere um lugar que ele já passou
            
            °- Se o Player ficar preso, o código retorna o "NÃO ACHEI" como direção, o que irá reiniciar o código e colocar um X na posição que ele travou, de modo que ele vai lentamente desconsiderar locais sem saída.

               e.g:
                    Mapa:
                        ['0' 'X' 'X' '█' 'X' 'X']
                        ['0' '0' 'X' 'X' 'X' 'X']
                        ['█' '0' '█' '█' '█' 'X']
                        ['X' '0' '█' '@' '█' 'X']
                        ['█' '0' '█' '1' '█' 'X']
                        ['.' '0' '0' '0' '█' 'X']

            °- Como não podemos andar na diagonal, temos que verificar se o Node PAI é atravessavel, assim podemos ir para o Node FILHO
                
                MAPA DE NODES:
                    FILHO    PAI   FILHO
                    [NODE1][NODE2][NODE3]
                PAI [NODE4][     ][NODE5]PAI
                    [NODE6][NODE7][NODE8]
                    FILHO    PAI   FILHO

    '''

    # Adicionamos as coordenadas dos nodes ortogonais:
    NODE1 = [posicaoX - 1, posicaoY - 1,0,1]
    NODE2 = [posicaoX    , posicaoY - 1,0,None]
    NODE3 = [posicaoX + 1, posicaoY - 1,0,1]

    
    NODE4 = [posicaoX - 1, posicaoY,0,None]
    NODE5 = [posicaoX + 1, posicaoY,0,None]

    NODE6 = [posicaoX - 1, posicaoY + 1,0,6]
    NODE7 = [posicaoX    , posicaoY + 1,0,None]
    NODE8 = [posicaoX + 1, posicaoY + 1,0,6]

    NODES = [NODE1,NODE2,NODE3,NODE4,NODE5,NODE6,NODE7,NODE8]

    # Agora descobrimos o valor de f para cada node vizinho do player
    for i, NODE in enumerate(NODES):
        try:
            if 0 <= NODE[1] < len(Mapa) and 0 <= NODE[0] < len(Mapa[0]):
                if Mapa[NODE[1]][NODE[0]] == "." or Mapa[NODE[1]][NODE[0]] == "@" or Mapa[NODE[1]][NODE[0]] == "8":  # Caminho livre


                    if TemMapa == True:
                        NODEhx = abs(posicaoXFinal - NODE[0])
                        NODEhy = abs(posicaoYFinal - NODE[1])
                        NODEh = NODEhx + NODEhy
                    else:
                        NODEhx = abs(posicaoXMapa - NODE[0])
                        NODEhy = abs(posicaoYMapa - NODE[1])
                        NODEh = NODEhx + NODEhy

                    distancia = h + NODEh
                    NODE[2] = distancia
                elif posicaoXArmadilha == NODE[0] and posicaoXArmadilha == NODE[1]:
                    NODE[2] = 999999999999  # Obstáculo
                else: 
                    NODE[2] = 999999999999  # Obstáculo
            else:  
                NODE[2] = 999999999999  # Fora dos limites do mapa
        
        except IndexError:  # Caso seja fora dos limites do mapa
            NODE[2] = 999999999999

        print("Node ", i + 1, " :", NODE)
    
    # Encontrar o node com menor valor de f
    MENOR = None
    for i, NODE in enumerate(NODES):

        #VERIFICA SE O NODE PAI É ATRAVESSAVEL SE NÃO, O NODE FILHO NÃO É ATRAVESSAVEL TAMBÉM
        if NODE[3] is not None:
            node_pai = NODES[NODE[3]]
            if node_pai[2] == 999999999999:
                NODE[2] = 999999999999


        
        #acha o menor F
        if MENOR is not None and NODE[2] == MENOR[2]:
            MENOR = NODE
            direcaoNUM = i + 1

        if MENOR is None or NODE[2] < MENOR[2]:
            MENOR = NODE
            direcaoNUM = i + 1
        
        #se todos os nodes não são atravessaveis retorne None
        if all(node[2] == 999999999999 for node in NODES):
            direcaoNUM = None


    direcao = {
        # Travei!
        0: "NaoAchei",  
        None : "NaoAchei"
    }

    print("Node menor:", MENOR)
    direcao[1] = "W"
    direcao[2] = "W"
    direcao[3] = "W"
    direcao[4] = "A"
    direcao[5] = "D"
    direcao[6] = "S"
    direcao[7] = "S"
    direcao[8] = "S"

    # Caso DirecaoNum retornar vazio (significando que não existe nenhum caminho naquele node a gente retorna o "Nao achei")
    try:
        return direcao[direcaoNUM]
    except UnboundLocalError:        
        return direcao[0]



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
        print("Caminho usado:")
        print(Historico)


