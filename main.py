from utils import *
from random import randint
import sys

if __name__ == "__main__":
    # Heurística Definitions
    def heuristica(estadoAtual, estadoFinal):
        #valor D que é o minimo dos custos de alteração de estado, logo, D = 1
        return abs(estadoAtual[0] - estadoFinal[0]) + abs(estadoAtual[1] - estadoFinal[1])

    def heuristica2(estadoAtual, guarda):
        return min(heuristica(estadoAtual, guarda[0]), heuristica(estadoAtual, guarda[1]))

    # A* Definition
    def search(estadoInicial, estadoFinal, bloqueios, heuristica):
        estadoAtual = estadoInicial
        listaFechada = []
        listaAberta = []

        # primeiro nó da árvore
        custo_G = 0
        heuristica_H = heuristica(estadoAtual, estadoFinal)
        total_F = custo_G + heuristica_H
        novo_no = No(estadoAtual, total_F, custo_G, heuristica_H, None)
        listaAberta.append(novo_no)

        # busca
        while estadoAtual != estadoFinal:
            listaExpansao = getAdjacentes(estadoAtual, listaAberta, listaFechada, bloqueios)
            listaAberta = abrirLista(listaExpansao, estadoInicial, estadoFinal, estadoAtual, listaAberta, listaFechada, heuristica)

            # fechar primeiro nó da listaAberta
            no = listaAberta[0]
            listaFechada.append(no)
            listaAberta.remove(no)
            listaAberta = reordenarLista(listaAberta)

            # mudar estado se ainda tiver listaAberta
            if len(listaAberta) != 0:
                estadoAtual = listaAberta[0].estado

        # fim da busca
        listaFechada.append(listaAberta[0])

        return melhorCaminho(estadoAtual, estadoInicial, listaFechada)

    # Game configs
    xfinal, yfinal = randint(0, 6), randint(0, 6)
    estadoFinal = (xfinal, yfinal)
    #print("Estado Objetivo: ", estadoFinal)
    
    qtdbloqueios = randint(3, 6)
    cordbloqueios_set = set()
    while len(cordbloqueios_set) < qtdbloqueios:
        x, y = randint(0, 6), randint(0, 6)
        if (x, y) != estadoFinal and (x, y) not in cordbloqueios_set:
            cordbloqueios_set.add((x, y))
    bloqueios = cordbloqueios_set
    #print("Bloqueios: ", bloqueios)

    qtdguardas = randint(2, 3)
    cordguardas_set = set()
    while len(cordguardas_set) < qtdguardas:
        x, y = randint(0, 6), randint(0, 6)
        if (x, y) != estadoFinal and (x, y) not in cordbloqueios_set and (x, y) not in cordguardas_set:
            cordguardas_set.add((x, y))
    guardas = cordguardas_set
    #print("Guardas: ", guardas)

    while True:
        print("Digite as coordenadas [separadas por uma virgula]:")
        x, y = input().split(',')
        x, y = int(x), int(y)
        if (x, y) != estadoFinal and (x, y) not in cordbloqueios_set and (x, y) not in cordguardas_set:
            if x >= 0 and x <= 6 and y >= 0 and y <= 6:
                estadoInicial = (x, y)
                break
        print("O estado inicial escolhido é invalido - posição já ocupada ou não existente")
    
    # Run
    caminho = search(estadoInicial, estadoFinal, bloqueios, heuristica)

    # Results
    for estado in caminho:   
        print('Estado:', estado, 'Heurística:', heuristica(estado, estadoFinal))     
        if (estado in guardas):
            print("GAME OVER - Ronaldinho foi preso")
            sys.exit()

    print('VICTORY - Ronaldinho fugiu')
    print("Quantidade de Movimentos:", len(caminho) - 1)