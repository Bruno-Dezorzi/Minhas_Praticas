#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

void atualizar_contador()
{
    FILE *arquivo = fopen("palavras.txt", "r+");
    if (arquivo == NULL)
    {
        printf("Erro ao abrir o arquivo para atualizar contador.\n");
        return;
    }

    int num = 0;
    fscanf(arquivo, "%d", &num); // lê o número da primeira linha
    num++;                       // incrementa

    // volta o ponteiro para o início do arquivo
    rewind(arquivo);
    fprintf(arquivo, "%d\n", num);

    fclose(arquivo);
}

void adicionapalavra()
{
    char escolha;

    printf("Você quer adicionar uma palavra ao banco de palavras? (S/N): ");
    scanf(" %c", &escolha); // atenção ao espaço antes do %c para ignorar '\n'

    if (toupper(escolha) == 'S')
    {
        char palavra[20];

        printf("Digite a palavra: ");
        scanf("%s", palavra);

        for (int i = 0; i < strlen(palavra); i++)
        {
            palavra[i] = toupper(palavra[i]);
        }

        FILE *f = fopen("palavras.txt", "a");
        if (f == NULL)
        {
            printf("Desculpe, banco de dados não disponível\n");
            exit(1);
        }

        fprintf(f, "%s\n", palavra);
        fclose(f);

        atualizar_contador();

        printf("Obrigado por adicionar a palavra %s ao banco de palavras!\n", palavra);

        printf("Quer adicionar outra palavra? (S/N): ");
        scanf(" %c", &escolha);
        if (toupper(escolha) == 'S')
        {
            adicionapalavra();
        }
    }
}

int main()
{
    system("chcp 65001 > nul"); // UTF-8 no Windows
    adicionapalavra();
    return 0;
}
