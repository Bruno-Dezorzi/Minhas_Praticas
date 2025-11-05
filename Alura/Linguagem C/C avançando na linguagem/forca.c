#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "forca.h"
#include <time.h>

char palavrasecreta[TAMANHO_PALAVRA];
char chutes[26];
int chutesdados = 0;

void abertura()
{
    printf("************************\n");
    printf("*****Jogo da Forca******\n");
    printf("************************\n");
}

void chuta()
{

    char chute;
    printf("Qual letra? ");
    scanf(" %c", &chute);

    chutes[chutesdados] = toupper(chute);
    chutesdados++;
}

void desenhaforca()
{
    for (int i = 0; i < strlen(palavrasecreta); i++)
    {

        int achou = jachutou(palavrasecreta[i]);

        if (achou)
        {
            printf("%c", palavrasecreta[i]);
        }
        else
        {
            printf(" _ ");
        }
    }
    printf("\n");
}

int ganhou()
{
    for (int i = 0; i < strlen(palavrasecreta); i++)
    {
        if (!jachutou(palavrasecreta[i]))
        {
            return 0;
        }
    }

    return 1;
}

int enforcou()
{

    int erros = 0;

    for (int i = 0; i < chutesdados; i++)
    {

        int existe = 0;

        for (int j = 0; j < strlen(palavrasecreta); j++)
        {
            if (chutes[i] == palavrasecreta[j])
            {
                existe = 1;
                break;
            }
        }

        if (!existe)
            erros++;
    }
    return erros >= 5;
}

int jachutou(char letra)
{

    int achou = 0;
    for (int j = 0; j < chutesdados; j++)
    {
        if (chutes[j] == letra)
        {
            (achou) = 1;
            break;
        }
    }

    return achou;
}

void adicionapalavra()
{
    char quer;
    printf("Você quer adicionar uma nova palavra ao jogo? (S/N) ");
    scanf(" %c", &quer);

    if (toupper(quer) == 'S')
    {
        char novapalavra[TAMANHO_PALAVRA];
        printf("Qual a nova palavra: ");
        scanf("%s", novapalavra);

        FILE *f = fopen("palavras.txt", "r+");

        if (f == 0)
        {
            printf("Desculpe, banco de dados não disponível\n");
            exit(1);
        }
        else
        {

            int qtd;

            fscanf(f, "%d", &qtd);
            qtd++;

            fseek(f, 0, SEEK_SET);
            fprintf(f, "%d", qtd);

            for (int i = 0; i < strlen(novapalavra); i++)
            {
                novapalavra[i] = toupper(novapalavra[i]);
            }

            fseek(f, 0, SEEK_END);
            fprintf(f, "\n%s", novapalavra);

            fclose(f);
        }
    }
}

void escolhepalavra()
{

    FILE *f;

    f = fopen("palavras.txt", "r");

    if (f == 0)
    {
        printf("Desculpe, banco de dados não disponível\n");
        exit(1);
    }
    else
    {
        int qtddepalavras;
        fscanf(f, "%d", &qtddepalavras);

        srand(time(0));
        int randomico = rand() % qtddepalavras;

        for (int i = 0; i <= randomico; i++)
        {
            fscanf(f, "%s", palavrasecreta);
        }
    }

    fclose(f);
}

void forca()
{
    escolhepalavra(palavrasecreta);

    // Reinicia o estado do jogo
    memset(chutes, 0, sizeof(chutes)); // zera o vetor de chutes
    chutesdados = 0;                   // zera o contador

    do
    {
        desenhaforca(palavrasecreta, chutes, chutesdados);
        chuta(chutes, &chutesdados);

    } while (!ganhou() && !enforcou());

    if (ganhou())
    {
        printf("Você ganhou! A palavra é %s\n", palavrasecreta);
    }
    else
    {
        printf("Você perdeu! A palavra é %s\n", palavrasecreta);
    }
}

int main()
{

    system("chcp 65001 > nul"); // UTF-8

    abertura();

    char jogando = 'S';

    while (toupper(jogando) == 'S')
    {
        forca();
        printf("Quer jogar novamente? (S/N): ");
        scanf(" %c", &jogando);
    }

    adicionapalavra();
    printf("Obrigado por jogar!");
}