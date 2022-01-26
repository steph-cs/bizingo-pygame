from pygame import *
from jogador import Jogador
from posicao import Posisao

class Tabuleiro():
    def __init__(self):
        self._jogador1 = Jogador(1)
        self._jogador2 = Jogador(2)

        self._tabuleiro = []

        self._vez = self._jogador1
        

    def vez(self):
        return self._vez
    
    def getEstado(self):
        e = self._estado
        estados = {
            0 : "aguardando jogada",
            1 : "nenhuma peca foi capturada",
            2 : "peca do oponente capturada",
            3 : "peca capturada pelo oponente ",
            4 : self.encerrarPartida()
        }
        return estados[e]
    
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

    def efetuarMovimentacaoPeca(self, peca, pos):
        pos.peca = peca.peca
        peca.peca = None

    def verificaVencedor(self):
        #verifica a existencia de um vencedor
        j1 = self._jogador1.totalPecas <= 2
        j2 = self._jogador2.totalPecas <= 2
        if  j1 or j2:
            return True

    def verificaCapturaJogador(self):
        #apos verificar a capturaAdversario e nao houve capturas
        #verifica se o movimento do jogador ocasionou a captura de sua peca para o adversario
        pass

    def verificaCapturaAdversario(self):
        #verifica se o movimento do jogador ocasionou uma captura de peca do adversario
        pass

    def encerrarPartida(self):
        pass