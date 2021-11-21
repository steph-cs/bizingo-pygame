

class Jogador:
    def __init__(self, peca:int):
        self._peca = peca
        self._nome = ("Jogador 1" if peca == 1 else "Jogador 2")
        self._totalPecas = 18

    @property
    def peca(self):
        return self._peca
    
    @property
    def nome(self):
        return self._nome

    @property
    def totalPecas(self):
        return self._totalPecas

    @totalPecas.setter
    def totalPecas(self, totalPecas: int):
        self._totalPecas = totalPecas



