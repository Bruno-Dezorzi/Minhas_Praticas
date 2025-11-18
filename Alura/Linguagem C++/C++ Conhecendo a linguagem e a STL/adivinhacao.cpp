#include <iostream>
#include <windows.h>
#include <random>
#include <chrono>

using namespace std;

void bem_vindo()
{
    cout << "*************************************" << endl;
    cout << "* Bem vindos ao jogo da adivinhação*" << endl;
    cout << "*************************************" << endl;
}

int chute_numero()
{
    int chute;
    cout << "Chute o número secreto: ";
    cin >> chute;
    return chute;
}

int gerar_numero_aleatorio()
{
    static mt19937 gen(
        static_cast<unsigned>(chrono::steady_clock::now().time_since_epoch().count()));
    uniform_int_distribution<> dist(1, 100);
    return dist(gen);
}

void comparacao_numero_secreto(int numero_secreto, int chute)
{
    bool maior = numero_secreto > chute;
    if (maior)
    {
        cout << "Você errou, o numero secreto é maior que seu chute atual" << endl;
    }
    else
    {
        cout << "Você errou, o numero secreto é menor que seu chute atual" << endl;
    }
}

void adivinhacao(int numero_secreto)
{
    int chute;
    int tentativas = 1;
    bool acabou = false;
    bool acertou = false;
    do
    {
        cout << "Tentantiva " << tentativas << endl;
        chute = chute_numero();
        acertou = numero_secreto == chute;

        if (acertou)
        {
            cout << "Você acertou, o número secreto é " << numero_secreto;
            acabou = true;
        }
        else
        {
            comparacao_numero_secreto(numero_secreto, chute);
            tentativas++;
        }
    } while (!acabou);
}

int main()
{
    SetConsoleOutputCP(CP_UTF8);

    bem_vindo();

    const int numero_secreto = gerar_numero_aleatorio();

    adivinhacao(numero_secreto);
}