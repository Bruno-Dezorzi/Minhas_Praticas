#! python3.11.7

arquivo = open('pessoas.csv') 
dados = arquivo.read()

arquivo.close()

for registro in dados.splitlines():
    #print(*registro.split(","))
    print('Nome: {} , Idade: {}'.format(*registro.split(',')))
    
