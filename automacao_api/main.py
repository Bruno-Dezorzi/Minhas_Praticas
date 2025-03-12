import time
import requests
from sqlalchemy import create_engine
import pandas as pd
import funcoes as f


def main():

    PAYLOAD = {}
    HEADERS = {
        "Authorization": "Basic XX="  # Substitua pela sua chave de autorização
    }

    # URL do banco de dados
    ENGINE = create_engine(
        "XX",
        echo= False
    )  # Substitua pela URL do seu banco de dados

    URL = "XX" # Substitua pela URL da API

    response = requests.request("GET", URL, headers=HEADERS, data=PAYLOAD)
    conteudo = response.json()
    dados = conteudo.get("value")

    df = pd.DataFrame(dados)
    tabelas = list(df["url"])

    tabelas_teste = 'Contracts'

    tempo_inicial = time.time()


    try:
        for tabela in tabelas:
            f.sync_data_with_api_by_timekey(tabela=tabela, engine=ENGINE, headers=HEADERS, payload=PAYLOAD,show_tokens_url= False)

        f.analyze_cardina(engine= ENGINE)
        
        for tabela in tabelas:
            f.remove_duplicate_records(tabela= tabela,engine= ENGINE)
            f.update_db_with_api_data(tabela= tabela,engine= ENGINE,headers=HEADERS, payload=PAYLOAD)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    

    

    tempo_final = time.time()

    tempo_total = tempo_final - tempo_inicial

    # Calculando horas, minutos e segundos
    horas = tempo_total // 3600
    minutos = (tempo_total % 3600) // 60
    segundos = tempo_total % 60

    # Exibindo o resultado
    print(
        f"Tempo total de execução: {int(horas)} horas, {int(minutos)} minutos, {int(segundos)} segundos"
    )


if __name__ == "__main__":
    main()