import requests

# URL da sua API
url = "http://127.0.0.1:8000/chat"

# Simula seu número de telefone (ID único)
meu_id = "5511999999999"

print("--- INICIANDO CHAT COM A MARIA LUIZA (COM MEMÓRIA) ---")
print("(Digite 'sair' para encerrar)\n")

while True:
    # 1. Você digita no terminal
    texto_usuario = input("Você: ")
    
    if texto_usuario.lower() == "sair":
        break

    # 2. Montamos o pacote para enviar (Agora com user_id!)
    dados = {
        "user_id": meu_id,
        "message": texto_usuario
    }

    # 3. Envia para a API
    try:
        resposta = requests.post(url, json=dados)
        
        # Verifica se deu certo (Código 200)
        if resposta.status_code == 200:
            resposta_ia = resposta.json()['response']
            print(f"Malu: {resposta_ia}\n")
        else:
            # Se der erro, mostra o motivo
            print("Erro na API:", resposta.text)
            
    except Exception as e:
        print("Erro de conexão:", e)