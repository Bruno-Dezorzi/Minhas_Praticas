#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>

#define PONTOS_MAXIMOS_POR_RODADA 1000

// Função para gerar um número aleatório
int gerar_numero_aleatorio(int min, int max) {
    return rand() % (max - min + 1) + min;
}

// Função para realizar um chute
int chutar() {
    while (1) {
        int chute;
        printf("Qual é o seu chute?\n");
        printf("Digite o seu chute por favor: ");
        scanf("%d", &chute);

        if (chute < 0) {
            printf("Não é permitido números negativos\n");
            printf("---------------\n");
        } else {
            printf("Chute registrado.\n");
            printf("---------------\n");
            return chute;
        }
    }
}

// Função principal do jogo
void adivinha(int pontosmaximo, double *pontuacao, int *rodadas) {
    double calculo;

    while (1) {
        int min = 0, max = 10;
        int numerosecreto = gerar_numero_aleatorio(min, max);
        int tentativas, escolha;
        bool mostrar_numero;

        printf("Escolha a quantidade de tentativas: ");
        scanf("%d", &tentativas);

        printf("Mostrar número secreto? (1 = sim, 0 = não): ");
        scanf("%d", &escolha);
        mostrar_numero = (escolha != 0);

        if (mostrar_numero) {
            printf("O número %d é o secreto. Não conta para ninguém!\n", numerosecreto);
        }

        printf("Chances atuais: %d\n", tentativas);

        for (int i = 1; i <= tentativas; i++) {
            int chances = tentativas - i;
            int chute = chutar();
            int acertou = (chute == numerosecreto);

            if (acertou) {
                printf("Você acertou, parabéns!\n");
                calculo = (double)pontosmaximo / i; // pontos de acordo com a tentativa
                *pontuacao += (double)calculo;
                printf("Sua pontuação atual: %2.lf\n", *pontuacao);
                break;
            } else if (numerosecreto > chute) {
                printf("Você errou! Seu chute é menor que o número secreto.\n");
            } else {
                printf("Você errou! Seu chute é maior que o número secreto.\n");
            }

            printf("---------------\n");
            printf("Tentativa %d de %d\n", chances, tentativas);

            if (chances == 0) {
                printf("GAME OVER!\n");
            }
        }

        (*rodadas)++;
        printf("Rodadas jogadas: %d\n", *rodadas);

        printf("\nQuer jogar novamente? (1 = Sim, 0 = Não): ");
        scanf("%d", &escolha);
        if (escolha == 0) {
            break;
        }
    }
}

int main() {
    system("chcp 65001 > nul"); // UTF-8
    printf("***************************************\n");
    printf("Bem vindo ao nosso jogo de adivinhação\n");
    printf("***************************************\n");


    int segundos = time(0);

    srand(segundos);

    double pontuacao = 0.0;
    int rodadas = 0;

    adivinha(PONTOS_MAXIMOS_POR_RODADA, &pontuacao, &rodadas);

    printf("\nJogo encerrado!\nPontuação final: %2.lf\nRodadas jogadas: %d\n", pontuacao, rodadas);
    return 0;
}
