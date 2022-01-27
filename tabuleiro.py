from pygame import *
from jogador import Jogador
from posicao import Posisao

class Tabuleiro():
    def __init__(self):
        self._jogador1 = Jogador(1)
        self._jogador2 = Jogador(2)

        self._tabuleiro = []

        self._jogadorVez = self._jogador1
        

    def jogadorVez(self):
        return self._jogadorVez
  
    def matriz(self):
        return self._tabuleiro

    def jogador1(self):
        return self._jogador1

    def jogador2(self):
        return self._jogador2

    def matrizTabuleiro(self):
        #construção da matriz do tabuleiro
        t_altura = 44
        t_largura = 50
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
                    self._tabuleiro[l].append(Posisao(jogador,cor,rect,t,l))  
                #neutro
                elif t+1== triangulos//2+1:
                    rect = Rect((meio, t_altura*l + 100),(50,44))
                    self._tabuleiro[l].append(Posisao(jogador,cor,rect,t,l))
                    x = 1
                #positivo
                else:
                    rect = Rect((meio + 25*x, t_altura*l + 100),(50,44))
                    self._tabuleiro[l].append(Posisao(jogador,cor,rect,t,l))
                    x += 1
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

    def habilitarOutroJogador(self):
        if self._jogadorVez == self._jogador1:
            self._jogadorVez = self._jogador2
        else:
            self._jogadorVez = self._jogador1

    def efetuarMovimentacaoPeca(self, peca, pos):
        pos.peca = peca.peca
        peca.peca = None

    def avaliarPosicao(self, peca, pos):
        #posicao vazia
        if pos.peca == None:
            #mesma cor
            if peca.cor == pos.cor:
                cor = peca.cor
                #pretas
                if cor == 0:
                    cols = []
                    if 8 == peca.linha and  pos.linha== 9 or 9 == peca.linha and  pos.linha== 8:
                        cols = [peca.col-1,peca.col+1]
                    else:
                        if peca.linha == pos.linha:
                            cols = [peca.col+2,peca.col-2]
                           
                        elif peca.linha +1  == pos.linha:
                            if peca.linha>8 and pos.linha>8:
                                cols = [peca.col,peca.col-2]
                            else:   
                                cols = [peca.col,peca.col+2]
                            
                        elif peca.linha -1  == pos.linha:
                            if peca.linha>8 and pos.linha>8:
                                cols = [peca.col,peca.col+2]
                            else:   
                                cols = [peca.col,peca.col-2]
                    
                    if pos.col in cols:
                        return True
                #brancas
                else:
                    cols = []
                    if 8 == peca.linha and  pos.linha== 9 or 9 == peca.linha and  pos.linha== 8:
                        cols = [peca.col-1,peca.col+1]
                    else:
                        if peca.linha == pos.linha:
                            cols = [peca.col+2,peca.col-2]
                           
                        elif peca.linha +1  == pos.linha:
                            if peca.linha>8 and pos.linha>8:
                                cols = [peca.col,peca.col-2]
                            else:   
                                cols = [peca.col,peca.col+2]
                            
                        elif peca.linha -1  == pos.linha:
                            if peca.linha>8 and pos.linha>8:
                                cols = [peca.col,peca.col+2]
                            else:   
                                cols = [peca.col,peca.col-2]
                           
                    if pos.col in cols:
                        return True
        return False  


    def avaliarEncerramentoPartida(self):
        #verifica a existencia de um vencedor
        vencedor = None
        j1 = self._jogador1.totalPecas <= 2
        j2 = self._jogador2.totalPecas <= 2
        if j1:
            vencedor = self._jogador1
        elif j2 :
            vencedor = self._jogador1
        return vencedor
    
    def avaliarCapturas(self, pos):
        self.verificaCapturaJogador(pos)
        self.verificaCapturaAdversario(pos)

    def verificaCapturaJogador(self, pos):
        #apos verificar a capturaAdversario e nao houve capturas
        #verifica se o movimento do jogador ocasionou a captura de sua peca para o adversario
        pass

    def verificaCapturaAdversario(self, pos):
        #verifica se o movimento do jogador ocasionou uma captura de peca do adversario
        pass
