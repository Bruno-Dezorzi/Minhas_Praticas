FROM python:3

# Atualiza os pacotes e instala o pip (já vem com a imagem do Python, mas incluímos para garantir atualizações)
RUN apt-get update -y && apt-get install -y python3-pip

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Instala as dependências do projeto
RUN pip install --no-cache-dir Flask

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Comando de inicialização da aplicação
CMD [ "python", "./app.py" ]
