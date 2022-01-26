import pygame as pg
from pygame.locals import *

from tabuleiro import Tabuleiro


# t1 - claro - pretas - 1(peca) - 11(cap)
# t2 - escuro - brancas - 2(peca) - 22(cap)
#cores
#clara = [(114, 199, 225),'#72c7e1']
#escura = [(0, 155, 160),'#009BA0']

class AtorJogador:
    def __init__(self):
        pg.init()
        self._tela = pg.display.set_mode((1000,650))
        
        self._area_selecionada = False
        self._moverPeca = None

        self._tabuleiro = Tabuleiro()
        self._tabuleiro.matrizTabuleiro()
        self._matrizTabuleiro = self._tabuleiro.matriz()

    def point_collide(self, point):
        self.notificacao = 0
        for linha in range(len(self._matrizTabuleiro)):
            if linha <= 8:
                triangulo = self._t2
            else:
                triangulo = self._t1
            for c in self._matrizTabuleiro[linha]:
                rect = c.posicao
                color = None
                
                if triangulo == self._t2:
                    color = (0, 155, 160)
                else:
                    color = (114, 199, 225)

                x, y = point
                x -= rect.x
                y -= rect.y

                #detects if click hits the image
                if 0 <= x < 50:
                    if 0 <= y < 44:
                        #detects if color at clicking position != colorkey-color
                        if triangulo.get_at((x,y))[0:3] == color:
                            if self._moverPeca == None:
                                if self._area_selecionada != False:
                                    self.estado = 0
                                    self.atualizarInterface()
                                    self._area_selecionada = False
                                if self._area_selecionada == False:
                                    return c
                            else:
                                self.selectPosicao(c)
                                self._moverPeca =None
                                self.atualizarInterface()
                                self._area_selecionada = False
                               
                if triangulo == self._t2:
                    triangulo = self._t1
                else:
                    triangulo = self._t2

    def atualizarInterface(self):
        self._tela.fill((255, 255, 255))
        self.construirTabuleiro()
        self.posPecas()
        self.exibirEstado()

    def atualizarEstado(self):
        estados = {
            0 : "selecione uma peca",
            1 : "selecione uma posicao"
        }
        notificacoes = {
            0 : "",
            1 : "*movimento invalido",
            2 : "*movimento realizado"
        }
        self.estadoMsg = estados[self.estado]
        self.notificacaoMsg = notificacoes[self.notificacao]

    def exibirEstado(self):            
        font_1 = pg.font.SysFont('Comic Sans MS', 50)
        font_2 = pg.font.SysFont('Comic Sans MS', 40)
        font_3 = pg.font.SysFont('Comic Sans MS', 20)

        title = font_1.render('Bizingo', False, (0, 0, 0))
        vez = font_2.render('Vez de:', False, (0, 0, 0))
        jogador = font_2.render(self._tabuleiro.vez().nome, False, (0, 0, 0))

        self.atualizarEstado()

        self.estadoM = self._tabuleiro.estado()
        status = font_3.render("Status:", False, (255, 0, 0))
        status_j = font_3.render(self.estadoMsg, False, (255, 0, 0))

        notificacao = font_3.render(self.notificacaoMsg, False, (255, 0, 0))

        pecas_restantes = font_3.render("Peças restantes:", False, (0, 0, 0))
        pecas_j1 = font_3.render("Jogador 1 : {}".format(self._tabuleiro.jogador1().totalPecas), False, (0, 0, 0))
        pecas_j2 = font_3.render("Jogador 2 : {}".format(self._tabuleiro.jogador2().totalPecas), False, (0, 0, 0))

        self._tela.blit(notificacao,(730,70))

        self._tela.blit(title,(250,0))

        self._tela.blit(vez,(730,150))
        self._tela.blit(jogador,(700,200))

        self._tela.blit(status,(770,300))
        self._tela.blit(status_j,(710,320))

        self._tela.blit(pecas_restantes,(720,400))
        self._tela.blit(pecas_j1,(700,430))
        self._tela.blit(pecas_j2,(700,460))

        pg.draw.line(self._tela,(0,0,0),(650,50),(650,600),5)
        pg.draw.line(self._tela,(0,0,0),(950,50),(950,600),5)

        pg.draw.line(self._tela,(0,0,0),(650,50),(950,50),5)
        pg.draw.line(self._tela,(0,0,0),(650,600),(950,600),5)

    def construirTabuleiro(self):
        for l in range(11):
            tr = self._t2
            if l >= 9:
                tr = self._t1
            for c in self._matrizTabuleiro[l]:
                self._tela.blit(tr, (c.posicao.x,c.posicao.y))
                if tr == self._t2:
                    tr = self._t1
                else:
                    tr = self._t2

    def iniciarJogo(self):
        self._tela.fill((255, 255, 255))
        pg.display.set_caption("Bizingo")
        self._t1 = pg.image.load('imgs/t1.png')
        self._t2 = pg.image.load('imgs/t2.png')

        self.area_t2 = pg.image.load('imgs/area_selecionada 50x44.png')
        self.area_t1 = pg.image.load('imgs/area_selecionada(1) 50x44.png')

        self.peca_t1 = pg.image.load('imgs/peca_preta 50x44.png')
        self.cap_t1 = pg.image.load('imgs/cap_preta 50x44.png')
        self.peca_t2 = pg.image.load('imgs/peca_branca 50x44.png')
        self.cap_t2 = pg.image.load('imgs/cap_branca 50x44.png')
        
        
        self.construirTabuleiro()
        self.pecas_iniciais()
        self.estado = 0
        self.notificacao = 0
        self.exibirEstado()
        while True:
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = self.point_collide(mouse_pos)
                    if( pos != None):
                        c =self.selectPeca(pos)
                        if c != None:
                            self._moverPeca = c
                            self.posValidas()
            pg.display.flip()

    def pecas_iniciais(self):
        for p in range(2):
            if p == 0:
                #brancas
                peca= self.peca_t2
                cap = self.cap_t2
                x_i = 2
                x_f = 6
                for i in range(2,6):
                    for c in range(len(self._matrizTabuleiro[i])):
                        if x_i<=c<=x_f and c%2 == 0:
                            rect = self._matrizTabuleiro[i][c].posicao
                            if (i == 5) and (c == 4 or c == 10):
                                self._matrizTabuleiro[i][c].peca = 22
                                self._tela.blit(cap, (rect.x,rect.y))
                            else:  
                                self._matrizTabuleiro[i][c].peca = 2
                                self._tela.blit(peca, (rect.x,rect.y ))
                    x_f += 2
            else:
                #pretas
                peca= self.peca_t1
                cap = self.cap_t1
                x_i = 1
                x_f = 15
                for i in range(7,10):
                    if i < 9:
                        x_i += 2
                        for c in range(len(self._matrizTabuleiro[i])):
                            if x_i<=c<=x_f and c%2 != 0:
                                rect = self._matrizTabuleiro[i][c].posicao
                                if (i == 7) and (c == 5 or c == 13):
                                    self._matrizTabuleiro[i][c].peca = 11
                                    self._tela.blit(cap, (rect.x,rect.y- 10))
                                else:
                                    self._matrizTabuleiro[i][c].peca = 1    
                                    self._tela.blit(peca, (rect.x,rect.y- 10))       
                    else:
                        x_i += 1
                        x_f -= 1
                        for c in range(len(self._matrizTabuleiro[i])):
                            if x_i<=c<=x_f and c%2 == 0:
                                rect = self._matrizTabuleiro[i][c].posicao
                                self._matrizTabuleiro[i][c].peca = 1
                                self._tela.blit(peca, (rect.x,rect.y- 10))

    def posPecas(self):
        for l in range(11):
            linha = self._matrizTabuleiro[l]
            for c in range(len(linha)):
                coluna = linha[c]
                if coluna.peca == None:
                    pass
                elif coluna.peca == 1 or coluna.peca == 11 :
                    if coluna.peca == 1:
                        peca = self.peca_t1
                        self._tela.blit(peca, (coluna.posicao.x,coluna.posicao.y-10))
                    else:
                        cap = self.cap_t1
                        self._tela.blit(cap, (coluna.posicao.x,coluna.posicao.y-10))
                else:
                    if coluna.peca == 2:
                        peca = self.peca_t2
                        self._tela.blit(peca, (coluna.posicao.x,coluna.posicao.y))
                    else:
                        cap = self.cap_t2
                        self._tela.blit(cap, (coluna.posicao.x,coluna.posicao.y))
               
    def selectPeca(self, pos):
        #verificar se tem uma peca na posicao do rect
        # se sim... captar outro clique
        # vreificar se esta vazio
        # verificra se é valido
        for l in self._matrizTabuleiro:
            for c in l:
                if c.posicao == pos.posicao and c.peca != None:
                    self.estado = 1
                    self.atualizarInterface()
                    if pos.cor == 0:
                        peca = self.area_t1
                    else:
                        peca = self.area_t2
                    self._tela.blit(peca, (pos.posicao.x,pos.posicao.y))
                    self._area_selecionada = True
                    return c

    def selectPosicao(self, pos):
        #posicao vazia
        if pos.peca == None:
            peca = self._moverPeca
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
                        self._tabuleiro.efetuarMovimentacaoPeca(peca,pos)
                        self.moverPeca()
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
                        self.moverPeca(peca,pos)
                        return True
        self.notificacao = 1
        self.estado = 0
        
    def moverPeca(self):
        self.estado = 0
        self.notificacao = 2
        
    def posValidas(self):
        pos = self._moverPeca
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
 
        for i in cols:
            l,c = i
            if(l>=0 and c >= 0):
                try:
                    p = self._matrizTabuleiro[l][c]
                    if p.peca == None:
                        if p.cor == 0:
                            cor = (0,0,0)
                        else:
                            cor = (255,255,255)
                        pg.draw.circle(self._tela,cor,(p.posicao.x + 25,p.posicao.y +22,),5) 
                except IndexError:
                    pass
            
