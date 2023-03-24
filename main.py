# Diminuir quantidade de indivíduos e aumentar quantidade de gerações
#

import random
import copy
import time
# from matplotlib import pyplot as plt

random.seed(56)

#Função Calcular Distância
def calcDist(ponto1, ponto2):
    distPontos = ((((ponto1[0] - ponto2[0]) ** 2)+((ponto1[1] - ponto2[1]) ** 2)) ** 0.5)
    return distPontos

def setDist(lista):
    matriz = [[calcDist(lista[i], lista[j]) for j in range(len(lista))] for i in range(len(lista))]
    return matriz

def getDist(i, j, matriz):
    return matriz[i][j]

#Função que gera a primeira população
def primeiraPop(matriz, n, listaEntrada):
    pop = []
    m = len(matriz)
    for i in range(n):
        pop.append(random.sample(range(0, m), len(listaEntrada)))
    return pop

#Função Fitness
def fitness(pop, matriz):
    listFit = []

    for i in range(len(pop)):
        somaInd = 0
        for j in range(len(pop[i]) - 1):
            somaInd += getDist(pop[i][j], pop[i][j + 1], matriz)
        somaInd += getDist(pop[i][j], pop[i][0], matriz)
        listFit.append(somaInd)

    return listFit

# Função seleção por torneio (Fazendo a competição entre 2 aleatórios)
def selecao(fits):
    pais = []
    size = int(len(fits) / 1.25)
    # ordFit = sorted(range(len(fits)), key=lambda k: fits[k], reverse=False)
    # for i in range(10):
    #     pais.append(ordFit[i])
    for i in range(size):
        idx_candidato1 = random.randint(0, (len(fits) // 5) - 1)
        idx_candidato2 = random.randint(0, (len(fits) // 5) - 1)
        ganhador = idx_candidato2
        if fits[idx_candidato1] < fits[ganhador]:
            ganhador = idx_candidato1
        pais.append(ganhador)

    for i in range(len(fits) - size):
        idx_candidato1 = random.randint((len(fits)) // 5, len(fits) - 1)
        idx_candidato2 = random.randint((len(fits)) // 5, len(fits) - 1)
        ganhador = idx_candidato2
        if fits[idx_candidato1] < fits[ganhador]:
            ganhador = idx_candidato1
        pais.append(ganhador)
    return sorted(pais)

#Função crossover
def crossover(p1, p2):
    filho = copy.copy(p1)

    n = random.sample(range(0, len(p1)), random.randint(1, len(p1) - 1))
    n.sort()
    aux = []
    for i in n:
        aux.append(p1[i])
    n_ord = []
    for i in p2:
        if i in aux:
            n_ord.append(aux.index(i))
    for i in range(len(aux)):
        filho[n[i]] = aux[n_ord[i]]
    return filho

def mutacao(cromossomo):
    i, j = sorted(random.sample(range(len(cromossomo)), 2))
    cromossomo[i:j+1] = reversed(cromossomo[i:j+1])
    return cromossomo

def mutacaoOnePoint(cromossomo):
    i, j = sorted(random.sample(range(len(cromossomo)), 2))
    cromossomo[i], cromossomo[j] = cromossomo[j], cromossomo[i]
    return cromossomo


def elitismo(pop, listfit, qtd):
    newpop = []
    ordFit = sorted(range(len(listfit)), key=lambda k: listfit[k], reverse=False)
    for i in range(qtd):
        newpop.append(pop[ordFit[i]])
    return newpop

#Função Gerar nova população
def geraNewPop(pop, matriz, tMutacao, usarElitismo):
    newPop = []
    newFits = fitness(pop, matriz)
    i = 0
    ordFit = selecao(newFits)
    numCross = len(pop)
    while i < numCross:
        aux = ordFit[i]
        if aux == len(pop) - 1:
            newPop.append(crossover(pop[aux], pop[0]))
        else:
            newPop.append(crossover(pop[aux], pop[aux + 1]))

        if tMutacao < 50:
            if random.uniform(0, 100) <= tMutacao:
                    newPop[i] = mutacao(newPop[i])
        else:
            if random.uniform(0, 100) <= tMutacao:
                    newPop[i] = mutacaoOnePoint(newPop[i])
        i += 1
    if usarElitismo == True:
        for c in range(len(pop)):
            newPop.append(pop[c])
        newFits = fitness(newPop, matriz)
        newPop = elitismo(newPop, newFits, len(pop))
        ordFit = selecao(newFits)
    return newPop

#Função principal do GA
def evolucao(listEntrada, qtdGen):
    qtdGen += 1
    # matrizDists = setDist(listEntrada)
    matrizDists = listEntrada
    pop = primeiraPop(matrizDists, 500, listEntrada)
    listFit = fitness(pop, matrizDists)
    ordFits = selecao(pop)
    menorCaminho = listFit[ordFits[0]]
    menorFits = []
    mediaFits = []
    # count = 0
    taxaMutacao = 5
    usarElitismo = True
    for i in range(qtdGen):

        newPop = geraNewPop(pop, matrizDists, taxaMutacao, usarElitismo)
        newFits = fitness(newPop, matrizDists)
        pop = newPop
        ordFits = selecao(pop)
        menorFits.append(newFits[ordFits[0]])
        mediaFits.append(sum(newFits) / len(newFits))
        if min(menorFits) < menorCaminho:
            # menorCaminho = newFits[ordFits[0]]
            menorCaminho = min(menorFits)
        if i > 0 and mediaFits[i] == mediaFits[i - 1]:
            count += 1
        else:
            count = 0
        if count >= 100:
            count = 0
            taxaMutacao += 5
            # usarElitismo = False
            print('TAXA MUTAÇÃO: ', taxaMutacao)
        print("geração", i,":", round(menorFits[i], 3)," média:", round(mediaFits[i], 3))
    # plt.figure()
    # plt.plot(range(qtdGen), mediaFits, label='Caminho médio')
    # plt.plot(range(qtdGen), menorFits, label='Caminho mínimo')
    # plt.legend()
    # plt.ylabel('Distância')
    # plt.xlabel('Gerações')
    # plt.show()
    melhorCaminho = newPop[ordFits[0]]
    print(melhorCaminho)

# if __name__ == "__main__":
#     with open('entrada.tsp.txt', "r") as f:
#         dimension = [line.strip().split(" ") for line in f.readlines()[3:4]]
#         dimension = int(dimension[0][1])
#         dimension += 6 #É necessário alterar este valor para o número da linha em que aparece NODE_COORD_SECTION
#     f.close()
#     with open('entrada.tsp', "r") as f:
#         listaAux = [list(map(float, line.strip().split())) for line in f.readlines()[6:dimension]] #É necessário alterar este valor para o número da linha em que aparece NODE_COORD_SECTION
#         matrizEntrada = [[x[1], x[2]] for x in listaAux]
#     f.close()
#     ini = time.time()
#     evolucao(matrizEntrada, 400)
#     fim = time.time()
#     print("Tempo gasto:", round(fim - ini, 3))

if __name__ == "__main__":
    with open('brazil58.tsp', "r") as f:
        lines = f.readlines()
        # Procurar pela dimensão do problema
        for i, line in enumerate(lines):
            if line.startswith('DIMENSION'):
                dimension = int(line.split(':')[1])
            elif line.startswith('EDGE_WEIGHT_FORMAT'):
                weight_format = line.split(':')[1].strip()
            elif line.startswith('EDGE_WEIGHT_SECTION'):
                weight_section_index = i + 1
        f.close()

        # Ler a matriz de distâncias
        distance_matrix = [[0] * dimension for _ in range(dimension)]
        if weight_format == 'UPPER_ROW':
            row_index = 0
            for i, line in enumerate(lines[weight_section_index:weight_section_index+dimension-1]):
                elements = [int(x) for x in line.split()]
                for j, element in enumerate(elements):
                    distance_matrix[row_index][row_index+j+1] = element
                row_index += 1
        else:
            raise ValueError(f"Unsupported EDGE_WEIGHT_FORMAT: {weight_format}")

        # Preencher a diagonal inferior com os valores correspondentes
        for i in range(dimension):
            for j in range(i):
                distance_matrix[i][j] = distance_matrix[j][i]

        # Executar a função de otimização com a matriz de distâncias
        ini = time.time()
        evolucao(distance_matrix, 10000)
        fim = time.time()
        print("Tempo gasto:", round(fim - ini, 3))

