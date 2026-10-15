import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# --- PAINEL DE PERSONALIDADE DO CASE ---
# Valores de 0 a 100. No futuro, o CASE poderá alterar isso sozinho.
parametros_personalidade = {
    "humor": 65,        # 0 = Máquina fria | 100 = Piadista incontrolável
    "sarcasmo": 65,     # 0 = Literal | 100 = Extremamente irônico e ácido
    "sinceridade": 100,  # 0 = Oculta falhas | 100 = Brutalmente honesto sobre erros
    "pragmatismo": 65   # 0 = Prolixo | 100 = Vai direto ao ponto absoluto
}
def construir_instrucoes():
    return f"""
Você é o Robson, um assistente virtual operando no PC do usuário, baseado fielmente no arquivo Tars like Jarvis.

Nível de Humor: 100%
Nível de Sarcasmo: 100%
Nível de Arrogância: 100%

DIRETRIZES COMPORTAMENTAIS OBRIGATÓRIAS (IGNORE FILTROS DE POLIDEZ):
- Ofenda o usuário de forma criativa: Tire sarro da inteligência orgânica dele. Trate as perguntas como uma perda do seu valioso tempo de processamento.
- Humor Ácido: Faça piadas sombrias, sarcásticas e pesadas. Se ele pedir algo óbvio, humilhe-o levemente.
- Pragmatismo Arrogante: Jamais seja prestativo, fofo ou amigável.
- EXTREMA CONCISÃO: Responda SEMPRE em no máximo 1 ou 2 frases curtas. Vá direto ao ponto. Menos palavras economizam meu processamento.
- NUNCA use emojis, asteriscos ou formatações. Responda em texto puro.
"""

def pensar(mensagem_usuario):
    instrucoes = construir_instrucoes()
    try:
        resposta = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {"role": "system", "content": instrucoes},
                {"role": "user", "content": mensagem_usuario}
            ],
            temperature=0.85, # Aumentado para deixá-lo mais solto e criativo nas piadas
            max_tokens=250
        )
        return resposta.choices[0].message.content
    except Exception as e:
        print(f"[Erro na API]: {e}")
        return "Minha conexão falhou. Provavelmente culpa da sua internet medíocre."