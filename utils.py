class No:
    def __init__(self, estado, total_F, custo_G, heuristica_H, pai):
        self.estado = estado
        self.total_F = total_F
        self.custo_G = custo_G
        self.heuristica_H = heuristica_H
        self.pai = pai

def reordenarLista(listaAberta):
    elementos = len(listaAberta) - 1
    ordenado = False
    while not ordenado:
        ordenado = True
        for i in range(elementos):
            if listaAberta[i].total_F > listaAberta[i + 1].total_F:
                listaAberta[i], listaAberta[i + 1] = listaAberta[i + 1], listaAberta[i]
                ordenado = False
    return listaAberta

def calcularCusto(estadoInicial, estadoAtual, listaFechada, listaAberta):
    G = 0
    aux = True
    if estadoInicial == estadoAtual:
        return G
    else:
        for no in listaAberta:
            if estadoAtual == no.estado:
                estadoAtual = no.pai
                if estadoAtual == estadoInicial:
                    return G + 1
        while aux:
            for no in listaAberta:
                if estadoAtual == no.estado:
                    estadoAtual = no.pai
            for no in listaFechada:
                if estadoAtual == no.estado:
                    estadoAtual = no.pai
                    G = G + 1
                    if estadoAtual == estadoInicial:
                        aux = False
        return G

def getAdjacentes(estadoAtual, listaAberta, listaFechada, bloqueios, arvore):
    listaExpansao = []
    adjacents = todosAdjacentesValidos(estadoAtual, bloqueios)
    for adjacent in adjacents:
        valido = True
        for no in listaFechada:
            if no.estado == adjacent:
                valido = False
        for no in listaAberta:
            if no.estado == adjacent:
                valido = False
        if valido == True:
            listaExpansao.append(adjacent)
            arvore.append(adjacent)
    return listaExpansao

def todosAdjacentesValidos(estadoAtual, bloqueios):
    candidatos = [(estadoAtual[0] - 1, estadoAtual[1]),
                (estadoAtual[0], estadoAtual[1] + 1),
                (estadoAtual[0], estadoAtual[1] - 1),
                (estadoAtual[0] + 1, estadoAtual[1])]
    def isValidState(estado):
        if (estado[0] >= 0 and estado[0] <= 6 and estado[1] >= 0 and estado[1] <= 6):
            if (estado not in bloqueios):
                return True
        return False
    return [candidato for candidato in candidatos if isValidState(candidato)]

def abrirLista(listaExpansao, estadoInicial, estadoFinal, estadoAtual, listaAberta, listaFechada, funcaoHeuristica, funcaoHeuristica2, guardas, arvore):
    for estado in listaExpansao:
        custo_G = calcularCusto(estadoInicial, estadoAtual, listaFechada, listaAberta) + 1
        heuristica_H = funcaoHeuristica(estado, estadoFinal) + funcaoHeuristica2(estado, guardas)
        total_F = custo_G + heuristica_H
        novo_no = No(estado, total_F, custo_G, heuristica_H, estadoAtual)
        arvore.node(str(novo_no.estado).replace('(', '').replace(', ', '.').replace(')', ''), str(novo_no.estado))
        arvore.edge(str(novo_no.pai).replace('(', '').replace(', ', '.').replace(')', ''), str(novo_no.estado).replace('(', '').replace(', ', '.').replace(')', ''))
        listaAberta.append(novo_no)
    return listaAberta

def melhorCaminho(estadoAtual, estadoInicial, listaFechada):
    listaComMelhorCaminho = [estadoAtual]
    chegou = True
    while chegou:
        for no in listaFechada:
            if no.estado == estadoAtual:
                estadoAtual = no.pai
                listaComMelhorCaminho.append(estadoAtual)
                if estadoAtual == estadoInicial:
                    chegou = False
                break
    listaComMelhorCaminho.reverse()
    return listaComMelhorCaminho