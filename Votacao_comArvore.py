import numpy as np
import time 
import os
import random

# O 1 é o Robô
# O @ é a Saída

# Variáveis globais

posicaoXInicio = 0
posicaoYInicio = 0
posicaoXMapa = 1
posicaoYMapa = 1

# Mapa inicial
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

# Coordenadas da saída
posicaoXFinal = 7
posicaoYFinal = 7
posicaoXArmadilha = 0
posicaoYArmadilha = 0
Historico = []

# Variáveis globais
TemMapa = True
Morreu = False
Ganhou = False
Travou = False
tempo = 0
passos = 0

mortes_resultados = []
vitorias_resultados = []
Travou_resultados = []

# Função para criar o mapa
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
    mapa_adicionado = True
    while not mapa_adicionado:
        posicaoXMapa = random.randint(0, len(Mapa) - 1)
        posicaoYMapa = random.randint(0, len(Mapa[0]) - 1)
        
        # Verifica se a posição está livre
        if Mapa[posicaoYMapa][posicaoXMapa] == "1":
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

# Função para adicionar o player ao mapa
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

    if not TemMapa:
        Mapa[posicaoYMapa][posicaoXMapa] = "8"

    return posicaoX, posicaoY


def andar(direcao, posicaoX, posicaoY):
    global Morreu, update, TemMapa, posicaoXInicio, posicaoYInicio, posicaoXMapa, posicaoYMapa, posicaoXFinal, posicaoYFinal, posicaoXArmadilha, posicaoYArmadilha, Ganhou

    if direcao == "NaoAchei":
        Travou = True
    else:
        movimentos = {
            "D": (1, 0, "."), 
            "A": (-1, 0, "."), 
            "S": (0, 1, "."), 
            "W": (0, -1, ".")}

        for mov in direcao.split(","):
            mov = mov.upper()
            if mov in movimentos:
                dx, dy, Caminho = movimentos[mov]
                novoX, novoY = posicaoX + dx, posicaoY + dy
                if 0 <= novoX < len(Mapa[0]) and 0 <= novoY < len(Mapa):
                    if Mapa[novoY][novoX] == "@" and novoX == posicaoXFinal and novoY == posicaoYFinal:
                        Ganhou = True
                        update = False
                        return posicaoX, posicaoY, False, TemMapa
                    elif Mapa[novoY][novoX] == "@" and novoX == posicaoXArmadilha and novoY == posicaoYArmadilha:
                        Morreu = True
                        update = False
                        return posicaoX, posicaoY, False, TemMapa
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

def pathfinding():
    global posicaoX, posicaoY, posicaoXFinal, posicaoYFinal, posicaoXMapa, posicaoYMapa, Mapa
    
    if TemMapa:
        hx = abs(posicaoXFinal - posicaoX)
        hy = abs(posicaoYFinal - posicaoY)
        h = hx + hy
    else:
        hx = abs(posicaoXMapa - posicaoX)
        hy = abs(posicaoYMapa - posicaoY)
        h = hx + hy

    NODE1 = [posicaoX - 1, posicaoY - 1, 0, 1]
    NODE2 = [posicaoX, posicaoY - 1, 0, None]
    NODE3 = [posicaoX + 1, posicaoY - 1, 0, 1]
    NODE4 = [posicaoX - 1, posicaoY, 0, None]
    NODE5 = [posicaoX + 1, posicaoY, 0, None]
    NODE6 = [posicaoX - 1, posicaoY + 1, 0, 6]
    NODE7 = [posicaoX, posicaoY + 1, 0, None]
    NODE8 = [posicaoX + 1, posicaoY + 1, 0, 6]

    NODES = [NODE1, NODE2, NODE3, NODE4, NODE5, NODE6, NODE7, NODE8]

    for i, NODE in enumerate(NODES):
        try:
            if 0 <= NODE[1] < len(Mapa) and 0 <= NODE[0] < len(Mapa[0]):
                if Mapa[NODE[1]][NODE[0]] in [".", "@", "8"]:
                    if TemMapa:
                        NODEhx = abs(posicaoXFinal - NODE[0])
                        NODEhy = abs(posicaoYFinal - NODE[1])
                        NODEh = NODEhx + NODEhy
                    else:
                        NODEhx = abs(posicaoXMapa - NODE[0])
                        NODEhy = abs(posicaoYMapa - NODE[1])
                        NODEh = NODEhx + NODEhy

                    distancia = h + NODEh
                    NODE[2] = distancia
                elif posicaoXArmadilha == NODE[0] and posicaoYArmadilha == NODE[1]:
                    NODE[2] = 999999999999  # Obstáculo
                else:
                    NODE[2] = 999999999999  # Obstáculo
            else:
                NODE[2] = 999999999999  # Fora dos limites do mapa
        
        except IndexError:
            NODE[2] = 999999999999

    MENOR = None
    for i, NODE in enumerate(NODES):
        if NODE[3] is not None:
            node_pai = NODES[NODE[3]]
            if node_pai[2] == 999999999999:
                NODE[2] = 999999999999

        if MENOR is not None and NODE[2] == MENOR[2]:
            MENOR = NODE
            direcaoNUM = i + 1

        if MENOR is None or NODE[2] < MENOR[2]:
            MENOR = NODE
            direcaoNUM = i + 1
        
        if all(node[2] == 999999999999 for node in NODES):
            direcaoNUM = None

    direcao = {
        0 : "NaoAchei",  
        None: "NaoAchei"
    }

    direcao[1] = "W"
    direcao[2] = "W"
    direcao[3] = "W"
    direcao[4] = "A"
    direcao[5] = "D"
    direcao[6] = "S"
    direcao[7] = "S"
    direcao[8] = "S"

    try:
        return direcao[direcaoNUM]
    except UnboundLocalError:        
        return direcao[0]

def aleatorio():
    direcao = {}
    direcao[1] = "W"
    direcao[2] = "W"
    direcao[3] = "W"
    direcao[4] = "A"
    direcao[5] = "D"
    direcao[6] = "S"
    direcao[7] = "S"
    direcao[8] = "S"

    direcaoNUM = random.choice(range(1, 8))
    return direcao[direcaoNUM]

def monstro():
    global posicaoX, posicaoY, posicaoXFinal, posicaoYFinal, posicaoXMapa, posicaoYMapa, Mapa

    direcoes = {
        "w": (0, -1),  # cima
        "a": (-1, 0),  # esquerda
        "s": (0, 1),   # baixo
        "d": (1, 0),   # direita
    }

    opostos = {
        "w": "s",
        "s": "w",
        "a": "d",
        "d": "a",
    }

    for direcao, (dx, dy) in direcoes.items():
        nx, ny = posicaoX + dx, posicaoY + dy
        
        if 0 <= ny < len(Mapa) and 0 <= nx < len(Mapa[0]):
            if Mapa[ny][nx] == "M":
                return opostos[direcao]

    return aleatorio()  


def navegar_grafo(inicio, fim):
    global Mapa
    """ cria uma arvore usando o mapa e
    Navega no mapa usando DFS e retorna o caminho em formato WASD.
    
    :param inicio: Tupla (x, y) representando a posição inicial.
    :param fim: Tupla (x, y) representando a posição final.
    :return: String com a sequência de movimentos em WASD.
    """
    # Direções possíveis: (dx, dy, movimento)
    direcoes = {
        (0, -1): 'W',  # Cima
        (0, 1): 'S',   # Baixo
        (-1, 0): 'A',  # Esquerda
        (1, 0): 'D'    # Direita
    }
    
    # Estruturas para DFS
    stack = [(inicio, [])]  # Pilha com tuplas (posição, caminho)
    visitados = set()  # Conjunto de posições visitadas

    while stack:
        (x, y), caminho = stack.pop()
        
        # Se chegamos ao destino, retornamos o caminho
        if (x, y) == fim:
            return ','.join(caminho)

        # Marca a posição como visitada
        visitados.add((x, y))
        
        # Explora as direções
        for (dx, dy), movimento in direcoes.items():
            nx, ny = x + dx, y + dy
            
            # Verifica se a nova posição está dentro dos limites e é acessível
            if (0 <= nx < len(Mapa[0]) and 
                0 <= ny < len(Mapa) and 
                Mapa[ny][nx] in [".", "@", "1"] and 
                (nx, ny) not in visitados and 
                (nx, ny) != (posicaoXArmadilha, posicaoYArmadilha)):  # Verifica se não é a posição da armadilha
                
                stack.append(((nx, ny), caminho + [movimento]))
    return "Caminho não encontrado"  # Se não encontrar um caminho





tempo_travado = 0  # Contador para o tempo travado
MAX_TEMPO_TRAVADO = 5  # Limite de iterações para considerar "travado"
direcao_anterior = None  # Direção anterior do jogador

def votacao():
    global posicaoXFinal, posicaoYFinal, posicaoX, posicaoY
    inicio = (posicaoX, posicaoY)
    fim = (posicaoXFinal, posicaoYFinal)
    votos = []
    menorD = pathfinding().upper()
    votos.append(menorD)

    aleatorio1 = aleatorio().upper()
    votos.append(aleatorio1)

    monstro1 = monstro().upper()
    votos.append(monstro1)
    arvore = navegar_grafo(inicio, fim)
    votos.append(arvore[0])



    w = votos.count("W")
    a = votos.count("A")
    s = votos.count("S")
    d = votos.count("D")

    variaveis = {"w": w, "a": a, "s": s, "d": d}
    print("votos: ", variaveis)

    maior_nome = max(variaveis, key=variaveis.get)
    
    return maior_nome

tempo = 0
resultados = []  # Lista para armazenar os resultados de cada thread
tempo_todos = []
passos_total = []



def jogar():
    global tempo, passos, update, posicaoX, posicaoY, direcao_anterior, tempo_travado, Travou, Morreu, Ganhou,raiz, posicaoXFinal, posicaoYFinal, TemMapa, posicaoXMapa, posicaoYMapa
    posicaoX, posicaoY = adicionarPlayer()
    movimentosanteriores = []
    posicaoX = 0
    posicaoY = 0


    update = True
    while update:
        

        
        os.system('cls' if os.name == 'nt' else 'clear')  
        
        print("Mapa:")
        print(np.matrix(Mapa))  



        
        
        
        direcao = votacao()
        if direcao == "NaoAchei":
            Travou = True
            
        
        
        print("X:", posicaoX)
        print("Y:", posicaoY)    
        print("Direcao: ", direcao)
        



        
        
        tempo += 0.1

        if direcao == "Caminho não encontrado":
            Travou = True
        else:
            posicaoX, posicaoY, update,TemMapa = andar(direcao, posicaoX, posicaoY)
                # Verificando se a posição atual já foi registrada nos movimentos anteriores
        posicaoxy = (posicaoX, posicaoY)
        if posicaoxy not in movimentosanteriores:
            movimentosanteriores.append(posicaoxy)
            travado = 0  # Reseta o contador de travado, já que houve movimento
        else:
            travado += 1  # Incrementa o contador de travado

        if travado == 100:
            Travou = True  # Marca o jogo como travado
            update = False  # Encerra o loop do jogo, já que o jogo travou
        if Morreu:
            update = False
        if Ganhou:
            update = False   
        if Travou:
            update = False         
        
        direcao_anterior = direcao  # Atualiza a direção anterior
        passos += 1  # Incrementa o contador de passos
    
    mortes_resultados.append(Morreu)
    vitorias_resultados.append(Ganhou)
    Travou_resultados.append(Travou)
    tempo_todos.append(tempo)
    passos_total.append(passos)

update = False

# Função para rodar uma execução do jogo
def rodar_jogo():
    global Mapa, raiz

    Mapa = [
    [".", ".", ".", ".", ".", ".", ".", "@"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "@"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "@"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."]
    ]
    
    criar_mapa()
    jogar()


for i in range(100):
    TemMapa = True
    Ganhou = False
    Travou = False
    Morreu = False
    tempo = 0
    passos = 0

    posicaoX = 0
    posicaoY = 0
    
    rodar_jogo()

if update == False:
    # Contagem de vitórias, mortes e travamentos
    vitorias = vitorias_resultados.count(True)
    mortes = mortes_resultados.count(True)
    travou = Travou_resultados.count(True)

    # Verdadeiras positivas (vitórias corretas), Falsos negativos (mortos ou travados)
    vitórias_corretas = vitorias
    falsos_negativos = mortes   # Se o jogo travou ou morreu, consideramos que não houve vitória

    # Falsos positivos - situações em que o jogo terminou, mas não houve vitória (se precisar considerar)
    falsos_positivos = travou  # Não temos a definição de falsos positivos diretamente, então deixamos como 0.

    # Cálculo de precisão (Precision) e revocação (Recall)
    if vitórias_corretas + falsos_positivos > 0:
        precision = vitórias_corretas / (vitórias_corretas + falsos_positivos)
    else:
        precision = 0

    if vitórias_corretas + falsos_negativos > 0:
        recall = vitorias / (vitorias + mortes + travou)
    else:
        recall = 0

        # Cálculo do F1 Score
    if precision + recall > 0:
        f1_score = 2 * (precision * recall) / (precision + recall)
    else:
        f1_score = 0

    print("Ganhou: ", vitorias)
    print("Morte: ", mortes)
    print("Travou: ", travou)

    # Exibe as métricas de precisão e revocação
    print(f"Precisão (Precision): {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1_score:.2f}")
    print("----------")

    media_passos = sum(passos_total) / len(passos_total)

    print("A media de Passos: ", media_passos)
    