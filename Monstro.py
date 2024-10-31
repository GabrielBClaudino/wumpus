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

        NODE1 = [posicaoX - 1, posicaoY - 1,0,1]
        NODE2 = [posicaoX    , posicaoY - 1,0,None]
        NODE3 = [posicaoX + 1, posicaoY - 1,0,1]

        
        NODE4 = [posicaoX - 1, posicaoY,0,None]
        NODE5 = [posicaoX + 1, posicaoY,0,None]

        NODE6 = [posicaoX - 1, posicaoY + 1,0,6]
        NODE7 = [posicaoX    , posicaoY + 1,0,None]
        NODE8 = [posicaoX + 1, posicaoY + 1,0,6]

        NODES = [NODE1,NODE2,NODE3,NODE4,NODE5,NODE6,NODE7,NODE8]

        for i in range(len(Mapa) - 1):
            for j in range(len(Mapa[i]) - 1):
                for i, NODE in enumerate(NODES):
                    try:
                        if any((Caminho) in Mapa[NODE[1]][NODE[0]] for Caminho in [">", "V", "^", "<"]):
                            Mapa[NODE[1]][NODE[0]] = "."
                    except IndexError:
                        pass





            

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
def Aleatorio():
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

# path finding de verdade

def pathfinding():
    global posicaoX, posicaoY, posicaoXFinal, posicaoYFinal, posicaoXMapa, posicaoYMapa, Mapa
    
    def contar_monstros_ao_redor(x, y):
        # Começa contagem em zero
        count = 0
        # Verifica as 8 posições ao redor
        # Imagine que você está em uma posição do mapa (X):
        # [ ][ ][ ]
        # [ ][X][ ]
        # [ ][ ][ ]
    
        # dx e dy são deslocamentos para verificar todas as 8 casas ao redor
        # dx = -1 (esquerda), 0 (centro), 1 (direita)
        # dy = -1 (cima), 0 (centro), 1 (baixo)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # Se dx=0 e dy=0, seria a própria posição, então pulamos
                if dx == 0 and dy == 0:
                    continue
                # Calcula nova posição para verificar
                novo_x = x + dx # Posição atual + deslocamento
                novo_y = y + dy # Posição atual + deslocamento
                # Verifica se a nova posição está dentro do mapa
                if 0 <= novo_x < len(Mapa[0]) and 0 <= novo_y < len(Mapa):
                    # Se encontrar um monstro "M", aumenta a contagem
                    if Mapa[novo_y][novo_x] == "M":
                        count += 1
        # Retorna total de monstros encontrados
        return count
        # Exemplo visual de como funciona:
        # Posição atual: X
        # Números: ordem que verifica
        # [1][2][3]
        # [4][X][5]
        # [6][7][8]

    # Define os nós possíveis (mesma estrutura anterior)
    NODE1 = [posicaoX - 1, posicaoY - 1, 0, 1]
    NODE2 = [posicaoX    , posicaoY - 1, 0, None]
    NODE3 = [posicaoX + 1, posicaoY - 1, 0, 1]
    NODE4 = [posicaoX - 1, posicaoY    , 0, None]
    NODE5 = [posicaoX + 1, posicaoY    , 0, None]
    NODE6 = [posicaoX - 1, posicaoY + 1, 0, 6]
    NODE7 = [posicaoX    , posicaoY + 1, 0, None]
    NODE8 = [posicaoX + 1, posicaoY + 1, 0, 6]

    NODES = [NODE1, NODE2, NODE3, NODE4, NODE5, NODE6, NODE7, NODE8]

    # Calcula o peso de cada nó baseado na distância e quantidade de monstros
    for i, NODE in enumerate(NODES):
        try:
            if 0 <= NODE[1] < len(Mapa) and 0 <= NODE[0] < len(Mapa[0]):
                if Mapa[NODE[1]][NODE[0]] == "." or Mapa[NODE[1]][NODE[0]] == "@" or Mapa[NODE[1]][NODE[0]] == "8":
                    # Calcula distância até o objetivo
                    if TemMapa:
                        NODEhx = abs(posicaoXFinal - NODE[0])
                        NODEhy = abs(posicaoYFinal - NODE[1])
                    else:
                        NODEhx = abs(posicaoXMapa - NODE[0])
                        NODEhy = abs(posicaoYMapa - NODE[1])
                    
                    # Conta monstros ao redor do nó
                    monstros = contar_monstros_ao_redor(NODE[0], NODE[1])
                    
                    # Peso final = distância + (peso_por_monstro * número_de_monstros)
                    peso_por_monstro = 2  # Ajuste este valor para dar mais ou menos importância aos monstros
                    NODE[2] = NODEhx + NODEhy + (monstros * peso_por_monstro)
                    
                else:
                    NODE[2] = 999999999999
            else:
                NODE[2] = 999999999999
        except IndexError:
            NODE[2] = 999999999999

        print("Node ", i + 1, " :", NODE)

    # Encontra o nó com menor peso (considerando monstros e distância)
    MENOR = None
    direcaoNUM = None
    
    for i, NODE in enumerate(NODES):
        # Verifica se o nó pai é atravessável
        if NODE[3] is not None:
            node_pai = NODES[NODE[3]]
            if node_pai[2] == 999999999999:
                NODE[2] = 999999999999

        # Escolhe o nó com menor peso
        if MENOR is None or NODE[2] < MENOR[2]:
            MENOR = NODE
            direcaoNUM = i + 1

    # Se todos os nós são inacessíveis
    if all(node[2] == 999999999999 for node in NODES):
        direcaoNUM = None

    # Define as direções possíveis
    direcao = {
        0: "NaoAchei",
        None: "NaoAchei",
        1: "W,A",
        2: "W",
        3: "W,D",
        4: "A",
        5: "D",
        6: "S,A",
        7: "S",
        8: "S,D"
    }

    print("Node menor:", MENOR)
    
    try:
        return direcao[direcaoNUM]
    except UnboundLocalError:
        return direcao[0]

def jogar():
    
    
    global tempo, passos, update, TemMapa, posicaoXFinal, posicaoYFinal, posicaoXArmadilha, posicaoYArmadilha
    update = True
    global posicaoX, posicaoY
    while update:
        os.system('cls' if os.name == 'nt' else 'clear')  
        
        print("Mapa:")
        print(np.matrix(Mapa))  
        direcao = pathfinding()



        
        
        print("X:", posicaoX)
        print("Y:", posicaoY)    
        print("Final X:", posicaoXFinal)
        print("Final Y:", posicaoYFinal)    
        print("Armadilha X:",  posicaoXArmadilha)
        print("Armadilha Y:", posicaoYArmadilha)    
        print("Direcao: ", direcao)
        print("Tempo: ", tempo, "Segundos")
        print("Passos (teclas apertadas): ", passos)
        
        

        time.sleep(0.1)

        tempo += 0.1
        Historico.append(direcao)
        if direcao == "NaoAchei":
            print("Prendi, usar Força bruta")
            direcao = Aleatorio()
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


