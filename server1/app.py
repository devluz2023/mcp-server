import streamlit as st
import asyncio
import docker
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from rag_engine import analisar_log
from agent import processar_interacao



st.set_page_config(page_title="SKU Analytics Control", layout="wide")

st.title("Central de Comando: SKU Analytics")



if prompt := st.chat_input("Ex: 'Rode os testes' ou 'Analise os logs'"):
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Agente está processando..."):
            try:
                # O agente chama a ferramenta automaticamente baseado no texto
                resultado = processar_interacao(prompt)
                st.markdown(resultado["output"])
            except Exception as e:
                st.error(f"Erro: {e}")
                

# --- MONITORAMENTO AUTOMÁTICO ---
@st.fragment(run_every="30s")
def monitor_status_fragment():
    try:
        client = docker.from_env()
        container = client.containers.get("logistica-sku-analytics")
        if container.status != "running":
            st.error(f"🚨 ALERTA CRÍTICO: O container está {container.status.upper()}!")
        else:
            st.success("Status: Pipeline ONLINE")
    except Exception:
        st.warning("⚠️ Monitor desconectado do Docker.")

monitor_status_fragment()

# --- SIDEBAR ---
with st.sidebar:
    st.header("Controles")
    if st.button("Atualizar Status Manual"):
        st.rerun()

# --- ÁREA DE ANÁLISE ---


# Funções Async
async def fetch_log_and_diagnose(container_name):
    server_params = StdioServerParameters(command="python", args=["monitor_server.py"])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            log_result = await session.call_tool("get_docker_logs", {"container_name": container_name})
            log_text = log_result.content[0].text
            diagnostico = analisar_log(log_text)
            return log_text, diagnostico

async def run_tests_async(service_path):
    server_params = StdioServerParameters(command="python", args=["monitor_server.py"])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return await session.call_tool("run_unit_tests", {"service_path": service_path})


container_input = st.text_input("Nome do container:", "logistica-sku-analytics")
prompt_usuario = st.chat_input("Digite 'Analisar Pipeline' ou 'Executar Testes'")

if prompt_usuario:
    st.chat_message("user").markdown(prompt_usuario)
    
    with st.chat_message("assistant"):
        with st.spinner("Executando..."):
            try:
                # Lógica de roteamento simples (SOLID: O app apenas roteia)
                comando = prompt_usuario.lower()
                
                if "analisar" in comando:
                    log_texto, solucao = asyncio.run(fetch_log_and_diagnose(container_input))
                    st.text_area("Logs:", log_texto, height=200)
                    st.success(f"Diagnóstico IA: {solucao}")
                    
                elif "teste" in comando:
                    result = asyncio.run(run_tests_async(container_input))
                    st.code(result.content[0].text, language="bash")
                    
                else:
                    st.warning("Comando não reconhecido. Tente 'Analisar Pipeline' ou 'Executar Testes'.")
                    
            except Exception as e:
                st.error(f"Erro na execução: {e}")

# --- BOTÕES DE AÇÃO ---
if st.button("Analisar Pipeline"):
    with st.spinner("Analisando logs..."):
        try:
            # Substitua o loop complexo por apenas asyncio.run()
            log_texto, solucao = asyncio.run(fetch_log_and_diagnose(container_input))
            st.text_area("Logs:", log_texto, height=200)
            st.success(f"Diagnóstico IA: {solucao}")
        except Exception as e:
            st.error(f"Erro: {e}")



if st.button("Executar Testes Unitários"):
    with st.spinner("Rodando testes..."):
        try:
            # Captura o resultado da chamada assíncrona
            result = asyncio.run(run_tests_async(container_input))
            st.code(result.content[0].text, language="bash")
        except Exception as e:
            # Isso vai revelar o erro real escondido pelo TaskGroup
            import traceback
            st.error(f"Erro completo: {traceback.format_exc()}")