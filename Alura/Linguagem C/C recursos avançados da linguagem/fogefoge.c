// fogefoge.c
#include <stdio.h>
#include <stdlib.h>
#include "fogefoge.h"
#include "mapa.h"

MAPA m;
POSICAO heroi;

void fantasmas(){
    for(int i=0; i < m.linhas;i++){
        for(int j=0; j < m.colunas;j++){
            if(m.matriz[i][j] == FANTASMA){
                if(ehvalida(&m,i,j+1)){
                    andanomapa(&m,i,j,i,j+1);
                }
            }
        }
    }
}

int acabou() {
	return 0;
}

int ehdirecao(char direcao) {
	return
		direcao == ESQUERDA || 
		direcao == CIMA ||
		direcao == BAIXO ||
		direcao == DIREITA;
}

void move(char direcao) {

	if(!ehdirecao(direcao))	
		return;

	int proximox = heroi.x;
	int proximoy = heroi.y;

	switch(direcao) {
		case ESQUERDA:
			proximoy--;
			break;
		case CIMA:
			proximox--;
			break;
		case BAIXO:
			proximox++;
			break;
		case DIREITA:
			proximoy++;
			break;
	}

	if(!ehvalida(&m, proximox, proximoy))
		return;

	if(!ehvazia(&m, proximox, proximoy))
		return;

	andanomapa(&m, heroi.x, heroi.y, proximox, proximoy);
	heroi.x = proximox;
	heroi.y = proximoy;
}

int main() {
	
	lemapa(&m);
	encontramapa(&m, &heroi, HEROI);

	do {
		imprimemapa(&m);

		char comando;
		scanf(" %c", &comando);

		move(comando);
        fantasmas();

	} while (!acabou());

	liberamapa(&m);
}