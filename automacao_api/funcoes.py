import logging
import requests
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
from ratelimit import limits, sleep_and_retry
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("data_update.log"), logging.StreamHandler()]
)

@retry(
    stop=stop_after_attempt(5),  # Tenta no máximo 5 vezes
    wait=wait_exponential(multiplier=1, min=2, max=10),  # Tempo de espera exponencial (2s, 4s, 8s...)
    retry=retry_if_exception_type((requests.exceptions.RequestException, ValueError))  # Repetir se houver erro de rede ou JSON inválido
)
@sleep_and_retry
@limits(calls=240, period=60)  # 240 chamadas por 60 segundos
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
    logging.info(f"Buscando dados para a tabela: {tabela} - get_data()")
    
    if db_api is not None:
        logging.info("Dados da API fornecidos como DataFrame - get_data()")
        df_db = fetch_db_data_for_update(tabela, engine)
        df_api = db_api  
    else:
        df_db = fetch_db_data_for_update(tabela, engine)
        df_api = fetch_api_data_for_update(tabela, headers, payload, show_tokens_url=False)
    
    logging.info(f"Dados recuperados para {tabela} - DB: {len(df_db)} registros, API: {len(df_api)} registros - get_data()")
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
    logging.info(f"Consultando dados do banco de dados para {tabela} - fetch_db_data_for_update()")
    query = f'SELECT "Id", "UpdatedAt" FROM mercado."{tabela}"'
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        logging.info(f"Consulta realizada com sucesso. {len(df)} registros obtidos - fetch_db_data_for_update()")
        return df
    except Exception as e:
        logging.error(f"Erro ao consultar {tabela}: {e} - fetch_db_data_for_update()")
        return pd.DataFrame()

@retry(
    stop=stop_after_attempt(5),  # Tenta no máximo 5 vezes
    wait=wait_exponential(multiplier=1, min=2, max=10),  # Tempo de espera exponencial (2s, 4s, 8s...)
    retry=retry_if_exception_type((requests.exceptions.RequestException, ValueError))  # Repetir se houver erro de rede ou JSON inválido
)
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

    logging.info(f"Buscando dados da API para a tabela {tabela} - fetch_api_data_for_update()")
    url = f"https://api.mercadoe.com/boost/v1/{tabela}"
    df_geral = pd.DataFrame()
    
    while url:
        try:
            response = requests.get(url, headers=headers, data=payload)
            response.raise_for_status()
            conteudo = response.json()
            dados = conteudo.get("value", [])
            
            df = pd.DataFrame(dados)
            df = df.dropna(axis=1, how='all') # Remove colunas com todos os valores nulos
            #df.fillna('') 
            df_geral = pd.concat([df_geral, df], ignore_index=True)
            
            url = conteudo.get("@odata.nextLink")
            if show_tokens_url:
                logging.info(f"Próxima URL: {url} - fetch_api_data_for_update()" )
        except Exception as e:
            logging.error(f"Erro ao buscar dados da API para {tabela}: {e} - fetch_api_data_for_update()")
            break
    
    logging.info(f"Dados da API obtidos para {tabela}: {len(df_geral)} registros - fetch_api_data_for_update()")
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

    logging.info(f'Iniciando processo de atualizacao para a tabela {tabela} - update_db_with_api_data()')
    
    df_db, df_api = get_data(tabela=tabela, engine=engine, db_api=db_api, headers=headers, payload=payload)

    if df_db.empty:
        logging.warning(f'Nenhum dado encontrado para {tabela} no DB - update_db_with_api_data()')
    if df_api.empty:
        logging.warning(f'Nenhum dado encontrado para {tabela} na API - update_db_with_api_data()')
    if df_db.empty and df_api.empty:
        logging.warning(f'Nenhum dado encontrado para {tabela} nas duas fontes - update_db_with_api_data()')
        return
    
    logging.info(f'Dados carregados para {tabela} - update_db_with_api_data()')

    if "Id" not in df_db.columns or "UpdatedAt" not in df_db.columns:
        logging.error(f'Faltando colunas necessárias na tabela {tabela} - update_db_with_api_data()')
        return
    
    logging.info('Convertendo colunas UpdatedAt para datetime - update_db_with_api_data()')
    df_api['UpdatedAt'] = pd.to_datetime(df_api['UpdatedAt'].str.replace('T',' ').str.slice(0,19))
    df_db['UpdatedAt'] = pd.to_datetime(df_db['UpdatedAt'].str.replace('T',' ').str.slice(0,19))

    if df_api["UpdatedAt"].isnull().any() or df_db["UpdatedAt"].isnull().any():
        logging.error("Há valores inválidos nas colunas 'UpdatedAt'. Verifique os dados - update_db_with_api_data()")
        return

    logging.info('Filtrando registros mais recentes da API para atualização - update_db_with_api_data()')
    df_api = df_api[df_api["Id"].isin(df_db["Id"])]
    df_api = df_api.merge(df_db[["Id", "UpdatedAt"]], on="Id")
    df_api = df_api[df_api["UpdatedAt_x"] > df_api["UpdatedAt_y"]]
    
    if df_api.empty:
        logging.info(f'Nao há registros para atualizar na tabela {tabela} - update_db_with_api_data()')
        return

    logging.info('Preparando dados para atualizacao - update_db_with_api_data()')
    df_api["UpdatedAt_x"] = df_api["UpdatedAt_x"].dt.strftime('%Y-%m-%d %H:%M:%S')
    df_api = df_api.rename(columns={"UpdatedAt_x": "UpdatedAt"})
    df_api["UpdatedAt"] = df_api["UpdatedAt"].astype(str)
    df_api = df_api.drop(columns='UpdatedAt_y')

    #df_api[col] = df_api[col].replace('None', 'null')
    #df_api[col]  = df_api[col].where(pd.notnull(df_api), 'null')

    for col in df_api.select_dtypes(include=['object', 'datetime']).columns:
        df_api[col] = df_api[col].replace({None: 'null', 'None': 'null'})  # Garante que None e 'None' virem 'null'
        df_api[col] = df_api[col].fillna('null')  # Substitui NaN (se houver) por 'null'

# Tratamento para colunas numéricas (int e float)
    for col in df_api.select_dtypes(include=['int', 'float']).columns:
        df_api[col] = df_api[col].replace({'None': 0, None: 0, np.nan: 0})  # Transforma qualquer None, 'None' ou NaN em 0
        df_api[col] = df_api[col].astype(float)  # Garante que os valores sejam numéricos e compatíveis com o banco

    # Caso especial da tabela OrderAttributes
    if 'Value' in df_api.columns:
        df_api['Value'] = df_api['Value'].str.replace(r"[\r\n]+", " ", regex=True)
        df_api['Value'] = df_api['Value'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii') if isinstance(x, str) else x)

    colunas_para_atualizar = [col for col in df_api.columns if col not in ["Id", "UpdatedAt_y"]]

    update_sql = f'''
        UPDATE mercado."{tabela}" AS db
        SET {", ".join([f'"{col}" = api."{col}"' for col in colunas_para_atualizar])}
        FROM (VALUES {", ".join([str(tuple(row)) for row in df_api.itertuples(index=False)])})
        AS api ("Id", {", ".join([f'"{col}"' for col in colunas_para_atualizar])})
        WHERE db."Id" = api."Id" AND db."UpdatedAt"::timestamp < api."UpdatedAt"::timestamp;
    '''

    try:
        with engine.connect() as conn:
            conn.execute(text(update_sql))
            conn.commit()
            logging.info(f'{len(df_api)} registros atualizados na tabela {tabela} - update_db_with_api_data()')
    except Exception as e:
        logging.error(f'Erro ao atualizar a tabela {tabela}: {e} - update_db_with_api_data()')
        
        # Exibir os IDs que geraram o erro
        ids_erro = df_api["Id"].tolist()  # Obtendo os IDs da API que estavam sendo atualizados
        logging.error(f"Erro ao atualizar os seguintes IDs na tabela {tabela}: {ids_erro} - update_db_with_api_data()")



@retry(
    stop=stop_after_attempt(5),  # Tenta no máximo 5 vezes
    wait=wait_exponential(multiplier=1, min=2, max=10),  # Tempo de espera exponencial (2s, 4s, 8s...)
    retry=retry_if_exception_type((requests.exceptions.RequestException, ValueError))  # Repetir se houver erro de rede ou JSON inválido
)
@sleep_and_retry
@limits(calls=240, period=60)  # 240 chamadas por 60 segundos
def sync_data_with_api_by_timekey(
    tabela: str,
    engine: create_engine, 
    headers: dict, 
    payload: dict,
    show_tokens_url: bool = False
) -> None:
    """
    Obtém dados de uma tabela da API com base no valor de TimeKey e realiza o update no banco de dados.

    Parâmetros:
    -----------
    tabela : str
        O nome da tabela a ser consultada na API e no banco de dados.

    engine : create_engine
        Conexão com o banco de dados que será usada para consultar e inserir dados.

    headers : dict
        O cabeçalho da requisição HTTP para a API.

    payload : dict
        Os dados a serem enviados no corpo da requisição HTTP.

    show_tokens_url : bool, opcional
        Se True, exibe a URL da próxima requisição da API.

    Retorna:
    --------
    None
    """
    url = f"https://api.mercadoe.com/boost/v1/{tabela}"
    
    df_geral = pd.DataFrame()

    logging.info(f"Iniciando sincronização da tabela: {tabela} - sync_data_with_api_by_timekey()")
    
    with engine.connect() as conn:
        # Buscar todos os TimeKeys existentes no banco
        check_results= conn.execute(text(f'SELECT count(*) FROM mercado."{tabela}" LIMIT 1')) 
        if check_results.scalar() > 0:
            result = conn.execute(text(f'SELECT "TimeKey" FROM mercado."{tabela}"'))
            existing_timekeys = {row[0] for row in result.fetchall()}  # Conjunto de TimeKeys existentes
        #logging.info(f"TimeKeys existentes no banco de dados: {existing_timekeys}")
        else:
            logging.warning("Sem registros na tabela")
            existing_timekeys = set()  # Permitir inserção de todos os dados da API
        
    while url is not None:
        try:
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            conteudo = response.json()
            dados = conteudo.get("value", [])

            df = pd.DataFrame(dados)
            df = df.dropna(axis=1, how='all') # Remove colunas com todos os valores nulos
            #df.fillna('')
            df_geral = pd.concat([df_geral, df], ignore_index=True)
            #logging.info(f"df_geral tem {len(df_geral)} registros - sync_data_with_api_by_timekey()")
            
            if df_geral.empty:
                logging.info(f"Nenhum dado novo encontrado para {tabela} - sync_data_with_api_by_timekey()")
                break

            df_geral["TimeKey"] = df_geral["TimeKey"].astype(np.int64)  # Garantir que seja int64

            # Filtrar registros cujos TimeKey não existem no banco de dados
            df_geral_timekey = df_geral[~df_geral["TimeKey"].isin(existing_timekeys)]
            
            if not df_geral_timekey.empty:
                try:
                    # Inserir os novos registros no banco de dados
                    df_geral_timekey.to_sql(tabela, engine, if_exists="append", index=False, schema="mercado")
                    logging.info(f"Inseridos {len(df_geral_timekey)} registros na tabela {tabela} - sync_data_with_api_by_timekey()")
                    # Atualizar o conjunto de TimeKeys após inserção
                    existing_timekeys.update(df_geral_timekey["TimeKey"].values)
                except Exception as e:
                    logging.error(f"Erro ao inserir dados na tabela {tabela}: {e} - sync_data_with_api_by_timekey()")
        
            url = conteudo.get("@odata.nextLink")
            if show_tokens_url:
                logging.info(f"Nova URL para requisição: {url} - sync_data_with_api_by_timekey()")

        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao requisitar dados da API: {e} - sync_data_with_api_by_timekey()")
            return
        
    if df_geral_timekey.empty:
        logging.info(f"Nenhum registro novo para inserir {tabela} - sync_data_with_api_by_timekey()")

    logging.info(f"Sincronização finalizada para {tabela} - sync_data_with_api_by_timekey()")


def update_db_with_api_data_chunked(
    tabela: str,
    engine: create_engine,
    db_api: pd.DataFrame = None,
    headers: dict = None,
    payload: dict = None,
    chunk_size: int = 500  # Número de registros por lote
) -> None:
    logging.info(f'Iniciando atualização fragmentada para {tabela} - update_db_with_api_data_chunked()')

    df_db, df_api = get_data(tabela=tabela, engine=engine, db_api=db_api, headers=headers, payload=payload)

    if df_db.empty or df_api.empty:
        logging.warning(f'Nenhum dado encontrado para {tabela} - update_db_with_api_data_chunked()')
        return
    
    df_api['UpdatedAt'] = pd.to_datetime(df_api['UpdatedAt'].str.replace('T',' ').str.slice(0,19))
    df_db['UpdatedAt'] = pd.to_datetime(df_db['UpdatedAt'].str.replace('T',' ').str.slice(0,19))

    df_api = df_api[df_api["Id"].isin(df_db["Id"])]
    df_api = df_api.merge(df_db[["Id", "UpdatedAt"]], on="Id")
    df_api = df_api[df_api["UpdatedAt_x"] > df_api["UpdatedAt_y"]]

    if df_api.empty:
        logging.info(f'Não há registros para atualizar em {tabela} - update_db_with_api_data_chunked()')
        return

    df_api["UpdatedAt_x"] = df_api["UpdatedAt_x"].dt.strftime('%Y-%m-%d %H:%M:%S')
    df_api = df_api.rename(columns={"UpdatedAt_x": "UpdatedAt"})
    df_api = df_api.drop(columns='UpdatedAt_y')

    for col in df_api.select_dtypes(include=['object', 'datetime']).columns:
        df_api[col] = df_api[col].fillna('null')

    for col in df_api.select_dtypes(include=['int', 'float']).columns:
        df_api[col] = df_api[col].replace({np.nan: 0}).astype(float)

    colunas_para_atualizar = [col for col in df_api.columns if col not in ["Id", "UpdatedAt_y"]]

    total_registros = len(df_api)
    logging.info(f"Total de registros para atualizar: {total_registros} - update_db_with_api_data_chunked()")

    for i in range(0, total_registros, chunk_size):
        df_chunk = df_api.iloc[i:i + chunk_size]
        update_sql = f'''
            UPDATE mercado."{tabela}" AS db
            SET {", ".join([f'"{col}" = api."{col}"' for col in colunas_para_atualizar])}
            FROM (VALUES {", ".join([str(tuple(row)) for row in df_chunk.itertuples(index=False)])})
            AS api ("Id", {", ".join([f'"{col}"' for col in colunas_para_atualizar])})
            WHERE db."Id" = api."Id" AND db."UpdatedAt"::timestamp < api."UpdatedAt"::timestamp;
        '''
        try:
            with engine.connect() as conn:
                conn.execute(text(update_sql))
                conn.commit()
                logging.info(f'Lote {i//chunk_size + 1} atualizado ({len(df_chunk)} registros) - update_db_with_api_data_chunked()')
        except Exception as e:
            logging.error(f'Erro ao atualizar lote {i//chunk_size + 1}: {e} - update_db_with_api_data_chunked()')

    logging.info(f"Atualização completa para {tabela} - update_db_with_api_data_chunked()")


def sync_data_with_api_by_timekey_chunked(
    tabela: str,
    engine: create_engine, 
    headers: dict, 
    payload: dict,
    show_tokens_url: bool = False,
    chunk_size: int = 500  # Número máximo de registros por requisição
) -> None:
    logging.info(f"Iniciando sincronização fragmentada para {tabela} - sync_data_with_api_by_timekey_chunked()")

    url = f"https://api.mercadoe.com/boost/v1/{tabela}"
    df_geral = pd.DataFrame()

    with engine.connect() as conn:
        check_results = conn.execute(text(f'SELECT count(*) FROM mercado."{tabela}" LIMIT 1')) 
        if check_results.scalar() > 0:
            result = conn.execute(text(f'SELECT "TimeKey" FROM mercado."{tabela}"'))
            existing_timekeys = {row[0] for row in result.fetchall()}
        else:
            logging.warning("Sem registros na tabela")
            existing_timekeys = set()  # Permitir inserção de todos os dados da API

    while url is not None:
        try:
            payload["$top"] = chunk_size  # Limita o número de registros por requisição
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            conteudo = response.json()
            dados = conteudo.get("value", [])

            df = pd.DataFrame(dados)
            df = df.dropna(axis=1, how='all') # Remove colunas com todos os valores nulos
            #df.fillna('')
            df_geral = pd.concat([df_geral, df], ignore_index=True)

            if df_geral.empty:
                logging.info(f"Nenhum dado novo encontrado para {tabela} - sync_data_with_api_by_timekey_chunked()")
                break

            df_geral["TimeKey"] = df_geral["TimeKey"].astype(np.int64)
            df_geral_timekey = df_geral[~df_geral["TimeKey"].isin(existing_timekeys)]

            if not df_geral_timekey.empty:
                try:
                    df_geral_timekey.to_sql(tabela, engine, if_exists="append", index=False, schema="mercado")
                    logging.info(f"Inseridos {len(df_geral_timekey)} registros na tabela {tabela} - sync_data_with_api_by_timekey_chunked()")
                    existing_timekeys.update(df_geral_timekey["TimeKey"].values)
                except Exception as e:
                    logging.error(f"Erro ao inserir dados na tabela {tabela}: {e} - sync_data_with_api_by_timekey_chunked()")

            url = conteudo.get("@odata.nextLink")
            if show_tokens_url:
                logging.info(f"Nova URL para requisição: {url} - sync_data_with_api_by_timekey_chunked()")

        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao requisitar dados da API: {e} - sync_data_with_api_by_timekey_chunked()")
            return
        
    logging.info(f"Sincronização finalizada para {tabela} - sync_data_with_api_by_timekey_chunked()")


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
    try:
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
            logging.info(f"{result.rowcount} registros duplicados removidos da tabela {tabela} - remove_duplicate_records()")
    except Exception as e:
        logging.error(f"Erro ao remover registros duplicados da tabela {tabela}: {e} - remove_duplicate_records()")


def analyze_cardina(
    engine: create_engine,
    tabela: str
) -> None:
    """
    Atualiza as estatísticas de cardinalidade das tabelas no banco de dados.

    Esta função executa o comando ANALYZE no banco de dados, que atualiza as estatísticas das tabelas
    e índices, permitindo ao otimizador de consultas tomar melhores decisões sobre planos de execução.

    Parâmetros:
    -----------
    engine : create_engine
        Objeto de conexão com o banco de dados.

    tabela : str
        Tabela para ser atualizada a cardinalidade

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
    try:
        with engine.connect() as conn:
            query = text(f'ANALYZE mercado."{tabela}"')
            conn.execute(query)
            conn.commit()
            logging.info("Cardinalidade das tabelas atualizada com sucesso - analyze_cardina()")
    except Exception as e:
        logging.error(f"Erro ao atualizar a cardinalidade: {e} - analyze_cardina()")