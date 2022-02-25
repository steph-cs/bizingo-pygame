import re
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
        

    def jogadorVez(self):
        return self._jogadorVez
  
    def matriz(self):
        return self._tabuleiro

    def jogador1(self):
        return self._jogador1

    def jogador2(self):
        return self._jogador2
    
    def vencedor(self):
        return self._vencedor

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
        j1 = self._jogador1.totalPecas <= 2
        j2 = self._jogador2.totalPecas <= 2
        if j1:
            self._vencedor = self._jogador2
            return True
        elif j2 :
            self._vencedor = self._jogador1
            return True
    
    def avaliarCapturas(self, pos):
        if self.verificaCapturaAdversario(pos):
            return 3
        else:
            if self.verificaCapturaJogador(pos):
                return 4

    def verificaCapturaAdversario(self, pos):
        #verifica se o movimento do jogador ocasionou uma captura de peca do adversario
        cor = pos.cor
        if cor == 0:
            cap = 11
            capAdv = 22 
        else:
            cap = 22
            capAdv = 11 
       
        pos_adjP = self.pecaPosicoesAdjacentes(pos)
        pos_cont = 0
        for _ in range(len(pos_adjP)):
            if pos_adjP[pos_cont].peca != None:
                pos_adjB = self.pecaPosicoesAdjacentes(pos_adjP[pos_cont])
               
                pecas = 0
                cont_cap = 0
                for p in pos_adjB:
                    if p.peca != None:
                        pecas += 1
                        if p.peca == cap:
                            cont_cap += 1
                if self.verificaPecaLimiteTabuleiro(pos_adjP[pos_cont]):
                    if pecas == 2 and cont_cap >= 1:
                        return self.realizarCapturaPeca(pos_adjP[pos_cont])
                elif pos_adjP[pos_cont].peca == capAdv and pecas == 3 and cont_cap >= 1:
                    return self.realizarCapturaPeca(pos_adjP[pos_cont])
                elif not(pos_adjP[pos_cont].peca == capAdv) and pecas == 3:
                    return self.realizarCapturaPeca(pos_adjP[pos_cont])
                else:
                    pos_cont += 1
            else:
                pos_cont += 1
 
    def realizarCapturaPeca(self, pos):
        pos.jogador.totalPecas -= 1
        pos.peca = None
        return True

    def verificaCapturaJogador(self, pos):
        #verifica se o movimento do jogador ocasionou uma captura de peca do adversario
        cor = pos.cor
        if cor == 0:
            cap = 11
            capAdv = 22 
        else:
            cap = 22
            capAdv = 11 

        pos_adjP = self.pecaPosicoesAdjacentes(pos)    
        pos_cont = 0
        for _ in range(len(pos_adjP)):
            pecas = 0
            cont_cap = 0
            for p in pos_adjP:
                if p.peca != None:
                    pecas += 1
                    if p.peca == capAdv:
                        cont_cap += 1
            if self.verificaPecaLimiteTabuleiro(pos):
                if pecas == 2 and cont_cap >= 1:
                    return self.realizarCapturaPeca(pos)
            elif pos.peca == cap and pecas == 3 and cont_cap >= 1:
                return self.realizarCapturaPeca(pos)
            elif not(pos.peca == cap) and pecas == 3:
                return self.realizarCapturaPeca(pos)
            else:
                pos_cont += 1
            
           
    def verificaPecaLimiteTabuleiro(self, pos):
        col = pos.col
        linha = pos.linha
        cor = pos.cor

        if linha == 0 and cor == 0:
            return True
        elif linha == 10 and cor == 1 :
            return True
        elif col == 0 :
            return True
        else:
            
            if linha <= 8:
                l = 0
                c = 4
                for i in range(9):
                    if l == linha and col == c:
                        return True
                    else:
                        l += 1
                        c += 2
            else:
                if (linha == 9 and col == 20) or (linha == 10 and col == 18):
                    return True
              
    def pecaPosicoesAdjacentes(self, pos):
        linha = pos.linha
        col = pos.col
        cor = pos.cor
        if cor == 0:
            if self.verificaPecaLimiteTabuleiro(pos):
                if linha == 0:
                    pos_adjP = [self.matriz()[linha][col -1]
                        ,self.matriz()[linha][col +1]
                    ]
                else:
                    if pos.col == 0:
                        pos_AdjP_Linha = {
                            9 : [self.matriz()[linha-1][col]
                                ,self.matriz()[linha][col +1]
                                ],
                            10 : [self.matriz()[linha-1][col+1]
                                ,self.matriz()[linha][col +1]
                                ]
                        }
                        pos_adjP = pos_AdjP_Linha[linha]
                    else:
                        if linha == 9:
                            pos_adjP = [self.matriz()[linha-1][col]
                                ,self.matriz()[linha][col -1]
                            ]
                        else:
                            pos_adjP =[self.matriz()[linha-1][col+1]
                                ,self.matriz()[linha][col -1]
                            ]
            else:
                if linha <= 8:
                    pos_adjP = [self.matriz()[linha-1][col -1]
                        ,self.matriz()[linha][col -1]
                        ,self.matriz()[linha][col +1]
                        ]
                else:
                    pos_AdjP_Linha = {
                        8 : [self.matriz()[linha-1][col -1]
                            ,self.matriz()[linha][col -1]
                            ,self.matriz()[linha][col +1]
                            ],
                        9 : [self.matriz()[linha-1][col]
                            ,self.matriz()[linha][col -1]
                            ,self.matriz()[linha][col +1]
                            ],
                        10 : [self.matriz()[linha-1][col+1]
                            ,self.matriz()[linha][col -1]
                            ,self.matriz()[linha][col +1]
                            ]
                    }
                    pos_adjP = pos_AdjP_Linha[linha]
        else:
            if self.verificaPecaLimiteTabuleiro(pos):
                if linha < 8:
                    if pos.col == 0:
                        pos_adjP = [self.matriz()[linha+1][col +1]
                                ,self.matriz()[linha][col +1]
                        ]
                    else:
                        pos_adjP = [self.matriz()[linha+1][col +1]
                            ,self.matriz()[linha][col -1]
                        ]
                elif linha == 8:
                    if pos.col == 0:
                        pos_adjP = [self.matriz()[linha+1][col]
                                ,self.matriz()[linha][col +1]
                        ]
                    else:
                        pos_adjP = [self.matriz()[linha+1][col]
                            ,self.matriz()[linha][col -1]
                        ]
                else:
                    pos_adjP = [self.matriz()[linha][col -1]
                            ,self.matriz()[linha][col +1]
                    ]
            else:
                if linha < 8:
                    pos_adjP = [self.matriz()[linha+1][col+1]
                    ,self.matriz()[linha][col -1]
                    ,self.matriz()[linha][col +1]
                    ]
                else:
                    if linha == 8:
                        pos_adjP = [self.matriz()[linha+1][col]
                            ,self.matriz()[linha][col -1]
                            ,self.matriz()[linha][col +1]
                            ]
                    else:
                        pos_adjP = [self.matriz()[linha+1][col-1]
                            ,self.matriz()[linha][col -1]
                            ,self.matriz()[linha][col +1]
                            ]
        return pos_adjP
