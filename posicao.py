from pygame import rect
from jogador import Jogador

class Posisao():
    def __init__(self, jogador:Jogador, cor:int,posicao:rect, col:int, linha:int, peca:int=None):
        self._jogador = jogador
        self._cor = cor
        self._posicao = posicao
        self._col = col
        self._linha = linha
        self._peca = peca

    @property
    def jogador(self):
        return self._jogador
    
    @jogador.setter
    def jogador(self, jogador:jogador):
        self._jogador = jogador

    @property
    def cor(self):
        return self._cor

    @property
    def posicao(self):
        return self._posicao
    
    @property
    def col(self):
        return self._col

    @property
    def linha(self):
        return self._linha
    
    @property
    def peca(self):
        return self._peca
    
    @peca.setter
    def peca(self, peca):
        self._peca = peca
