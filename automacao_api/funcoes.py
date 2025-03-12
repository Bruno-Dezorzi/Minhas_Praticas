import requests
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
from datetime import datetime

def get_data(
    tabela: str,
    engine: create_engine,
    db_api: pd.DataFrame = None,
    headers: dict = None,
    payload: dict = None
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Obtém os dados da tabela do banco de dados e da API, caso necessário.

    Esta função busca os dados de uma tabela no banco de dados e, opcionalmente, os dados de uma API.
    Se um DataFrame db_api for fornecido, ele será usado como fonte de dados da API.
    Caso contrário, a função chamará fetch_api_data_for_update para buscar os dados da API.

    Parâmetros:
    -----------
    tabela : str
        Nome da tabela no banco de dados.

    engine : create_engine
        Objeto de conexão com o banco de dados.

    db_api : pd.DataFrame, opcional
        DataFrame contendo os dados da API (caso já tenham sido obtidos previamente).
        Se fornecido, os dados da API não serão buscados novamente.

    headers : dict, opcional
        Cabeçalhos para a requisição da API. Necessário caso os dados da API precisem ser buscados.

    payload : dict, opcional
        Corpo da requisição da API. Necessário caso os dados da API precisem ser buscados.

    Retorno:
    --------
    tuple[pd.DataFrame, pd.DataFrame]
        - df_db: DataFrame contendo os dados da tabela do banco de dados.
        - df_api: DataFrame contendo os dados da API (se fornecido ou buscado via requisição).

    Observações:
    ------------
    - A função assume que fetch_db_data_for_update e fetch_api_data_for_update estão implementadas e 
      são responsáveis por buscar os dados do banco e da API, respectivamente.
    - Se db_api for None, os dados da API serão buscados via requisição HTTP.
    - O parâmetro show_tokens_url é definido como False por padrão na chamada da API.
    """
    if db_api is not None:
        df_db = fetch_db_data_for_update(tabela, engine)
        df_api = db_api  # Dados diretamente do db_api
    else:
        df_db = fetch_db_data_for_update(tabela, engine)
        df_api = fetch_api_data_for_update(tabela, headers, payload,show_tokens_url= False)
    return df_db, df_api

def fetch_db_data_for_update(
    tabela: list, engine: create_engine
) -> pd.DataFrame:  # Para o UPDATE
    """
    Obtém os dados de uma ou mais tabelas do banco de dados.

    Esta função executa uma consulta SQL para buscar os dados de uma ou mais tabelas especificadas
    no banco de dados e retorna um DataFrame contendo os resultados da consulta.

    Parâmetros:
    -----------
    tabela : list
        Uma lista contendo os nomes das tabelas a serem consultadas. Cada nome de tabela será usado
        para formar a consulta SQL de acordo com a estrutura do banco de dados.

    engine : create_engine
        A instância de conexão com o banco de dados, utilizada para executar a consulta SQL e obter os dados.

    Retorna:
    --------
    pd.DataFrame
        Um DataFrame contendo as colunas "Id" e "UpdatedAt" para os registros encontrados nas tabelas
        consultadas. Caso não haja registros, o DataFrame será vazio.

    Exceções:
    ----------
    Se houver algum erro na execução da consulta ou na conexão com o banco de dados, a função pode
    levantar exceções relacionadas à conexão ou à execução da SQL.
    """
    query = f'SELECT "Id", "UpdatedAt" FROM mercado."{tabela}"'
    with engine.connect() as conn:
        result = conn.execute(text(query))

    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def fetch_api_data_for_update(
    tabela: list, headers: dict, payload: dict, show_tokens_url: bool = False
) -> pd.DataFrame:  # Para o UPDATE
    """
    Obtém os dados de uma tabela da API.

    Esta função faz uma requisição à API para obter os dados de uma tabela específica,
    realizando requisições paginadas caso a resposta contenha múltiplas páginas de dados.
    Os dados são então combinados em um único DataFrame.

    Parâmetros:
    -----------
    tabela : list
        Uma lista contendo os nomes das tabelas a serem consultadas. O nome da tabela
        é usado para formar a URL da requisição à API.

    headers : dict
        O cabeçalho da requisição HTTP, incluindo informações como autenticação ou tipos de conteúdo.

    payload : dict
        Os dados da requisição HTTP, enviados no corpo da requisição, conforme necessário pela API.

    show_tokens_url: bool
        Caso queria ver os tokens printados, deixe igual a True

    Retorna:
    --------
    pd.DataFrame
        Um DataFrame contendo os dados retornados pela API para a tabela solicitada.
        Se houver múltiplas páginas de resultados, os dados de todas as páginas serão concatenados.

    Exceções:
    ----------
    Caso a requisição falhe ou os dados retornados sejam inválidos, a função pode gerar erros de rede
    ou formatação de dados, como exceções relacionadas à API ou à conversão para DataFrame.
    """

    url = f"https://api.mercadoe.com/boost/v1/{tabela}"

    df_geral = pd.DataFrame()
    print(f"Começando a tabela {tabela}")
    while url != None:

        # Fazer a requisição para a API
        response = requests.request("GET", url, headers=headers, data=payload)
        conteudo = response.json()
        dados = conteudo.get("value")

        # Converter para DataFrame
        df = pd.DataFrame(dados)

        # Concatenar os dados recebidos
        df_geral = pd.concat([df_geral, df], ignore_index=True)

        # Verificar se há uma próxima página de dados
        url = conteudo.get("@odata.nextLink")
        if show_tokens_url == True:
            print(f"Nova URL: {url}")
    return df_geral


def update_db_with_api_data(
    tabela: str,
    engine: create_engine,
    db_api: pd.DataFrame = None,
    headers: dict = None,
    payload: dict = None,
) -> None:
    """
    Atualiza registros em uma tabela no banco de dados com base nos dados de uma API.

    Parâmetros:
    ----------- 
    tabela : str
        O nome da tabela no banco de dados que será atualizada.

    engine : create_engine
        A instância de conexão com o banco de dados. Usada para executar os comandos SQL.

    db_api : pd.DataFrame, opcional
        Um DataFrame contendo os dados do banco de dados para comparação com os dados da API.
        Se não fornecido, os dados da API serão obtidos diretamente usando a função get_data_api.

    headers : dict, opcional
        Cabeçalhos para a requisição HTTP à API, necessário apenas se db_api não for fornecido.

    payload : dict, opcional
        O corpo da requisição HTTP à API, necessário apenas se db_api não for fornecido.

    Retorna:
    --------
    None
        Esta função não retorna nada. Ela atualiza registros diretamente no banco de dados.
    """

    df_db, df_api = get_data(tabela=tabela, engine= engine, db_api= db_api, headers= headers,payload= payload)

    if df_db.empty:
        print(f"Nenhum dado encontrado para {tabela} no DB")
    elif df_api.empty:
        print(f"Nenhum dado encontrado para {tabela} na API")
    elif df_db.empty and df_api.empty :
        print(f"Nenhum dado encontrado para {tabela} nas duas fontes")
    else:
        print(f"Dados encontrados para {tabela} nas duas fontes")

    if "Id" not in df_db.columns or "UpdatedAt" not in df_db.columns:
        print(f"Faltando colunas necessárias na tabela {tabela}")
        return

    # Garantir que as colunas 'UpdatedAt' sejam convertidas corretamente para datetime
    df_api['UpdatedAt'] = pd.to_datetime(pd.to_datetime(df_api['UpdatedAt'].str.replace('T',' ').str.slice(0,19)))
    df_db['UpdatedAt'] = pd.to_datetime(pd.to_datetime(df_db['UpdatedAt'].str.replace('T',' ').str.slice(0,19)))


    if df_api["UpdatedAt"].isnull().any() or df_db["UpdatedAt"].isnull().any():
        print("Há valores inválidos nas colunas 'UpdatedAt'. Verifique os dados.")
        return

    # Filtrar registros da API que são mais novos
    df_api = df_api[df_api["Id"].isin(df_db["Id"])]
    df_api = df_api.merge(df_db[["Id", "UpdatedAt"]], on="Id")
    df_api = df_api[df_api["UpdatedAt_x"] > df_api["UpdatedAt_y"]]
    
    if df_api.empty:
        print(f"Não há registros para atualizar na tabela {tabela}")
        return


    # Converter as datas para o formato de string SQL adequado
    df_api["UpdatedAt_x"] = df_api["UpdatedAt_x"].dt.strftime('%Y-%m-%d %H:%M:%S')
    df_api = df_api.rename(columns={"UpdatedAt_x": "UpdatedAt"})  # Renomeia a coluna
    df_api['UpdatedAt'] = df_api['UpdatedAt'].astype(str)
    df_api = df_api.drop(columns='UpdatedAt_y')

    # Substituindo 'None' (string) por NaN
    df_api = df_api.replace('None', 'null')

    # Garantir que os valores None reais sejam convertidos para NaN também
    df_api = df_api.where(pd.notnull(df_api), 'null')

    # Identificar colunas para atualizar
    colunas_para_atualizar = [col for col in df_api.columns if col not in ["Id", "UpdatedAt_y"]]

    # Criar query dinâmica para o UPDATE
    update_sql = f"""
        UPDATE mercado."{tabela}" AS db
        SET {", ".join([f'"{col}" = api."{col}"' for col in colunas_para_atualizar])}
        FROM (VALUES {", ".join([str(tuple(row)) for row in df_api.itertuples(index=False)])})
        AS api ("Id", {", ".join([f'"{col}"' for col in colunas_para_atualizar])})
        WHERE db."Id" = api."Id" AND db."UpdatedAt"::timestamp < api."UpdatedAt"::timestamp;
    """ 

    try:
        with engine.connect() as conn:
            conn.execute(text(update_sql))
            conn.commit()
    except Exception as e:
        print(f"Erro ao atualizar a tabela {tabela}: {e}")

    print(f"{len(df_api)} registros atualizados na tabela {tabela}")



def sync_data_with_api_by_timekey(
    tabela: str,
    engine: create_engine, 
    headers: dict, 
    payload: dict,
    show_tokens_url: bool = False
) -> None:
    """
    Obtém dados de uma tabela da API com base no valor de TimeKey e realiza o update no banco de dados.

    Esta função faz uma requisição à API para obter dados de uma tabela específica, com base no valor de 
    TimeKey, e insere apenas os registros que possuem um TimeKey maior que o valor máximo presente no banco. 
    Após a inserção dos dados novos, a função chama get_data_update para realizar as atualizações no banco 
    de dados.

    Parâmetros:
    -----------
    tabela : str
        O nome da tabela a ser consultada na API e no banco de dados.

    engine : create_engine
        Conexão com o banco de dados que será usada para consultar e inserir dados.

    headers : dict
        O cabeçalho da requisição HTTP para a API, incluindo informações como autenticação e tipo de conteúdo.

    payload : dict
        Os dados a serem enviados no corpo da requisição HTTP, conforme necessário pela API.

    Retorna:
    --------
    None
        A função não retorna valores. Ela realiza a inserção dos dados no banco e chama outra função para 
        atualizar os dados.

    Processamento:
    --------------
    A função verifica o maior TimeKey presente na tabela do banco de dados e faz requisições à API 
    para obter os dados. Somente os registros com TimeKey maior que o valor máximo encontrado são 
    inseridos no banco. Após a inserção, a função chama get_data_update para realizar atualizações 
    nos registros da tabela.

    Exceções:
    ----------
    A função assume que a API retorna dados no formato esperado. Caso contrário, pode ocorrer falha na 
    conversão dos dados para DataFrame ou na inserção no banco.
    """
    url = f"https://api.mercadoe.com/boost/v1/{tabela}"
    df_geral = pd.DataFrame()
    print(f"Começando a tabela {tabela} às {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with engine.connect() as conn:
        result = conn.execute(text(f'SELECT max("TimeKey") FROM mercado."{tabela}"'))
        max_time_key = np.int64(result.scalar())  # Obtém o maior TimeKey
        print(f"Maior TimeKey atual: {max_time_key}")

    while url != None:

        # Fazer a requisição para a API
        response = requests.request("GET", url, headers=headers, data=payload)
        conteudo = response.json()
        dados = conteudo.get("value")

        # Converter para DataFrame
        df = pd.DataFrame(dados)

        # Concatenar os dados recebidos
        df_geral = pd.concat([df_geral, df], ignore_index=True)
        df_geral_timekey = df_geral[df_geral["TimeKey"] > max_time_key]

        # Verificar se há uma próxima página de dados
        url = conteudo.get("@odata.nextLink")
        if show_tokens_url == True:
            print(f"Nova URL: {url}")

    # Inserir no banco de dados, garantindo que os dados sejam adicionados apenas se o TimeKey for maior
    if not df_geral_timekey.empty:
        df_geral_timekey.to_sql(
            tabela, engine, if_exists="append", index=False, schema="mercado"
        )
        print(f"Inseridos {len(df_geral_timekey)} registros na tabela {tabela}")
    else:
        print(f"Nenhum novo registro para inserir na tabela {tabela}")
    print(f"Tabela {tabela} finalizada")

    #analyze_cardina(engine= engine)

    #remove_duplicate_records(tabela, engine)

    #update_db_with_api_data(tabela, engine, df_geral)


def remove_duplicate_records(
    tabela: str, 
    engine: create_engine
) -> None :
    """
    Remove registros duplicados de uma tabela no banco de dados.

    Esta função identifica e remove registros duplicados de uma tabela, mantendo apenas o registro 
    com o valor mais recente da coluna "UpdatedAt" para cada "Id". Caso existam múltiplos registros 
    com o mesmo "Id", ela exclui os registros com a data de atualização mais antiga.

    Parâmetros:
    -----------
    tabela : str
        O nome da tabela do banco de dados de onde os registros duplicados serão removidos.

    engine : create_engine
        Conexão com o banco de dados que será usada para executar a consulta de exclusão.

    Retorna:
    --------
    None
        A função não retorna valores. Ela realiza a exclusão dos registros duplicados da tabela.

    Processamento:
    --------------
    A função executa uma subconsulta para identificar os registros duplicados com base na coluna "Id". 
    Para cada grupo de registros com o mesmo "Id", ela mantém o registro com o maior valor em "UpdatedAt" 
    e exclui os outros, garantindo que a tabela contenha apenas um registro por "Id" com o valor mais recente de "UpdatedAt".

    Exceções:
    ----------
    A função assume que a tabela possui as colunas "Id" e "UpdatedAt". Se qualquer uma dessas colunas 
    estiver faltando ou os dados estiverem corrompidos, a função pode falhar ou produzir resultados incorretos.
    """
    with engine.connect() as conn:
        query = text(
            f"""
                DELETE FROM mercado."{tabela}" as principal
                WHERE "Id" IN (
                    SELECT "Id"
                    FROM mercado."{tabela}"
                    GROUP BY "Id"
                    HAVING COUNT(*) > 1
                )
                AND "UpdatedAt" < (
                    SELECT MAX("UpdatedAt")
                    FROM mercado."{tabela}" AS sub
                    WHERE sub."Id" = principal."Id"
                );
            """
        )
        result = conn.execute(query)
        conn.commit()
        print(f"Registros duplicados removidos da tabela {tabela}")
        registros_afetados = result.rowcount
        print(f"{registros_afetados} registros duplicados foram removidos da tabela {tabela}.")


def analyze_cardina(
    engine: create_engine
) -> None:
    """
    Atualiza as estatísticas de cardinalidade das tabelas no banco de dados.

    Esta função executa o comando ANALYZE no banco de dados, que atualiza as estatísticas das tabelas
    e índices, permitindo ao otimizador de consultas tomar melhores decisões sobre planos de execução.

    Parâmetros:
    -----------
    engine : create_engine
        Objeto de conexão com o banco de dados.

    Retorno:
    --------
    None
        A função não retorna valores. Ela apenas executa o comando ANALYZE no banco de dados.

    Observações:
    ------------
    - O comando ANALYZE coleta estatísticas sobre a distribuição dos dados nas tabelas, 
      melhorando a eficiência das consultas SQL.
    - Esta função deve ser executada regularmente em bancos de dados com muitas atualizações, 
      inserções e deleções para garantir um bom desempenho nas consultas.
    - A função assume que a conexão com o banco de dados já está configurada corretamente.
    """
    with engine.connect() as conn:
        query = text(
            f"""
                ANALYZE;
            """
        )
        conn.execute(query)
        conn.commit()
        print(f"Cardinalidades Atualizadas")