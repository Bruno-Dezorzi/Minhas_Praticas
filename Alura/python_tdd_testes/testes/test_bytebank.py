from codigo.bytebank import Funcionario
from pytest import raises, mark


class TestClass:
    def test_quando_idade_recebe_13_03_2000_deve_retornar_22(self):
        entrada = '13/03/2000'  # Given - Contexto
        esperado = 25

        funcionario = Funcionario('Teste', entrada, 1111)

        # When-ação
        resultado = funcionario.idade()

        assert resultado == esperado

    def test_quando_sobrenome_recebe_Lucas_Carvalho_deve_retornar_Carvalho(self):
        entrada = 'Lucas Carvalho'
        esperado = 'Carvalho'

        funcionario = Funcionario(entrada, '13/03/2000', 1111)

        # When-ação
        resultado = funcionario.sobrenome()

        assert resultado == esperado
    
    #@mark.skip(reason="não quero executar isso agora")
    #@mark.skipif(sys.version_info < (3, 10), reason="Requer Python na versão 3.10 ou superior")
    #@mark.skip
    def test_quando_decrescimo_salario_recebe_100000_deve_retornar_90000(self):
        entrada_salario = 100000 #given
        entrada_nome = 'Paulo Bragança'
        esperado = 90000
        
        funcionario_teste = Funcionario(entrada_nome, '13/03/2000', entrada_salario)
        funcionario_teste.decrescimo_salario() #When
        resultado = funcionario_teste.salario
        
        assert resultado == esperado #then
        
    @mark.calcular_bonus
    def test_quando_calcular_bonus_recebe_1000_deve_retornar_100(self):
        entrada = 1000
        esperado = 100
        
        funcionario_teste = Funcionario('teste','12/03/1997',entrada)
        valor = funcionario_teste.calcular_bonus()
        
        assert valor == esperado
        
    @mark.calcular_bonus
    def test_quando_calcular_bonus_recebe_10000000000_deve_retornar_exception(self):
        with raises(Exception):
            entrada = 10000000000
            
            funcionario_teste = Funcionario('teste','12/03/1997',entrada)
            funcionario_teste.calcular_bonus()
            

    
        