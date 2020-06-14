from utils import *
from tkinter import *
from random import randint
import sys

if __name__ == "__main__":
    class ScrolledFrame(Frame):
        def __init__(self, parent, vertical=True, horizontal=False):
            super().__init__(parent)

            #Configurando container para o conteúdo da janela
            self._canvas = Canvas(self)
            self._canvas.grid(row=0, column=0, sticky='news')
            self._vertical_bar = Scrollbar(self, orient='vertical', command=self._canvas.yview)
            if vertical:
                self._vertical_bar.grid(row=0, column=1, sticky='ns')
            self._canvas.configure(yscrollcommand=self._vertical_bar.set)
            self.inner = Frame(self._canvas)
            self._window = self._canvas.create_window((0, 0), window=self.inner, anchor='nw')
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            self.inner.bind('<Configure>', self.resize)
            self._canvas.bind('<Configure>', self.frame_width)

        def frame_width(self, event):
            canvas_width = event.width
            self._canvas.itemconfig(self._window, width = canvas_width)

        def resize(self, event=None): 
            self._canvas.configure(scrollregion=self._canvas.bbox('all'))

    class Application:
        def __init__(self, master=None):
            self.tentativas = 0
            self.qtdDerrotas = 0
            self.index = False

            self.fontePadrao = ("Arial", "10")
            self.primeiroContainer = Frame(master)
            self.primeiroContainer["pady"] = 10
            self.primeiroContainer.pack()
    
            self.segundoContainer = Frame(master)
            self.segundoContainer["padx"] = 20
            self.segundoContainer.pack()
    
            self.terceiroContainer = Frame(master)
            self.terceiroContainer["padx"] = 20
            self.terceiroContainer.pack()
    
            self.quartoContainer = Frame(master)
            self.quartoContainer["padx"] = 20
            self.quartoContainer.pack()
            
            self.quintoContainer = Frame(master)
            self.quintoContainer["pady"] = 20
            self.quintoContainer.pack()
    
            self.titulo = Label(self.primeiroContainer, text="Prison's Heist")
            self.titulo["font"] = ("Arial", "10", "bold")
            self.titulo.pack()
    
            self.titulo = Label(self.segundoContainer, text="RODADA 1")
            self.titulo["font"] = ("Arial", "8", "bold")
            self.titulo.pack()
    
            self.nomeLabel = Label(self.terceiroContainer,text="Digite as coordenadas do estado inicial entre 0 e 6 (Ex. 0,6)", font=self.fontePadrao)
            self.nomeLabel.pack()
    
            self.entrada = Entry(self.terceiroContainer)
            self.entrada["width"] = 30
            self.entrada["font"] = self.fontePadrao
            self.entrada.pack()

            self.autenticar = Button(self.quartoContainer)
            self.autenticar["text"] = "Encontre o caminho!"
            self.autenticar["font"] = ("Calibri", "8")
            self.autenticar["width"] = 20
            self.autenticar["command"] = self.rodarJogo
            self.autenticar.pack()
    
            self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
            self.mensagem["fg"] = "red"
            self.mensagem.pack()

            self.msgEstados = Label(self.quartoContainer, text="", font=self.fontePadrao)
            self.msgEstados.pack()

            self.resultado = Label(self.quartoContainer, text="", font=self.fontePadrao)
            self.resultado.pack()

            self.passos = Label(self.quartoContainer, text="", font=self.fontePadrao)
            self.passos.pack()

            self.mapa = Label(self.quartoContainer, text="", font=self.fontePadrao)
            self.mapa.pack()

            self.saida = Label(self.quartoContainer, text="", font=self.fontePadrao)
            self.saida.pack()

        # Heurística Definitions
        def heuristica(self,estadoAtual, estadoFinal):
            return abs(estadoAtual[0] - estadoFinal[0]) + abs(estadoAtual[1] - estadoFinal[1])
        def heuristica2(self,estadoAtual, guardas):
            valorh2 = min([self.heuristica(estadoAtual, guarda) for guarda in guardas])
            if valorh2 != 0:
                return 1/valorh2
            else:
                return 0

        # A* Definition
        def search(self,estadoInicial, estadoFinal, bloqueios, guardas, heuristica, heuristica2, listaAberta, listaFechada, arvore):
            estadoAtual = estadoInicial
            arvore.append(estadoInicial)

            # primeiro nó da árvore
            custo_G = 0
            heuristica_H = heuristica(estadoAtual, estadoFinal) + heuristica2(estadoAtual, guardas)
            total_F = custo_G + heuristica_H
            novo_no = No(estadoAtual, total_F, custo_G, heuristica_H, None)
            listaAberta.append(novo_no)
            passos = ""

            # busca
            while estadoAtual != estadoFinal:
                listaExpansao = getAdjacentes(estadoAtual, listaAberta, listaFechada, bloqueios, arvore)
                listaAberta = abrirLista(listaExpansao, estadoInicial, estadoFinal, estadoAtual, listaAberta, listaFechada, heuristica, heuristica2, guardas)

                # fechar primeiro nó da listaAberta
                try:
                    no = listaAberta[0]
                except IndexError:
                    self.index = True
                    return None
                
                passos += "Árvore expandindo!\n" + str(arvore) + "\n----\n"
                passos += "Lista aberta expandindo!\n"
                for node in listaAberta:
                    passos += str(node.estado) + " "
                passos += "\n----\n"
                passos += "Lista Fechada expandindo!\n"
                for node in listaFechada:
                    passos += str(node.estado) + " "
                passos += "\n----\n"

                self.passos["text"] = passos

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
        def estFinalConfig(self):
            xfinal, yfinal = randint(0, 6), randint(0, 6)
            estadoFinal = (xfinal, yfinal)
            return estadoFinal
        def blockConfig(self,estadoFinal, adjacentesFinal):
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
        def guardaConfig(self,estadoFinal, bloqueios, adjacentesFinal):
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
        def solicitarEstadoInicial(self, entrada, estadoFinal, bloqueios, guardas):
            if entrada and len(entrada) == 3 and entrada[1] == ',' and entrada[0].isdigit() and entrada[2].isdigit():
                x, y = entrada.split(',')
                x, y = int(x), int(y)
                if x >= 0 and x <= 6 and y >= 0 and y <= 6:
                    if (x, y) != estadoFinal and (x, y) not in bloqueios and (x, y) not in guardas:
                        estadoInicial = (x, y)
                        self.mensagem["text"] = ""
                        return estadoInicial
                self.mensagem["text"] = "Estado inicial inválido - posição já ocupada ou não existente"
                return None
            self.mensagem["text"] = "Entrada inválida"
            return None

        # Game
        def rodarJogo(self):
            estadoFinal = self.estFinalConfig()
            adjacentesFinal = todosAdjacentesValidos(estadoFinal, [])
            bloqueios = self.blockConfig(estadoFinal, adjacentesFinal)
            guardas = self.guardaConfig(estadoFinal, bloqueios, adjacentesFinal)
            listaAberta = []
            listaFechada = []
            arvore = []
            
            for i in range(3):
                self.resultado["text"] = ""
                self.msgEstados["text"] = ""
                self.tentativas = i + 1        
                self.titulo["text"] = ("RODADA " + str(self.tentativas))
                estadoInicial = self.solicitarEstadoInicial(self.entrada.get(),estadoFinal, bloqueios, guardas)
                if(estadoInicial == None):
                    return None
                caminho = self.search(estadoInicial, estadoFinal, bloqueios, guardas, self.heuristica, self.heuristica2, listaAberta, listaFechada, arvore)

                # Results
                foiPreso = False
                if caminho:
                    textoEstado = ''
                    for estado in caminho:   
                        valorFnTotal = self.heuristica(estado, estadoFinal) + self.heuristica2(estado, guardas)
                        textoEstado += ('Estado: ' + str(estado) + ' F(n): ' + str(valorFnTotal) + '\n') 
                        if (estado in guardas):
                            textoResultado = "DERROTA - Havia um guarda em seu caminho"
                            self.qtdDerrotas += 1
                            foiPreso = True
                            break
                    self.msgEstados["text"] = textoEstado
                if not foiPreso:
                    break
                else:
                    self.resultado["fg"] = "red"
                    self.resultado["text"] = textoResultado

            self.entrada.destroy()
            self.autenticar.destroy()
            self.nomeLabel.destroy()
            self.mensagem.destroy()
            self.titulo["text"] = ("RESULTADO")
            if self.qtdDerrotas == 3:
                self.resultado["fg"] = "red"
                self.resultado["text"] = " GAME OVER - Após 3 tentativas, você foi realocado de prisão"
            elif caminho == None:
                self.resultado["fg"] = "red"
                self.resultado["text"] = " GAME OVER - Literalmente, não havia uma rota de fuga! Que azar!"
            else:
                self.resultado["fg"] = "green"
                self.resultado["text"] = (" VITÓRIA - Você fugiu em " + str(self.tentativas) + " tentativa(s)\n Quantidade de Movimentos: " + str(len(caminho) - 1))

            self.mapa["text"] = ("MAPA DO JOGO\nBloqueios: " + str(bloqueios) + "\nGuardas: " + str(guardas) + "\nEstado Final: " + str(estadoFinal))
            if(not self.index):
                textoAberto = ""
                for no in listaAberta:
                    textoAberto += str(no.estado) + " "

                textoFechado = ""
                for no in listaFechada:
                    textoFechado += str(no.estado) + " "

                self.saida["text"] = ("SAÍDA DO ALGORITMO\nNós abertos:" + textoAberto + "\nNós fechados:" + textoFechado + "\nÁrvore:" + str(arvore))
    root = Tk()
    root.geometry("600x600")
    root.title("Prison's Heist")
    window = ScrolledFrame(root)
    window.pack(expand=True, fill='both')
    Application(window.inner)

    root.mainloop()