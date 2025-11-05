#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main()
{

    char quer;
    printf("Você quer adicionar uma nova palavra ao jogo? (S/N) ");
    scanf(" %c", &quer);

    if (toupper(quer) == 'S')
    {
        char novapalavra[20];
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

            for(int i = 0; i < strlen(novapalavra); i++){
                novapalavra[i] = toupper(novapalavra[i]);
            }

            fseek(f, 0, SEEK_END);
            fprintf(f, "\n%s", novapalavra);

            fclose(f);
        }
    }

}
