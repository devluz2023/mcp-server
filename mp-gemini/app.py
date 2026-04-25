import streamlit as st
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

import databricks_ops as db

# =========================
# CONFIG
# =========================
load_dotenv()

st.set_page_config(page_title="Databricks Assistant", page_icon="🤖")
st.title("🤖 Assistente Databricks")

# =========================
# TOOLS (WRAPPERS)
# =========================

@tool
def listar_jobs_databricks() -> str:
    """Lista jobs no Databricks"""
    return db.listar_jobs()

@tool
def executar_job_databricks(job_id: int) -> str:
    """Executa job no Databricks"""
    return db.executar_job(job_id)

@tool
def criar_job_databricks(nome: str) -> str:
    """Cria job no Databricks"""
    return db.criar_job(nome)

@tool
def atualizar_job_databricks(job_id: int, novo_nome: str) -> str:
    """Atualiza job no Databricks"""
    return db.atualizar_job(job_id, novo_nome)

@tool
def deletar_job_databricks(job_id: int) -> str:
    """Deleta job no Databricks"""
    return db.deletar_job(job_id)

@tool
def criar_dashboard_databricks() -> str:
    """Cria dashboard no Databricks"""
    return db.criar_dashboard_padrao()

@tool
def pipeline_databricks() -> str:
    """
    Pipeline completo: CSV → Delta → Feature Store
    """
    return db.executar_pipeline_fixo()

@tool
def deploy_modelo_databricks(nome_modelo: str) -> str:
    """Faz deploy de modelo Python"""
    return db.deploy_modelo(nome_modelo)

@tool
def listar_modelos() -> str:
    """Lista modelos locais"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "..", "models")

    return "\n".join([
        f for f in os.listdir(models_dir)
        if f.endswith(".py")
    ])


# =========================
# TOOL REGISTRY (IMPORTANTE)
# =========================
tools = {
    "listar_jobs_databricks": listar_jobs_databricks,
    "executar_job_databricks": executar_job_databricks,
    "criar_job_databricks": criar_job_databricks,
    "atualizar_job_databricks": atualizar_job_databricks,
    "deletar_job_databricks": deletar_job_databricks,
    "criar_dashboard_databricks": criar_dashboard_databricks,
    "deploy_modelo_databricks": deploy_modelo_databricks,
    "listar_modelos": listar_modelos,
    "pipeline_databricks":pipeline_databricks
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
# MEMORY
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# CHAT HISTORY
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# INPUT
# =========================
if prompt := st.chat_input("Pergunte algo..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        try:
            response = llm_with_tools.invoke([
                HumanMessage(content=f"""
Você é um assistente de Databricks.

REGRAS:
- Use tools corretamente.
- NÃO invente funções.
- Se precisar listar modelos use listar_modelos.
- Se precisar deploy use deploy_modelo_databricks.



Pergunta:
{prompt}
""")
            ])

            # =========================
            # TOOL EXECUTION SAFE LOOP FIX
            # =========================
            executed = set()

            if response.tool_calls:

                for call in response.tool_calls:
                    name = call["name"]

                    if name in executed:
                        continue

                    executed.add(name)

                    args = call.get("args", {})

                    if name in tools:
                        result = tools[name].invoke(args)
                    else:
                        result = f"Tool não encontrada: {name}"

                    st.markdown(result)

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


