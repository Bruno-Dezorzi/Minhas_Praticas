// Screen Sound



void BoasVindas(){
    string mensagemDeBoasVindas = "Boas vindas ao Screen Sound!";
    Console.WriteLine("************************************");
    Console.WriteLine(mensagemDeBoasVindas);
    Console.WriteLine("************************************");
}

BoasVindas();


class Carro{
    private string marca;
    private string modelo;
    private string cor;

    public Carro(string marca, string modelo, string cor){
        this.marca = marca;
        this.modelo = modelo;
        this.cor = cor;
    }
}