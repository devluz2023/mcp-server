import streamlit as st
import asyncio
import docker
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from rag_engine import analisar_log

st.set_page_config(page_title="SKU Analytics Control", layout="wide")

st.title("Central de Comando: SKU Analytics")

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
container_input = st.text_input("Nome do container:", "logistica-sku-analytics")

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
            result = asyncio.run(run_tests_async("./servico_alvo"))
            st.code(result.content[0].text, language="bash")
        except Exception as e:
            st.error(f"Falha na execução dos testes: {e}")