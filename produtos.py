estoque = {
    "tenis_masculinos": [
        {"nome": "Nike Air Jordan 1 High", "preco": 1299.90, "tamanhos": [39, 40, 41, 42], "cores": ["Chicago (Vermelho/Branco)", "Panda (Preto/Branco)"]},
        {"nome": "Adidas Yeezy Boost 350", "preco": 1599.00, "tamanhos": [40, 41, 42], "cores": ["Onyx (Preto)", "Bone (Bege)"]},
        {"nome": "Nike Dunk Low Retro", "preco": 899.90, "tamanhos": [38, 39, 40, 41, 42, 43], "cores": ["Panda", "Grey"]}
    ],
    "tenis_femininos": [
        {"nome": "Nike Air Force 1 '07", "preco": 799.90, "tamanhos": [34, 35, 36, 37, 38], "cores": ["Branco Clássico"]},
        {"nome": "Vans Old Skool", "preco": 499.90, "tamanhos": [34, 35, 36, 37, 38, 39], "cores": ["Preto", "Xadrez"]}
    ],
    "acessorios": [
        {"nome": "Meia Nike Everyday (Kit 3 pares)", "preco": 59.90, "tamanhos": ["Único"], "cores": ["Branca", "Preta"]},
        {"nome": "Boné New York Yankees", "preco": 199.90, "tamanhos": ["Ajustável"], "cores": ["Azul Marinho", "Preto"]}
    ]
}

def formatar_catalogo():
    """
    Transforma o dicionário de estoque em um texto legível para a IA.
    A IA entende melhor texto corrido do que JSON puro às vezes.
    """
    texto = "CATÁLOGO DE PRODUTOS DISPONÍVEIS AGORA:\n"
    
    for categoria, itens in estoque.items():
        texto += f"\n--- {categoria.upper().replace('_', ' ')} ---\n"
        for item in itens:
            texto += f"- {item['nome']}: R$ {item['preco']:.2f}\n"
            texto += f"  Cores: {', '.join(item['cores'])}\n"
            # Truque para transformar lista de números em texto
            tamanhos_str = [str(t) for t in item['tamanhos']]
            texto += f"  Tamanhos: {', '.join(tamanhos_str)}\n"
            
    return texto

# Teste rápido (se rodar esse arquivo direto)
if __name__ == "__main__":
    print(formatar_catalogo())