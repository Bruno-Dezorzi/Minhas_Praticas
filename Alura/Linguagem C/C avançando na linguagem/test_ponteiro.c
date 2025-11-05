#include <stdio.h>


int main(){

    int var = 15;
    int *ptr;

    printf("EVENTO -> ptr = &var\n");
    printf("\n");

    printf("ANTES:\n");
    printf("conteudo de var = %d\n", var);
    printf("conteudo de ptr = %p\n",ptr);
    printf("endereco de memoria de var = %p\n", &var);
    printf("endereco de memoria do proprio ponteiro = %p\n",&ptr);
    
    
    printf("\n");

    ptr = &var;

    printf("DEPOIS:\n");
    printf("conteudo de var = %d\n", var);
    printf("conteudo de ptr = %p\n",ptr);
    printf("endereco de memoria de var = %p\n", &var);
    printf("endereco de memoria do proprio ponteiro = %p\n",&ptr);
    

    return 0;
}

