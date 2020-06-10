from utils import *

if __name__ == "__main__":
    # Heurística Definition
    def heuristica(estadoAtual, estadoFinal):
        return abs(estadoFinal[0] - estadoAtual[0]) + abs(estadoFinal[1] - estadoAtual[1]) 

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
    estadoInicial = (0,0)
    estadoFinal = (6,6)
    bloqueios = [(0,5),(1,5),(2,5),(3,5),(5,5),(6,5)]    

    # Run
    caminho = search(estadoInicial, estadoFinal, bloqueios, heuristica)

    # Results
    for estado in caminho:
        print('Estado:', estado, 'Heurística:', heuristica(estado, estadoFinal))

    print("Quantidade de Movimentos:", len(caminho) - 1)