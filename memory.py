import sqlite3
import datetime

DB_NAME = "robson_memoria.db"

def iniciar_memoria():
    """Cria o banco de dados se ele não existir"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Cria uma tabela para guardar as contas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cobrancas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            vencimento DATE NOT NULL,
            status TEXT DEFAULT 'pendente'
        )
    ''')
    conn.commit()
    conn.close()

def agendar_pagamento(descricao, valor, vencimento_str):
    """O Robson usa isso para anotar uma nova cobrança"""
    try:
        # Formato esperado do vencimento: YYYY-MM-DD
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cobrancas (descricao, valor, vencimento) 
            VALUES (?, ?, ?)
        ''', (descricao, valor, vencimento_str))
        conn.commit()
        conn.close()
        return f"Anotado. Cobrança de {descricao} no valor de {valor} para o dia {vencimento_str}."
    except Exception as e:
        return f"Erro ao acessar a memória: {e}"

def checar_contas_do_dia():
    """O Robson roda isso todo dia de manhã para ver o que vence hoje"""
    hoje = datetime.date.today().strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT descricao, valor FROM cobrancas 
        WHERE vencimento = ? AND status = 'pendente'
    ''', (hoje,))
    
    contas = cursor.fetchall()
    conn.close()
    
    if contas:
        lista = ", ".join([f"{c[0]} (R$ {c[1]})" for c in contas])
        return f"Aviso proativo: As seguintes contas vencem hoje: {lista}. Deseja que eu inicie o pagamento?"
    return None

# Garante que o banco seja criado na primeira vez
iniciar_memoria()