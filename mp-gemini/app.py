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
    return db.listar_jobs()

@tool
def executar_job_databricks(job_id: int) -> str:
    return db.executar_job(job_id)

@tool
def verificar_custo_job(run_id: int) -> str:
    return db.calcular_custo(run_id)

tools = {
    "listar_jobs_databricks": listar_jobs_databricks,
    "executar_job_databricks": executar_job_databricks,
    "verificar_custo_job": verificar_custo_job
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
                HumanMessage(content=prompt)
            ])

            # 🔥 TOOL CALL
            if response.tool_calls:
                for call in response.tool_calls:
                    name = call["name"]
                    args = call["args"]

                    result = tools[name].invoke(args)

                    st.markdown(f"🔧 {result}")

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