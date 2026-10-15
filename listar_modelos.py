import os
from openai import OpenAI
from dotenv import load_dotenv

# Use load_dotenv("tarsvis.env") se você manteve aquele nome de arquivo no passo anterior
load_dotenv() 

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

print("Consultando servidores... Modelos disponíveis no Groq agora:")
# Acessa a lista de modelos ativos na sua conta
modelos_ativos = client.models.list()

for modelo in modelos_ativos.data:
    print(f"- {modelo.id}")