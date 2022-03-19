import pygame as pg
from pygame.locals import *

from tabuleiro import Tabuleiro


# t1 - claro - pretas - 1(peca) - 11(cap)
# t2 - escuro - brancas - 2(peca) - 22(cap)
#cores
#clara = [(114, 199, 225),'#72c7e1']
#escura = [(0, 155, 160),'#009BA0']

class interfaceJogador:
    def __init__(self):
        pg.init()
        self._tela = pg.display.set_mode((1000,650))
        
        self._area_selecionada = False
        self._moverPeca = None
        
        self._tabuleiro = Tabuleiro()
        self._tabuleiro.construirMatrizTabuleiro()
        self._matrizTabuleiro = self._tabuleiro.matriz()
        self._jogadorVez = self._tabuleiro.jogadorVez()

#deteccao click tabuleiro
    def point_collide(self, point):
        self.notificacao = None
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
                                if self._area_selecionada:
                                    self.estado = 0
                                    self.atualizarInterface()
                                    self._area_selecionada = False
                                if self._area_selecionada == False:
                                    return c
                            else:
                                
                                if self.selecionarPosicao(c) == 0:
                                    return 0
                                else:
                                    
                                    self._area_selecionada = False             
                if triangulo == self._t2:
                    triangulo = self._t1
                else:
                    triangulo = self._t2

#iniciar jogo/ loop jogo
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
        self.posicionarPecasIniciais()
        self.estado = 0
        self.notificacao = None
        self.exibirEstado()
        while True:
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    if self._tabuleiro.vencedor() == None:
                        pos = self.point_collide(mouse_pos)
                        if pos == 0:
                            pass
                        elif( pos != None):
                            self.selecionarPeca(pos)
            pg.display.flip()

#construcao elementos jogo na interface
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

    def posicionarPecasIniciais(self):
        #criacao na matriz e posicionamento na interface das pecas iniciais
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

    def posicionarPecas(self):
        # posicionamento atual das pecas (*atualizacao interface)
        for l in range(11):
            linha = self._matrizTabuleiro[l]
            for c in range(len(linha)):
                pos = linha[c]
                if pos.peca == None:
                    pass
                elif pos.cor == 0 :
                    if pos.peca == 1:
                        peca = self.peca_t1
                        self._tela.blit(peca, (pos.posicao.x,pos.posicao.y-10))
                    else:
                        cap = self.cap_t1
                        self._tela.blit(cap, (pos.posicao.x,pos.posicao.y-10))
                else:
                    if pos.peca == 2:
                        peca = self.peca_t2
                        self._tela.blit(peca, (pos.posicao.x,pos.posicao.y))
                    else:
                        cap = self.cap_t2
                        self._tela.blit(cap, (pos.posicao.x,pos.posicao.y))

#atualizazao de estado/ interface
    def atualizarInterface(self):
        self._tela.fill((255, 255, 255))
        self.construirTabuleiro()
        self.posicionarPecas()
        self._jogadorVez = self._tabuleiro.jogadorVez()
        self.exibirEstado()

    def exibirEstado(self):            
        font_1 = pg.font.SysFont('Comic Sans MS', 50)
        font_2 = pg.font.SysFont('Comic Sans MS', 40)
        font_3 = pg.font.SysFont('Comic Sans MS', 20)

        title = font_1.render('Bizingo', False, (0, 0, 0))
        vez = font_2.render('Vez de:', False, (0, 0, 0))
        jogador = font_2.render(self._tabuleiro.jogadorVez().nome, False, (0, 0, 0))

        self.atualizarEstado()

        status = font_3.render("Status:", False, (255, 0, 0))
        status_j = font_3.render(self.estadoMsg, False, (255, 0, 0))

        notificacao = font_3.render(self.notificacaoMsg, False, (255, 0, 0))

        pecas_restantes = font_3.render("Peças restantes:", False, (0, 0, 0))
        pecas_j1 = font_3.render("Jogador 1 : {}".format(self._tabuleiro.jogador1().totalPecas), False, (0, 0, 0))
        pecas_j2 = font_3.render("Jogador 2 : {}".format(self._tabuleiro.jogador2().totalPecas), False, (0, 0, 0))

        self._tela.blit(notificacao,(655,70))

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

    def atualizarEstado(self):
        estados = {
            0 : "selecione uma peca",
            1 : "selecione uma posicao"
        }
        notificacoes = {
            None : "",
            1 : "*movimento invalido",
            2 : "*movimento realizado",
            3 : "*peca oponente capturada",
            4 : "*peca capturada pelo oponente"
        }
        self.estadoMsg = estados[self.estado]
        self.notificacaoMsg = notificacoes[self.notificacao]

#selecao peca        
    def selecionarPeca(self, pos):
        if pos.peca != None and pos.jogador == self._jogadorVez:
            self.estado = 1
            self.atualizarInterface()
            if pos.cor == 0:
                peca = self.area_t1
            else:
                peca = self.area_t2
            self._tela.blit(peca, (pos.posicao.x,pos.posicao.y))
            self._area_selecionada = True
            self._moverPeca = pos
            self.exibirPosicoesValidas()

    def exibirPosicoesValidas(self):
        pos = self._moverPeca
        cols = self._tabuleiro.posicoesAdjacentes(pos, 'V')
        for p in cols:
            if p.peca == None:
                if p.cor == 0:
                    cor = (0,0,0)
                else:
                    cor = (255,255,255)
                pg.draw.circle(self._tela,cor,(p.posicao.x + 25,p.posicao.y +22,),5) 

#selecao nova posicao
    def selecionarPosicao(self, pos):
        peca = self._moverPeca
        if self._tabuleiro.avaliarPosicao(peca, pos):
            self.efetuarMovimentacaoPeca(peca, pos)
            self.avaliarCapturas(pos)
            if self.avaliarEncerramentoPartida():
                self.encerrarPartida()
                return 0
            self._tabuleiro.habilitarOutroJogador()
        else:
            self.notificacao = 1
            self.estado = 0
        self._moverPeca =None
        self.atualizarInterface() 
        
    def efetuarMovimentacaoPeca(self, peca,pos):
        self._tabuleiro.efetuarMovimentacaoPeca(peca,pos)
        self.estado = 0
        self.notificacao = 2
        
#captura/ encerramento partida
    def avaliarCapturas(self, pos):
        notificacao = self._tabuleiro.avaliarCapturas(pos)
        if notificacao != None:
            self.notificacao = notificacao

    def avaliarEncerramentoPartida(self):
        return self._tabuleiro.avaliarEncerramentoPartida()

    def encerrarPartida(self):
        self._tela.fill((0,0,0))
        font_1 = pg.font.SysFont('Comic Sans MS', 50)
        jogador = font_1.render("{} ganhou o jogo!".format(self._tabuleiro.vencedor().nome), False, (255,255,255))
        self._tela.blit(jogador,(250,285))
