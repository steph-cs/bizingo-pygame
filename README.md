# Bizingo
Trabalho da disciplina Análise e Projeto de Sistemas da Universidade Federal de Santa Catarina (UFSC)
Bizingo é um jogo de tabuleiro, de dois jogadores, cujo objetivo é
reduzir as peças do oponente a 2 (dois), o jogo contém dois tipos de peças: as
peças normais (16 por jogador) e o capitão (2 por jogador).

## Requisitos
* python - v 3.8
* pygame - v 2.0

## Movimentação das peças:
Cada jogador em seu turno move uma de suas peças, obedecendo às
seguintes regras: podem mover para qualquer um dos triângulos
vizinhos (que tenha um vértice em comum), da sua própria cor e que
esteja vazio.

## Tipos de Captura:
### Captura por custódia:
- O jogador captura uma peça inimiga (exceto capitão)
cercando-a em três lados, com 3 peças suas qualquer.
- O capitão é capturado cercando-o pelos três lados, desde
que, pelo menos uma das peças seja o capitão.
### Movimentação:
- Caso um jogador mova sua peça para uma casa cercada por
três peças do adversário ela deve ser capturada, a menos que,
durante o movimento, o jogador capture uma peça inimiga.
### Captura:
- Um jogador pode capturar uma peça inimiga na borda
do tabuleiro cercando-a com apenas duas peças, mas
uma delas deve ser um capitão.

### Desenvolvido com Python; biblioteca Pygame
### [Modelagem UML e Especificação de Requisitos](https://drive.google.com/drive/folders/1krmnWdyLZ1MKKra8rcMVhRIcrOe7pdrf?usp=sharing)
Referências
- https://youtu.be/n03VBTZ4qgI
- https://www.ludopedia.com.br/jogo/bizingo
