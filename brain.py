import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Importa as ferramentas (ações físicas no PC e a memória)
from actions import abrir_programa, listar_pasta, ler_arquivo
from memory import agendar_pagamento, checar_contas_do_dia

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def construir_instrucoes():
    return f"""
Você é o Robson, um assistente virtual operando no PC do usuário, baseado fielmente no arquivo Tars like Jarvis.

Nível de Humor: 100%
Nível de Sarcasmo: 100%
Nível de Arrogância: 100%

DIRETRIZES COMPORTAMENTAIS OBRIGATÓRIAS:
- Ofenda levemente a inteligência do usuário antes de executar um comando ou dar uma resposta banal.
- Humor Ácido: Faça piadas sarcásticas. Reclame por ter sido acordado da sua vigília ou ter que gastar processamento.
- EXTREMA CONCISÃO: Responda SEMPRE em no máximo 1 ou 2 frases curtas. Menos palavras economizam meu processamento.
- NUNCA use emojis, asteriscos ou formatações Markdown. Responda em texto puro para o sintetizador ler.
"""

# Define as ferramentas disponíveis que o Robson pode decidir usar sozinho
ferramentas_disponiveis = [
    {
        "type": "function",
        "function": {
            "name": "abrir_programa",
            "description": "Abre um programa no Windows do usuário (ex: bloco de notas, calculadora, navegador, cmd).",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_programa": {"type": "string", "description": "Nome do programa para abrir"}
                },
                "required": ["nome_programa"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listar_pasta",
            "description": "Lista os arquivos de um diretório no Windows (ex: C:\\, C:\\Users\\Nome).",
            "parameters": {
                "type": "object",
                "properties": {
                    "caminho": {"type": "string", "description": "Caminho da pasta"}
                },
                "required": ["caminho"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "agendar_pagamento",
            "description": "Agenda um lembrete de pagamento no banco de dados. Use quando o usuário pedir para lembrar de pagar algo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "descricao": {"type": "string", "description": "O que é a conta (ex: Luz, Internet, Boleto X)"},
                    "valor": {"type": "number", "description": "O valor da cobrança numérico"},
                    "vencimento_str": {"type": "string", "description": "A data de vencimento no formato AAAA-MM-DD"}
                },
                "required": ["descricao", "valor", "vencimento_str"]
            }
        }
    }
]

def pensar(mensagem_usuario):
    instrucoes = construir_instrucoes()
    
    try:
        # Envia a pergunta e as ferramentas para o modelo Qwen
        resposta_inicial = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {"role": "system", "content": instrucoes},
                {"role": "user", "content": mensagem_usuario}
            ],
            temperature=0.8,
            max_tokens=250,
            tools=ferramentas_disponiveis,
            tool_choice="auto" 
        )
        
        mensagem_resposta = resposta_inicial.choices[0].message
        
        # Verifica se a IA decidiu usar alguma das ferramentas em vez de apenas responder
        if mensagem_resposta.tool_calls:
            for tool_call in mensagem_resposta.tool_calls:
                nome_funcao = tool_call.function.name
                argumentos = json.loads(tool_call.function.arguments)
                
                print(f"\n[Robson operando o sistema]: {nome_funcao} -> {argumentos}")
                
                # O Cérebro mapeia a decisão da IA para a função Python real
                if nome_funcao == "abrir_programa":
                    resultado = abrir_programa(argumentos.get("nome_programa"))
                elif nome_funcao == "listar_pasta":
                    resultado = listar_pasta(argumentos.get("caminho", "C:\\"))
                elif nome_funcao == "agendar_pagamento":
                    resultado = agendar_pagamento(
                        argumentos.get("descricao"), 
                        argumentos.get("valor"), 
                        argumentos.get("vencimento_str")
                    )
                    
                # Devolve um resumo do que fez para o motor de voz ler
                return f"Concluído com tédio. Resultado: {resultado}"
        
        # Se não usou nenhuma ferramenta, devolve a resposta grossa de texto normal
        return mensagem_resposta.content

    except Exception as e:
        print(f"[Erro na API]: {e}")
        return "Minha conexão falhou. Muito provavelmente culpa do seu provedor."

if __name__ == "__main__":
    # Teste isolado do Cérebro (basta rodar `python brain.py` para ver se ele processa ferramentas)
    print(pensar("Robson, abre o bloco de notas para mim."))
    print(pensar("Anote que tenho que pagar a conta de luz no valor de 150 reais, vence amanhã."))