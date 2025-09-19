#include <stdio.h>
#include <time.h>

void demonstrar_ponteiros(){
    int numero1 = 1;          // Cria uma variável inteira chamada numero1 com valor 1
    int *numero2 = &numero1;  // numero2 é um ponteiro que armazena o endereço de numero1

    // Mostrar o valor de numero1
    printf("Valor de numero1: %d\n", numero1);

    // Mostrar o endereço de numero1
    printf("Endereco de numero1: %p\n", &numero1);

    // Mostrar o que está dentro de numero2 (o endereço armazenado nele)
    printf("Valor de numero2 (endereco guardado): %p\n", numero2);

    // Mostrar o endereço de numero2 em si (onde o ponteiro está na memória)
    printf("Endereco de numero2: %p\n", &numero2);

    // Mostrar o valor armazenado no endereço que numero2 aponta
    printf("Valor apontado por numero2: %d\n", *numero2);
}

void testar_funcao_time(){
    time_t agora = time(0);
    printf("Timestamp atual: %ld", agora);
}

int main(){
    
    // demonstrar_ponteiros();
    // testar_funcao_time();

    return 0;
}
