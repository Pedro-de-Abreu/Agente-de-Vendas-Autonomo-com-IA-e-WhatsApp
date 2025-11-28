import sqlite3
from datetime import datetime

# Nome do arquivo onde tudo ficará salvo
NOME_BANCO = "loja_database.db"

def conectar():
    """Conecta ao banco de dados SQLite"""
    return sqlite3.connect(NOME_BANCO)

def criar_tabela():
    """Cria a tabela de histórico se ela não existir"""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def criar_tabela_pedidos():
    """Cria a tabela de pedidos se ela não existir"""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        produto TEXT NOT NULL,
        tamanho TEXT NOT NULL,
        endereco TEXT NOT NULL,
        metodo_pagamento TEXT NOT NULL,
        data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def salvar_mensagem(user_id, role, content):
    """Salva uma mensagem no banco"""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO historico (user_id, role, content)
    VALUES (?, ?, ?)
    """, (user_id, role, content))
    
    conn.commit()
    conn.close()

def carregar_historico(user_id):
    """Lê todas as mensagens antigas de um usuário"""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT role, content 
    FROM historico 
    WHERE user_id = ? 
    ORDER BY id ASC
    """, (user_id,))
    
    mensagens = cursor.fetchall()
    conn.close()
    
    historico_formatado = []
    for role, content in mensagens:
        historico_formatado.append({
            "role": role,
            "parts": [{"text": content}] # Formato compatível com SDK nativo
        })
        
    return historico_formatado

def salvar_pedido(user_id, produto, tamanho, endereco, metodo_pagamento):
    """Salva o pedido finalizado no banco de dados"""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO pedidos (user_id, produto, tamanho, endereco, metodo_pagamento)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, produto, tamanho, endereco, metodo_pagamento))
    
    conn.commit()
    conn.close()
    
    print(f"PEDIDO REGISTRADO NO BANCO para {user_id}: {produto}")
    return "Pedido salvo com sucesso."

def listar_pedidos():
    """Retorna todos os pedidos para o Painel Admin"""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, user_id, produto, tamanho, endereco, metodo_pagamento, data_pedido 
    FROM pedidos 
    ORDER BY id DESC
    """)
    
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos

if __name__ == "__main__":
    criar_tabela()
    criar_tabela_pedidos()
    print("--- Tabelas verificadas com sucesso ---")