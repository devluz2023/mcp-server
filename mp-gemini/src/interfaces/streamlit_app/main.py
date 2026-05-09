import streamlit as st
from src.application.services.agent_service import AgentService
from src.domain.use_cases.setup_devops_environment import SetupDevOpsEnvironment
from src.infrastructure.adapters.azure_git_adapter import AzureGitAdapter
from src.infrastructure.config.settings import settings
from src.infrastructure.llm_gateways.openai_gateway import OpenAIGateway

# Inicializa o serviço (maestro)
if "agent" not in st.session_state:
    gateway = OpenAIGateway(api_key=settings.openai_api_key)
    st.session_state.agent = AgentService(llm_provider=gateway)

    azure_adapter = AzureGitAdapter()
    devops_use_case = SetupDevOpsEnvironment(git_service=azure_adapter)

st.set_page_config(page_title="Databricks Assistant", page_icon="🤖")
st.title("🤖 Assistente Databricks")

st.markdown(
    """
    **Comandos Git/DevOps disponíveis:**
    - listar_repositorios
    - commit_e_push_arquivo
    - versionar_arquivo
    - versionar_arquivo_models
    - listar_prs
    - aprovar_pr
    - merge_pr
    - criar_branch
    - criar_repositorio_gitflow

    Use frases como:
    - "listar repositórios"
    - "versionar o arquivo models/meu_arquivo.py no repositório X branch feature/teste"
    - "commitar e dar push de arquivo models/meu_arquivo.py no repositório X branch feature/teste"
    - "criar branch feature/teste no repositório X a partir da main"
    - "listar PRs do repositório X"
    - "aprovar PR 123"
    - "mergear PR 123"
    - "criar repositório com gitflow para x"
    """
)

# Histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input do usuário
if prompt := st.chat_input("Pergunte algo... Ex: listar repositórios, aprovar PR 123"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # A lógica está encapsulada no serviço
        try:
            resposta = st.session_state.agent.process_message(prompt)
            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
        except Exception as e:
            st.error(f"Erro no processamento: {str(e)}")
