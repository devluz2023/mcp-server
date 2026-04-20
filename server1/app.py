import streamlit as st
import asyncio
from agents import executar_agente

st.set_page_config(page_title="SKU Analytics", layout="wide")
st.title("📦 Central de Comando: SKU Analytics")

if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Como posso ajudar?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Executa de forma não bloqueante
    with st.spinner("O Agente está processando..."):
        try:
            # Roda a função em uma thread separada para não travar o Streamlit
            resultado = asyncio.run(asyncio.to_thread(executar_agente, prompt))
            resposta = resultado['resposta']
            
            st.chat_message("assistant").markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
        except Exception as e:
            st.error(f"Erro: {e}")