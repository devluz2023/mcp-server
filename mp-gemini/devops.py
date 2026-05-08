import os
from dotenv import load_dotenv
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.git.models import GitPullRequestSearchCriteria
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from azure.devops.v7_1.git.models import GitPullRequestCompletionOptions
load_dotenv()

# --- 1. CONEXÕES ---
def obter_conexao():
    pat = os.getenv('PERSONAL_ACCESS_TOKEN')
    org_url = os.getenv('ORGANIZATION_URL')
    credentials = BasicAuthentication('', pat)
    return Connection(base_url=org_url, creds=credentials)

def obter_meu_id(connection):
    """Descobre o ID do usuário vinculado ao PAT de forma oficial"""
    # Usamos o cliente de Identidade para buscar o perfil logado
    identity_client = connection.clients.get_identity_client()
    config_client = connection.clients.get_location_client()
    
    # Busca informações da conexão atual
    connection_data = config_client.get_connection_data()
    meu_id = connection_data.authenticated_user.id
    return meu_id

# --- 2. ANÁLISE E VOTO ---
def aprovar_pull_request(git_client, pr, meu_id):
    """Vota 10 (Approved) usando o ID validado pelo sistema"""
    project = os.getenv('PROJECT_NAME')
    repo_id = os.getenv('REPOSITORY_NAME')
    
    reviewer_vote = {
        "vote": 10,
        "id": meu_id
    }

    git_client.create_pull_request_reviewer(
        reviewer_vote, 
        repository_id=repo_id,
        pull_request_id=pr.pull_request_id,
        reviewer_id=meu_id, 
        project=project
    )

# --- 3. FLUXO PRINCIPAL ---
def processar_prs_pendentes():
    try:
        # Criamos a conexão uma vez
        conexao = obter_conexao()
        git_client = conexao.clients.get_git_client()
        
        # 1. Descobrimos quem somos para evitar o erro de "votar por outro"
        meu_id = obter_meu_id(conexao)
        print(f"👤 Autenticado como ID: {meu_id}")

        project = os.getenv('PROJECT_NAME')
        repo_id = os.getenv('REPOSITORY_NAME')

        # 2. Busca PRs
        search_criteria = GitPullRequestSearchCriteria(status='active')
        pull_requests = git_client.get_pull_requests(repo_id, search_criteria, project=project)

        for pr in pull_requests:
            print(f"\n📑 Analisando PR #{pr.pull_request_id}: {pr.title}")
            
            # (Aqui você mantém suas funções de buscar_mudancas_codigo e analisar_pr_com_ai)
            # Simulando aprovação da IA para o teste de voto:
            decisao = "ok" # Substitua pela chamada da sua IA

            if "ok" in decisao:
                print(f"✅ IA aprovou! Votando...")
                aprovar_pull_request(git_client, pr, meu_id)
                print(f"⭐ PR #{pr.pull_request_id} aprovada!")

    except Exception as e:
        print(f"❌ Erro: {e}")
def completar_pull_request(git_client, pr):
    """Realiza o Merge e fecha a PR oficialmente"""
    project = os.getenv('PROJECT_NAME')
    repo_id = os.getenv('REPOSITORY_NAME')

    # Configurações do Merge
    options = GitPullRequestCompletionOptions(
        delete_source_branch=True,          # Deleta a branch após o merge (opcional)
        bypass_policy=False,                # Respeita as políticas da branch
        squash_merge=True,                  # Faz squash para manter o histórico limpo
        transition_work_items=True          # Fecha tasks vinculadas automaticamente
    )

    # Para completar, mudamos o status para 'completed' e passamos o ID do último commit
    pr_update = {
        "status": "completed",
        "lastMergeSourceCommit": pr.last_merge_source_commit,
        "completionOptions": options
    }

    try:
        git_client.update_pull_request(
            pr_update, 
            repository_id=repo_id, 
            pull_request_id=pr.pull_request_id, 
            project=project
        )
        print(f"🏁 PR #{pr.pull_request_id} MERGEADA e FINALIZADA!")
    except Exception as e:
        print(f"⚠️ Erro ao completar PR: {e} (Verifique se há conflitos de código)")


if __name__ == "__main__":
    processar_prs_pendentes()