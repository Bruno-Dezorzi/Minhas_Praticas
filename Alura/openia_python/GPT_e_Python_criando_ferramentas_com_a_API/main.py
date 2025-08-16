import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

resposta = cliente.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "Listar apenas os nomes dos produtos, sem considerar a descrição",
        },
        {
            "role": "user",
            "content": "Liste 3 produtos sustentáveis",
        },
    ]
)

print(resposta.choices[0].message.content)
