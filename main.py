from utils import *
from random import randint

if __name__ == "__main__":
    # Heurística Definition
    def heuristica(estadoAtual, estadoFinal):
        #valor D que é o minimo dos custos de alteração de estado, logo, D=1
        return abs(estadoAtual[0] - estadoFinal[0]) + abs(estadoAtual[1] - estadoFinal[1])
    # 0 é a primeira coordenada e o 1 é a segunda

    def heuristica2(estadoAtual, guarda):
        return min( heuristica(estadoAtual, guarda[0]), heuristica(estadoAtual, guarda[1]))

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

    # Game config
    print("Digite as coordenadas [separadas por uma virgula]: \n")
    x, y = input().split(',')
    x, y = int(x), int(y)
    estadoInicial = (x, y)
    xfinal, yfinal = randint(0, 6), randint(0, 6)
    estadoFinal = (xfinal, yfinal)
    print("Estado Objetivo:", estadoFinal)

    qtdbloqueios = randint(3, 6) #mudar no relatorio
    qtdguardas = randint(2, 3)
    #print("Quantidade de bloqueios: ", qtdbloqueios)
    cordbloqueios_set = set()
    while len(cordbloqueios_set) < qtdbloqueios:
        x, y = 6, 0
        while (x, y) == (6, 0):
            x, y = randint(0, 6), randint(0, 6)
            cordbloqueios_set.add((x, y))
    bloqueios = cordbloqueios_set
    print("Bloqueios: ", bloqueios)

    cordguarda_set = set()
    while len(cordguarda_set) < qtdguardas:
        x, y = 6, 0
        while (x, y) == (6, 0):
            x, y = randint(0, 6), randint(0, 6)
            cordguarda_set.add((x, y))
    cordguarda_set.add((1, 2)) #depois apaga
    guarda = cordguarda_set
    print("Guardas: ", guarda)

    if estadoInicial in bloqueios:
        print("O estado inicial escolhido é invalido(tentou inserir em um bloqueio)")
    else:
        # Run
        caminho = search(estadoInicial, estadoFinal, bloqueios, heuristica)
        # Results
        #arrumar isso aqui, pois ele nao ta pegando mesmo que tenha guardas no caminho
        if (guarda in caminho):
            print("Ronaldinho foi preso")
        else:
            for estado in caminho:
                print('Estado:', estado, 'Heurística:', heuristica(estado, estadoFinal))
            print('Ronaldinho conseguiu driblar os guardas da prisão!')
            print("Quantidade de Movimentos:", len(caminho) - 1)