import streamlit as st  # CORRETO

# 1. Configurações
from config import settings

# 2. Infraestrutura (Adapters e Gateways)
from src.infrastructure.adapters.git_adapter import GitAdapter
from src.infrastructure.adapters.job_adapter import JobAdapter
from src.infrastructure.services.openai_gateway import OpenAIGateway

# 3. Aplicação (Use Cases)
from src.application.use_cases.git_automation import GitAutomationUseCase
from src.application.use_cases.job_automation import JobAutomationUseCase

# 4. Domínio (Services) e Registro de Tools
from src.domain.services.agent_service import AgentService
from src.interfaces.tools.agent_tools import initialize_tools

# Configuração visual
st.set_page_config(page_title="Assistente MLOps", page_icon="🤖")
st.title("🤖 Assistente de MLOps Databricks")


# --- BOOTSTRAP DA APLICAÇÃO (Executado uma vez) ---
if "agent" not in st.session_state:
    try:
        # A. Inicializa Infra
        gateway = OpenAIGateway(api_key=settings.OPENAI_API_KEY)
        azure_adapter = GitAdapter()
        db_adapter = JobAdapter()

        # B. Inicializa Use Cases
        git_use_Case = GitAutomationUseCase(git_repository=azure_adapter)
        job_use_case = JobAutomationUseCase(job_repository=db_adapter)

        # C. Registra as Tools injetando os Use Cases nelas
        # Isso permite que a Tool dentro do AgentService tenha "poder" de execução
        initialize_tools(git_uc=git_use_Case, job_uc=job_use_case)

        # D. Inicializa o Maestro (AgentService)
        st.session_state.agent = AgentService(llm_provider=gateway)

    except Exception as e:
        st.error(f"Falha na inicialização do sistema: {e}")

# --- INTERFACE DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input do Usuário
if prompt := st.chat_input("Ex: 'Crie uma branch feature/modelo-novo e liste os jobs'"):
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Processamento via Maestro
    with st.chat_message("assistant"):
        try:
            # O AgentService orquestra: LLM -> Tool Call -> Use Case -> Resposta
            resposta = st.session_state.agent.process_message(prompt)

            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})

        except Exception as e:
            st.error(f"Erro ao processar solicitação: {str(e)}")
