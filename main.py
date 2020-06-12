from utils import *
from random import randint
import sys

if __name__ == "__main__":
    # Heurística Definitions
    def heuristica(estadoAtual, estadoFinal):
        return abs(estadoAtual[0] - estadoFinal[0]) + abs(estadoAtual[1] - estadoFinal[1])
    def heuristica2(estadoAtual, guardas):
        valorh2 = min([heuristica(estadoAtual, guarda) for guarda in guardas])
        if valorh2 != 0:
            return 1/valorh2
        else:
            return 0

    # A* Definition
    def search(estadoInicial, estadoFinal, bloqueios, guardas, heuristica, heuristica2):
        estadoAtual = estadoInicial
        listaFechada = []
        listaAberta = []

        # primeiro nó da árvore
        custo_G = 0
        heuristica_H = heuristica(estadoAtual, estadoFinal) + heuristica2(estadoAtual, guardas)
        total_F = custo_G + heuristica_H
        novo_no = No(estadoAtual, total_F, custo_G, heuristica_H, None)
        listaAberta.append(novo_no)

        # busca
        while estadoAtual != estadoFinal:
            listaExpansao = getAdjacentes(estadoAtual, listaAberta, listaFechada, bloqueios)
            listaAberta = abrirLista(listaExpansao, estadoInicial, estadoFinal, estadoAtual, listaAberta, listaFechada, heuristica, heuristica2, guardas)

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

    # Game configs Definitions
    def estFinalConfig():
        xfinal, yfinal = randint(0, 6), randint(0, 6)
        estadoFinal = (xfinal, yfinal)
        #print("Estado Objetivo:", estadoFinal)
        return estadoFinal
    def blockConfig(estadoFinal, adjacentesFinal):
        qtdbloqueios = randint(3, 6)
        cordbloqueios_set = set()
        while len(cordbloqueios_set) < qtdbloqueios:
            x, y = randint(0, 6), randint(0, 6)
            if (x, y) != estadoFinal and (x, y) not in cordbloqueios_set:
                if (x, y) in adjacentesFinal and len(adjacentesFinal) > 1:
                    cordbloqueios_set.add((x, y))
                    adjacentesFinal.remove((x, y))
                else:
                    cordbloqueios_set.add((x, y))
        bloqueios = cordbloqueios_set
        #print("Bloqueios:", bloqueios)
        return bloqueios
    def guardaConfig(estadoFinal, bloqueios, adjacentesFinal):
        qtdguardas = randint(2, 3)
        cordguardas_set = set()
        while len(cordguardas_set) < qtdguardas:
            x, y = randint(0, 6), randint(0, 6)
            if (x, y) != estadoFinal and (x, y) not in bloqueios and (x, y) not in cordguardas_set:
                if (x, y) in adjacentesFinal and len(adjacentesFinal) > 1:
                    cordguardas_set.add((x, y))
                    adjacentesFinal.remove((x, y))
                else:
                    cordguardas_set.add((x, y))
        guardas = cordguardas_set
        #print("Guardas:", guardas)
        return guardas

    # User input
    def solicitarEstadoInicial(estadoFinal, bloqueios, guardas):
        while True:
            print("Digite as coordenadas do estado inicial (Ex. 0,6)")
            x, y = input().split(',')
            x, y = int(x), int(y)
            if x >= 0 and x <= 6 and y >= 0 and y <= 6:
                if (x, y) != estadoFinal and (x, y) not in bloqueios and (x, y) not in guardas:
                    estadoInicial = (x, y)
                    break
            print("Estado inicial inválido - posição já ocupada ou não existente")
        return estadoInicial

    # Game
    estadoFinal = estFinalConfig()
    adjacentesFinal = todosAdjacentesValidos(estadoFinal, [])
    bloqueios = blockConfig(estadoFinal, adjacentesFinal)
    guardas = guardaConfig(estadoFinal, bloqueios, adjacentesFinal)
    
    tentativas = 0
    qtdDerrotas = 0
    for i in range(3):
        tentativas = i + 1        
        print("\nRODADA",tentativas,"------------------------------------------------------------")
        estadoInicial = solicitarEstadoInicial(estadoFinal, bloqueios, guardas)
        caminho = search(estadoInicial, estadoFinal, bloqueios, guardas, heuristica, heuristica2)

        # Results
        foiPreso = False
        for estado in caminho:   
            valorFnTotal = heuristica(estado, estadoFinal) + heuristica2(estado, guardas)
            print(' Estado:', estado, 'F(n):', valorFnTotal)   
            if (estado in guardas):
                print(" DERROTA - Havia um guarda em seu caminho")
                qtdDerrotas += 1
                foiPreso = True
                break
        
        if not foiPreso:
            break

    print("\nRESULTADO -----------------------------------------------------------")
    if qtdDerrotas == 3:
        print(" GAME OVER - Após 3 tentativas, você foi realocado de prisão")
    else:
        print(" VITÓRIA - Você fugiu em", tentativas, "tentativa(s)")
        print(" Quantidade de Movimentos:", len(caminho) - 1)

    print("\nMAPA DO JOGO --------------------------------------------------------")
    print(" Bloqueios:", bloqueios)
    print(" Guardas:", guardas)
    print(" Estado Final:", estadoFinal)

    print("\nSAÍDA DO ALGORITMO --------------------------------------------------")
    print(" Nós abertos:")
    print(" Nós fechados:")
    print(" Árvore:")