from pygame import *
from jogador import Jogador
from posicao import Posisao

class Tabuleiro():
    def __init__(self):
        self._jogador1 = Jogador("t1")
        self._jogador2 = Jogador("t2")

        self._tabuleiro = []

    def matriz(self):
        return self._tabuleiro

    def jogador1(self):
        return self._jogador1

    def jogador2(self):
        return self._jogador2

    def matrizTabuleiro(self):
    
        t_altura = 44
        t_largura = 50
        #meio ponto 325 , x_meio 325 - 25 (metade da largura do triangulo)
        meio = 325 -25
        
        triangulos = 5
        for l in range(11):
            self._tabuleiro.append([])
           
            cor = "t2"
            jogador = self._jogador2
            if l >= 9:
                cor = "t1"
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

                if cor == "t2":
                    cor = "t1"
                    jogador = self._jogador1
                else:
                    cor = "t2"
                    jogador = self._jogador2
                
            if l == 8:
                pass
            elif l == 9 :
                triangulos -= 2
            else:
                triangulos += 2