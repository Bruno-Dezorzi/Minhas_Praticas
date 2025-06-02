#! python3.11.7
arquivo = open('pessoas.csv')

for registro in arquivo:
    print("Nome: {}, Idade: {}".format(*registro.split(',')))
    
arquivo.close()