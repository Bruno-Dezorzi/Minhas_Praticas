FROM python:3.11

# Atualiza o gerenciador de pacotes e instala dependências do sistema (opcional)
RUN apt-get update -y && apt-get install -y gcc

# Define o diretório de trabalho
WORKDIR /app

# Instala as bibliotecas Python necessárias
RUN pip install Flask requests flask_mysqldb

# Copia os arquivos do projeto para dentro do container
COPY . .

# Expõe a porta usada pela aplicação Flask
EXPOSE 5000

# Comando para iniciar a aplicação
CMD [ "python", "./app.py" ]
