import os
from os.path import join
import pandas as pd
from datetime import datetime, timedelta 


# intervalo de datas
data_inicio = datetime.today()
data_fim = data_inicio + timedelta(days=7)

# formatando as datas
data_inicio = data_inicio.strftime('%Y-%m-%d')
data_fim = data_fim.strftime('%Y-%m-%d')

city = 'Boston'
key = 'MJCZV6K78GMMH7DH7D6VZLJ4U'

URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
            f'{city}/{data_inicio}/{data_fim}?unitGroup=metric&include=days&key={key}&contentType=csv')

dados = pd.read_csv(URL)
print(dados.head())

base_path = r'C:\Devs\Repositorios\Minhas_Praticas\Alura\Airflow\apache-airflow-primeiro-pipeline'
file_path = os.path.join(base_path, f'semana={data_inicio}')


os.makedirs(file_path, exist_ok=True)

dados.to_csv(file_path + 'dados_brutos.csv')
dados[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temperaturas.csv')
dados[['datetime', 'description', 'icon']].to_csv(file_path + 'condicoes.csv')