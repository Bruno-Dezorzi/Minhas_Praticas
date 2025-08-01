import time
import requests
from sqlalchemy import create_engine
import pandas as pd
import funcoes as f
from datetime import datetime
import logging

# Configuração do logger
logging.basicConfig(
    filename=f"logs/log_execucao_{datetime.now().strftime('%Y-%m-%d')}.log",  # Nome do arquivo de log com a data no formato YYYY-MM-DD
    level=logging.INFO,  # Nível mínimo de log (INFO, DEBUG, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato das mensagens
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)  # Criar um logger


def processar_grupos(grupo, tabelas, ENGINE, HEADERS, PAYLOAD, chunked=False):
    """Processa um grupo de tabelas com sleep entre as execuções para evitar o timeout"""
    for tabela in tabelas:

        response = requests.get(url= f'https://xxxxx/{tabela}' , headers=HEADERS, params=PAYLOAD)
        response.raise_for_status()
        conteudo = response.json()
        dados = conteudo.get("value", [])

        df = pd.DataFrame(dados)

        if not df.empty:

            logger.info(f"Iniciando processamento da tabela {tabela} no {grupo}.")

            
            # Sincronizando dados com a API
            logger.info(f"Sincronizacao inicial começou da tabela {tabela}.")
            f.sync_data_with_api_by_timekey(tabela=tabela, engine=ENGINE, headers=HEADERS, payload=PAYLOAD, show_tokens_url=False)
            logger.info(f"Sincronizacao concluída para {tabela}.")

            # Analisando a cardinalidade
            logger.info(f"Analisando cardinalidade da tabela {tabela}.")
            f.analyze_cardina(engine=ENGINE, tabela=tabela)
            logger.info(f"Analise de cardinalidade concluida para {tabela}.")

            # Removendo duplicatas
            logger.info(f"Removendo duplicatas da tabela {tabela}.")
            f.remove_duplicate_records(tabela=tabela, engine=ENGINE)
            logger.info(f"Remocao de duplicatas concluida para {tabela}.")

            # Atualizando dados com a API
            logger.info(f"Atualizando dados da tabela {tabela}.")
            f.update_db_with_api_data(tabela=tabela, engine=ENGINE, headers=HEADERS, payload=PAYLOAD)
            logger.info(f"Atualização concluída para {tabela}.")
            
            '''# Aguardar 1 minuto antes de passar para o próximo
            logger.info(f"Aguardando 10 segundos antes de processar a próxima tabela.")
            time.sleep(10)  # Espera de 1 minuto'''
        else:
            logging.warning(f"Sem dados na API para a tabela {tabela}")



def main():
    logger.info("INICIANDO A EXECUCAO DO SCRIPT.")

    grupo_teste = ['OrderItems'] 
    grupo_isolado = ['PreOrderItemAttributes','OrderItemAttributes']  # Estudar esses casos
    grupo_vazio = ['InvoiceAttributes','RfqBorgs','RfqTasks','ServiceOrders','ServiceSheets','SupplierBorgs','RfqTaskEvaluationResponses']
    grupo_1 = ['ContractAttributeValues', 'OrderItemRequests', 'OrderItemDeliveries', 'PreOrderAddresses','InvoiceAttributes']
    grupo_2 = ['PreOrderItemRequests', 'PreOrderItemDeliveries', 'PreOrderApprovals', 'PreOrderAttributes']
    grupo_3 = ['RfqItemAttributeValues', 'ProductAttributes', 'InvoiceItemAttributes', 'Contracts']
    grupo_4 = ['ContractItems', 'ContractBorgs', 'Users', 'Requests', 'RequestBorgs']
    grupo_5 = ['Orders', 'OrderBorgs', 'OrderItems', 'OrderItemBorgs', 'OrderItemDates']
    grupo_track = ['TrackingTransactions']
    grupo_6 = ['PreOrders', 'PreOrderBorgs', 'PreOrderItems', 'PreOrderItemBorgs', 'Rfqs']
    grupo_7 = ['RfqBorgs', 'RfqItems', 'RfqAttendees', 'OrderAddresses', 'RfqTasks']
    grupo_8 = ['Products', 'ServiceOrders', 'Invoices', 'InvoiceItems', 'ServiceSheets']
    grupo_9 = ['Suppliers', 'SupplierGroups', 'SupplierBorgs', 'RequestApprovalsUserGroups', 'RfqResponseItemCounterProposals']
    grupo_10 = ['RequestItemDeliverySchedules', 'RfqTaskEvaluationResponses', 'RequestApprovalHistory', 'RequestItems', 'RequestItemBorgs']



    PAYLOAD = {}
    HEADERS = {
        "Authorization": "Basic xxxxxxx="  # Substitua pela sua chave de autorização
    }

    ENGINE = create_engine("xxxxx", echo=False)  # Substitua pela URL do seu banco de dados
    URL = "https://xxxxxx/"

    try:
        response = requests.request("GET", URL, headers=HEADERS, data=PAYLOAD)
        response.raise_for_status()  # Verifica se houve erro na requisição HTTP
        conteudo = response.json()
        dados = conteudo.get("value")

        df = pd.DataFrame(dados)
        #tabelas = list(df["url"])

        tempo_inicial = time.time()

        # Processando os grupos com sleep entre cada execução
        #processar_grupos("Grupo Teste", grupo_teste, ENGINE, HEADERS, PAYLOAD)
        processar_grupos("Grupo 1", grupo_1, ENGINE, HEADERS, PAYLOAD)
        processar_grupos("Grupo 2", grupo_2, ENGINE, HEADERS, PAYLOAD)
        processar_grupos("Grupo 3", grupo_3, ENGINE, HEADERS, PAYLOAD)
        processar_grupos("Grupo 4", grupo_4, ENGINE, HEADERS, PAYLOAD)
        processar_grupos("Grupo 5", grupo_5, ENGINE, HEADERS, PAYLOAD)
        processar_grupos("Grupo 6", grupo_6, ENGINE, HEADERS, PAYLOAD)
        processar_grupos("Grupo 7", grupo_7, ENGINE, HEADERS, PAYLOAD)
        processar_grupos("Grupo 8", grupo_8, ENGINE, HEADERS, PAYLOAD)
        processar_grupos("Grupo 9", grupo_9, ENGINE, HEADERS, PAYLOAD)
        processar_grupos("Grupo 10", grupo_10, ENGINE, HEADERS, PAYLOAD)
        processar_grupos("Grupo Track", grupo_track, ENGINE, HEADERS, PAYLOAD)
        #processar_grupos("Grupo Isolado", grupo_isolado, ENGINE, HEADERS, PAYLOAD)

    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}", exc_info=True)

    tempo_final = time.time()
    tempo_total = tempo_final - tempo_inicial

    horas = tempo_total // 3600
    minutos = (tempo_total % 3600) // 60
    segundos = tempo_total % 60

    logger.info(f"Tempo total de execucao: {int(horas)}h {int(minutos)}m {int(segundos)}s.")
    logger.info("EXECUCAO DE SCRIPT FINALIZADA")


if __name__ == "__main__":
    main()