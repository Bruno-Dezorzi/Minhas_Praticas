#include <stdio.h>
#include <stdlib.h>

void calcular(int *c){
    printf("%d <- Dentro da função\n", (*c));
    (*c)++;
    printf("%d <- Dentro da função\n", (*c));
}

void soma(int *num,int a, int b){
    (*num) = a + b;
}

int soma_int(int a,int b){
    int num = a + b;
    return num;
}

int main(){

    system("chcp 65001 > nul"); 
    

    int c = 10;

    
    printf("%d <- Fora da função antes dela\n", c);
    calcular(&c);
    printf("%d <- Fora da função depois dela\n", c);

    
    int num;
    soma(&num,10,15);
    printf("%d\n",num);

    int num_2;
    num_2 = soma_int(10,15);
    //printf("%d\n",num_2);



    return 0;
}