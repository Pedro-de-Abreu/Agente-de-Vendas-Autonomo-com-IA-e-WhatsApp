import os
import uvicorn
import json
from fastapi import FastAPI, HTTPException, Form, Response
from fastapi.responses import HTMLResponse # Import necessário para o Painel
from pydantic import BaseModel
import google.generativeai as genai 
from dotenv import load_dotenv

# Importa o banco e o catálogo
import banco_de_dados
import produtos 

# --- 1. CONFIGURAÇÃO ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Chave não encontrada no .env!")

genai.configure(api_key=API_KEY)

# --- 2. FUNÇÕES E CÉREBRO ---
def finalizar_compra(user_id: str, produto: str, tamanho: str, endereco: str, metodo_pagamento: str):
    """
    Registra uma venda completa no sistema.
    """
    # Forçamos o retorno a ser uma string simples
    return str(banco_de_dados.salvar_pedido(user_id, produto, tamanho, endereco, metodo_pagamento))

catalogo_texto = produtos.formatar_catalogo()

regras_de_vendas = f"""
Você é a Maria Luiza, vendedora da loja King Shoes.

SUAS DIRETRIZES:
1. Use APENAS o catálogo abaixo para responder.
2. Seja simpática e breve.
3. Se o cliente tiver fornecido TODAS as informações (produto, tamanho, endereço, pagamento), chame a função finalizar_compra.

ESTOQUE ATUAL:
{catalogo_texto}
"""

model = genai.GenerativeModel(
    'models/gemini-2.5-flash',
    system_instruction=regras_de_vendas,
    tools=[finalizar_compra]
)

app = FastAPI(title="Agente de Vendas King Shoes")

class UserMessage(BaseModel):
    user_id: str
    message: str

# --- 3. ROTA DO PAINEL ADMINISTRATIVO (VISUAL) ---
@app.get("/admin", response_class=HTMLResponse)
async def admin_panel():
    # 1. Busca os dados no banco
    pedidos = banco_de_dados.listar_pedidos()
    
    # 2. Cria as linhas da tabela HTML
    linhas_tabela = ""
    for p in pedidos:
        # p é uma tupla: (id, user_id, produto, tamanho, endereco, pgto, data)
        linhas_tabela += f"""
        <tr>
            <td>#{p[0]}</td>
            <td>{p[6]}</td>
            <td><strong>{p[2]}</strong></td>
            <td>{p[3]}</td>
            <td>{p[1]}</td>
            <td>{p[4]}</td>
            <td><span class="badge">{p[5]}</span></td>
        </tr>
        """

    # 3. O HTML completo da página
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Painel King Shoes</title>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #f4f4f9; padding: 20px; }}
            h1 {{ color: #333; text-align: center; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ background-color: #4CAF50; color: white; padding: 12px; text-align: left; }}
            td {{ padding: 12px; border-bottom: 1px solid #ddd; color: #555; }}
            tr:hover {{ background-color: #f1f1f1; }}
            .badge {{ background-color: #2196F3; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.9em; }}
            .total {{ margin-top: 20px; font-size: 1.2em; font-weight: bold; text-align: right; color: #333; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👟 Painel Administrativo King Shoes</h1>
            <p>Acompanhamento de vendas em tempo real.</p>
            
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Data</th>
                        <th>Produto</th>
                        <th>Tam.</th>
                        <th>Cliente (Tel)</th>
                        <th>Endereço</th>
                        <th>Pagamento</th>
                    </tr>
                </thead>
                <tbody>
                    {linhas_tabela}
                </tbody>
            </table>
            
            <div class="total">Total de Vendas: {len(pedidos)}</div>
        </div>
    </body>
    </html>
    """
    return html_content

# --- 4. ROTA DE TESTE LOCAL ---
@app.post("/chat")
async def chat_with_agent(user_msg: UserMessage):
    try:
        chat_id = user_msg.user_id
        historico = banco_de_dados.carregar_historico(chat_id)
        chat_session = model.start_chat(history=historico)
        banco_de_dados.salvar_mensagem(chat_id, "user", user_msg.message)
        response = chat_session.send_message(user_msg.message)
        
        if hasattr(response, 'text') and response.text:
            banco_de_dados.salvar_mensagem(chat_id, "model", response.text)
        
        return {"response": response.text if hasattr(response, 'text') else "Processando..."}
    except Exception as e:
        print(f"Erro local: {e}") 
        raise HTTPException(status_code=500, detail="Erro interno")

# --- 5. ROTA WHATSAPP (A FINAL E FUNCIONAL) ---
@app.post("/whatsapp")
async def reply_whatsapp(Body: str = Form(), From: str = Form()):
    try:
        chat_id = From
        msg_cliente = Body
        print(f"--- ZAP RECEBIDO DE: {chat_id} ---")

        # Carregar histórico e limpar se necessário
        historico_completo = banco_de_dados.carregar_historico(chat_id)
        if len(historico_completo) > 5 and msg_cliente.lower() in ["olá", "oi", "ola", "tudo bem"]:
            historico_completo = []
            print("--- Histórico limpo ---")

        conteudo_da_conversa = historico_completo + [{'role': 'user', 'parts': [{'text': msg_cliente}]}]
        banco_de_dados.salvar_mensagem(chat_id, "user", msg_cliente)
        
        pedido_salvo_com_sucesso = False 
        
        # Loop de Function Calling
        while True:
            response = model.generate_content(
                contents=conteudo_da_conversa,
                tools=[finalizar_compra]
            )

            if hasattr(response, 'function_calls') and response.function_calls:
                print("--- IA chamou a função finalizar_compra! ---")
                
                fc = response.function_calls[0]
                # Tratamento robusto de JSON
                try:
                    # Tenta converter argumentos, se já não for dict
                    f_args = json.loads(fc.args) if isinstance(fc.args, str) else dict(fc.args)
                except:
                    # Se falhar a conversão direta, tenta usar como dict direto (padrão Google SDK)
                    f_args = dict(fc.args)

                # Executa o salvamento
                try:
                    finalizar_compra(
                        user_id=str(f_args.get('user_id', chat_id)),
                        produto=str(f_args.get('produto', 'N/A')),
                        tamanho=str(f_args.get('tamanho', 'N/A')),
                        endereco=str(f_args.get('endereco', 'N/A')),
                        metodo_pagamento=str(f_args.get('metodo_pagamento', 'N/A'))
                    )
                    pedido_salvo_com_sucesso = True
                    print("--- SUCESSO: PEDIDO SALVO! ---")
                except Exception as e:
                    print(f"Erro ao salvar: {e}")
                
                break # Sai do loop para confirmar
            
            break

        # Resposta Final
        if pedido_salvo_com_sucesso:
            texto_final = "Tudo certo! Seu pedido foi registrado. Maria Luiza enviará os dados para pagamento. Muito obrigado(a) pela compra! 👟"
            banco_de_dados.salvar_mensagem(chat_id, "model", texto_final)
        elif hasattr(response, 'text') and response.text:
             texto_final = response.text
             banco_de_dados.salvar_mensagem(chat_id, "model", texto_final)
        else:
             texto_final = "Desculpe, tive um erro técnico. Tente novamente."

        # Limpeza visual
        texto_final = texto_final.replace("**", "*").replace("* ", "👟 ")

        xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Response><Message>{texto_final}</Message></Response>"""
        
        return Response(content=xml_response, media_type="application/xml")

    except Exception as e:
        print(f"ERRO GERAL: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    banco_de_dados.criar_tabela()
    banco_de_dados.criar_tabela_pedidos()
    uvicorn.run(app, host="0.0.0.0", port=8000)