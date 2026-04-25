import streamlit as st
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

import databricks_ops as db

# CONFIG
load_dotenv()

st.set_page_config(page_title="Databricks Assistant", page_icon="🤖")
st.title("🤖 Assistente Databricks")

# =========================
# TOOLS
# =========================
@tool
def listar_jobs_databricks() -> str:
    """
    Use esta função APENAS quando o usuário pedir para ver/listar jobs disponíveis.
    NÃO use para executar jobs.
    """
    return db.listar_jobs()


@tool
def executar_job_databricks(job_id: int) -> str:
    """
    Use esta função quando o usuário pedir explicitamente para executar um job.
    Exemplo: 'execute o job 123'
    """
    return db.executar_job(job_id)


@tool
def verificar_custo_job(run_id: int) -> str:
    """Consulta o custo de uma execução específica"""
    return db.calcular_custo(run_id)


@tool
def criar_job_databricks(nome: str) -> str:
    """
    Use quando o usuário quiser criar um novo job.
    Exemplo: 'crie um job chamado teste'
    """
    return db.criar_job(nome)


@tool
def atualizar_job_databricks(job_id: int, novo_nome: str) -> str:
    """
    Use quando o usuário quiser atualizar um job existente.
    Exemplo: 'atualize o job 123 para novo_nome'
    """
    return db.atualizar_job(job_id, novo_nome)


@tool
def deletar_job_databricks(job_id: int) -> str:
    """
    Use quando o usuário quiser deletar um job.
    Exemplo: 'delete o job 123'
    """
    return db.deletar_job(job_id)

tools = {
    "listar_jobs_databricks": listar_jobs_databricks,
    "executar_job_databricks": executar_job_databricks,
    "verificar_custo_job": verificar_custo_job,
    "criar_job_databricks": criar_job_databricks,
    "atualizar_job_databricks": atualizar_job_databricks,
    "deletar_job_databricks": deletar_job_databricks
}

# =========================
# LLM
# =========================
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

llm_with_tools = llm.bind_tools(list(tools.values()))

# =========================
# UI
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Pergunte algo..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = llm_with_tools.invoke([
                HumanMessage(content=f"""
            Você é um assistente de Databricks.

            Regras:
            - Se o usuário pedir para executar um job, use executar_job_databricks.
            - Se pedir para listar, use listar_jobs_databricks.
            - NÃO confunda as funções.

            Pergunta:
            {prompt}
            """)
            ])

            # 🔥 TOOL CALL
            if response.tool_calls:
                for call in response.tool_calls:
                    name = call["name"]
                    args = call["args"]

                    result = tools[name].invoke(args)

                    st.text(result)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result
                    })

            else:
                reply = response.content
                st.markdown(reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

        except Exception as e:
            st.error(f"Erro: {str(e)}")