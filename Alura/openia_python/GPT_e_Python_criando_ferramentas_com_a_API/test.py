import psycopg2
from openai import OpenAI

# --- CONFIG OPENAI ---
OPENAI_API_KEY = "SUA_CHAVE_AQUI"
client = OpenAI(api_key=OPENAI_API_KEY)

# --- CONFIG BANCO ---
DB_NAME = "reparai"
DB_USER = "postgres"
DB_PASSWORD = "123456"
DB_HOST = "localhost"
DB_PORT = "5432"

# --- FUNÇÃO PARA CONECTAR AO BANCO ---
def conectar_banco():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# --- FUNÇÃO PARA BUSCAR PROFISSIONAIS FILTRADOS ---
def buscar_profissionais(servico: str, limite: int = 5):
    query = """
        SELECT 
            p.nome AS nome_prestador,
            e.nome AS especialidade,
            pr.nota_media,
            en.bairro,
            en.cidade
        FROM dim_prestador pr
        JOIN dim_pessoa p ON pr.id_pessoa = p.id_pessoa
        JOIN dim_especialidade_prestador ep ON pr.id_prestador = ep.id_prestador
        JOIN dim_especialidade e ON ep.id_especialidade = e.id_especialidade
        JOIN dim_endereco en ON p.id_endereco = en.id_endereco
        WHERE e.nome ILIKE %s
        ORDER BY pr.nota_media DESC
        LIMIT %s;
    """
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute(query, (f"%{servico}%", limite))
    dados = cur.fetchall()
    colunas = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return [dict(zip(colunas, row)) for row in dados]

# --- FUNÇÃO PARA CONSULTAR O LLM ---
def consultar_llm(servico, profissionais):
    prompt = f"""
    Você é um assistente que recomenda prestadores de serviços.
    O usuário pediu: "{servico}".
    Base de dados (profissionais filtrados):
    {profissionais}

    Formate a resposta de forma amigável, listando os nomes, especialidades, notas
    e bairros, recomendando os melhores.
    """
    resposta = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return resposta.output_text

# --- FLUXO PRINCIPAL ---
if __name__ == "__main__":
    servico_desejado = input("Digite o serviço desejado (ex: eletricista, pintor): ")
    profissionais = buscar_profissionais(servico_desejado)

    if profissionais:
        resposta_llm = consultar_llm(servico_desejado, profissionais)
        print("\n--- Recomendações ---")
        print(resposta_llm)
    else:
        print("Nenhum profissional encontrado para esse serviço.")
