# 🤖 Agente Autônomo de Vendas - WhatsApp & IA (Gemini)

## 🎯 O Problema
No ambiente dinâmico do e-commerce, o tempo de resposta é crucial para a conversão de vendas. Este projeto foi concebido para resolver o gargalo do primeiro atendimento, buscando automatizar o contato inicial, qualificar leads e direcionar o suporte ao cliente de forma rápida, inteligente e com linguagem natural.

## 💡 A Solução
Desenvolvi um agente autônomo integrado ao WhatsApp utilizando **Python** e a **API do Google Gemini**. O bot recebe a mensagem do usuário, analisa a intenção da compra ou dúvida através da Inteligência Artificial Generativa, e formula uma resposta baseada no contexto do negócio para realizar a qualificação inicial antes de repassar o contato para um atendente humano.

> **⚠️ Status do Projeto (Ambiente Controlado)**
> Este projeto é uma **Prova de Conceito (PoC)**. A aplicação foi validada com sucesso em um ambiente de testes controlados (sandbox), cumprindo todos os requisitos lógicos, tratamento de erros e integração propostos. A arquitetura está funcional, porém o sistema ainda não foi exposto ao tráfego do público final em ambiente de produção comercial.

## 🛠️ Tecnologias Utilizadas
*   **Python:** Linguagem principal para estruturação do backend e lógica de negócios.
*   **Google Gemini API:** Motor de IA Generativa utilizado para o Processamento de Linguagem Natural (NLP) e tomada de decisão no fluxo de conversa.
*   **Integração WhatsApp:** Ferramenta/Biblioteca para recebimento e envio das mensagens.
*   **Arquitetura:** Lógica de qualificação de leads e separação de variáveis de ambiente (`.env`) para segurança de chaves de API.

## ⚙️ Como Funciona o Fluxo
1. O cliente envia uma mensagem via WhatsApp.
2. O script em Python intercepta a mensagem e envia o conteúdo para a API do Gemini, acompanhado de um *prompt* de sistema (comportamento esperado do vendedor).
3. A IA processa a entrada, classifica o grau de interesse do lead e gera uma resposta adequada.
4. A automação devolve a mensagem ao cliente ou sinaliza a necessidade de intervenção humana.

## 🚀 Como Executar o Projeto Localmente

**Pré-requisitos:** Python 3.x instalado e uma chave válida da API do Google Gemini.


📸 Screenshots

![alt text](image.png)
![alt text](image-1.png)



1. Clone este repositório:
   ```bash
   git clone [https://github.com/pedro-de-abreu/](https://github.com/pedro-de-abreu/)[nome-do-repositorio].git


Desenvolvido por Pedro de Abreu🚀
