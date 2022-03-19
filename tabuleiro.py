from pygame import *
from jogador import Jogador
from posicao import Posisao

class Tabuleiro():
    def __init__(self):
        self._jogador1 = Jogador(1)
        self._jogador2 = Jogador(2)
        self._vencedor = None

        self._tabuleiro = []

        self._jogadorVez = self._jogador1

#getters
    def jogadorVez(self):
        return self._jogadorVez
  
    def jogador1(self):
        return self._jogador1

    def jogador2(self):
        return self._jogador2
    
    def vencedor(self):
        return self._vencedor

    def matriz(self):
        return self._tabuleiro

#matriz tabuleiro
    def construirMatrizTabuleiro(self):
        #construção da matriz do tabuleiro
        t_altura = 44
        #t_largura = 50
        #meio ponto 325 , x_meio 325 - 25 (metade da largura do triangulo)
        meio = 325 -25
        triangulos = 5
        for l in range(11):
            self._tabuleiro.append([])
            cor = 1
            jogador = self._jogador2
            if l >= 9:
                cor = 0
                jogador = self._jogador1
            x = triangulos//2 
            for t in range(triangulos):
                #negativo
                if t+1< triangulos//2+1:
                    rect = Rect((meio -25*x+25*t, t_altura*l + 100),(50,44))   
                #neutro
                elif t+1== triangulos//2+1:
                    rect = Rect((meio, t_altura*l + 100),(50,44))
                    x = 1
                #positivo
                else:
                    rect = Rect((meio + 25*x, t_altura*l + 100),(50,44))
                    x += 1
                self._tabuleiro[l].append(Posisao(jogador,cor,rect,t,l))
                if cor == 1:
                    cor = 0
                    jogador = self._jogador1
                else:
                    cor = 1
                    jogador = self._jogador2
            if l == 8:
                pass
            elif l == 9 :
                triangulos -= 2
            else:
                triangulos += 2

#prox jogador
    def habilitarOutroJogador(self):
        if self._jogadorVez == self._jogador1:
            self._jogadorVez = self._jogador2
        else:
            self._jogadorVez = self._jogador1

#movimentacao peca
    def efetuarMovimentacaoPeca(self, peca, pos):
        pos.peca = peca.peca
        peca.peca = None

    def avaliarPosicao(self, peca, pos):
        valida = False
        #posicao vazia
        if pos.peca == None:
            #mesma cor
            if peca.cor == pos.cor:
                posicoesValidas = self.posicoesAdjacentes(peca, 'V')           
                if pos in posicoesValidas:
                    valida = True
        return valida  

#captura peca  
    def avaliarCapturas(self, pos):
        notificacao = None
        if self.verificaCapturaAdversario(pos):
            notificacao = 3
        else:
            if self.verificaCapturaJogador(pos):
                notificacao = 4
        return notificacao

    def verificaCapturaAdversario(self, pos):
        #verifica se o movimento do jogador ocasionou uma captura de peca do adversario
        captura = False
    
        if pos.cor == 0:
            cap = 11
            capAdv = 22 
        else:
            cap = 22
            capAdv = 11 
       
        pos_adjJ = self.posicoesAdjacentes(pos, 'A')

        pos_cont = 0
        for _ in range(len(pos_adjJ)):
            if pos_adjJ[pos_cont].peca != None:
                pos_adjA = self.posicoesAdjacentes(pos_adjJ[pos_cont], 'A')

                pecas = 0
                cont_cap = 0
                for p in pos_adjA:
                    if p.peca != None:
                        pecas += 1
                        if p.peca == cap:
                            cont_cap += 1
                if self.verificaPecaLimiteTabuleiro(pos_adjJ[pos_cont]):
                    if pecas == 2 and cont_cap >= 1:
                        captura = True
                        break
                elif pos_adjJ[pos_cont].peca == capAdv and pecas == 3 and cont_cap >= 1:
                    captura = True
                    break
                elif not(pos_adjJ[pos_cont].peca == capAdv) and pecas == 3:
                    captura = True
                    break
                else:
                    pos_cont += 1
            else:
                pos_cont += 1
        if captura:
            return self.realizarCapturaPeca(pos_adjJ[pos_cont])

    def verificaCapturaJogador(self, pos):
        #verifica se o movimento do jogador ocasionou uma captura da sua peca
        captura = False

        cor = pos.cor
        if cor == 0:
            cap = 11
            capAdv = 22 
        else:
            cap = 22
            capAdv = 11 

        pos_adjJ = self.posicoesAdjacentes(pos, 'A')    

        pecas = 0
        cont_cap = 0
        for p in pos_adjJ:
            if p.peca != None:
                pecas += 1
                if p.peca == capAdv:
                    cont_cap += 1
        if self.verificaPecaLimiteTabuleiro(pos):
            if pecas == 2 and cont_cap >= 1:
                captura = True
        elif pos.peca == cap and pecas == 3 and cont_cap >= 1:
            captura = True
        elif not(pos.peca == cap) and pecas == 3:
            captura = True

        if captura:
            return self.realizarCapturaPeca(pos)
 
    def realizarCapturaPeca(self, pos):
        pos.jogador.totalPecas -= 1
        pos.peca = None
        return True

#avalia encerramento
    def avaliarEncerramentoPartida(self):
        #verifica a existencia de um vencedor
        j1 = self._jogador1.totalPecas <= 2
        j2 = self._jogador2.totalPecas <= 2
        if j1:
            self._vencedor = self._jogador2 
        elif j2 :
            self._vencedor = self._jogador1
            
        if self._vencedor != None:
            return True

#metodos auxiliares            
    def verificaPecaLimiteTabuleiro(self, pos):
        col = pos.col
        linha = pos.linha
        cor = pos.cor

        limite = False

        if linha == 0 and cor == 0:
            limite = True
        elif linha == 10 and cor == 1 :
            limite = True
        elif col == 0 :
            limite = True
        else:
            if linha <= 8:
                l = 0
                c = 4
                for i in range(9):
                    if l == linha and col == c:
                        limite = True
                        break
                    else:
                        l += 1
                        c += 2
            else:
                if (linha == 9 and col == 20) or (linha == 10 and col == 18):
                    limite = True

        return limite

    def arestaPosicoesAdjacentes(self, pos):
        #posicoes adjacentes as arestas do triangulo
        #pos que pertencem ao adversario
        l = pos.linha
        c = pos.col
        
        if pos.cor == 0:
            #pretas
            if l <= 8:
                cols = [(l,c+1),(l,c-1),
                (l-1,c-1)]
            elif l == 9:
                cols = [(l,c+1),(l,c-1),
                (l-1,c)]
            else:
                cols = [(l,c+1),(l,c-1),
                (l-1,c+1)]
        else:
            #brancas
            if l < 8:
                cols = [(l,c+1),(l,c-1),
                (l+1,c+1)]
            elif l == 8:
                cols = [(l,c+1),(l,c-1),
                (l+1,c)]
            elif l >= 9:
                cols = [(l,c+1),(l,c-1),
                (l+1,c-1)]

        return cols

    def verticePosicoesAdjacentes(self, pos):
        #pos adjacentes ao vertice do triangulo
        #pos para onde pode mover a peca
        l = pos.linha
        c = pos.col
        if l < 8:
            cols = [(l,c+2),(l,c-2),
            (l+1,c),(l+1,c+2),
            (l-1,c), (l-1,c-2)]
        elif l == 8:
            cols = [(l,c+2),(l,c-2),
            (l+1,c+1),(l+1,c-1),
            (l-1,c),(l-1,c-2)]
        elif l == 9:
            cols = [(l,c+2),(l,c-2),
            (l+1,c),(l+1,c-2),
            (l-1,c+1),(l-1,c-1)]
        else:
            cols = [(l,c+2),(l,c-2),
            (l+1,c),(l+1,c-2),
            (l-1,c),(l-1,c+2)]

        return cols

    def posicoesAdjacentes(self, pos, tipo):
        # V - vertice
        # A - aresta
        if tipo == 'V':
            cols = self.verticePosicoesAdjacentes(pos)
        else:
            cols = self.arestaPosicoesAdjacentes(pos)

        pos = []
        for i in cols:
            l,c = i
            if(l>=0 and c >= 0):
                try:
                    pos.append(self._tabuleiro[l][c])
                except IndexError:
                    pass

        return pos
