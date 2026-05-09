import os

from azure.devops.connection import Connection
from azure.devops.exceptions import AzureDevOpsServiceError
from azure.devops.v7_1.git.models import GitPullRequestSearchCriteria
from dotenv import load_dotenv  # Adicione esta linha
from msrest.authentication import BasicAuthentication

# --- CONFIGURAÇÕES ---
# ⚠️ Lembre-se de rotacionar seu PAT após os testes por segurança.
load_dotenv()

PERSONAL_ACCESS_TOKEN = os.getenv("PERSONAL_ACCESS_TOKEN")
ORGANIZATION_URL = os.getenv("ORGANIZATION_URL")
PROJECT_NAME = os.getenv("PROJECT_NAME")
REPOSITORY_NAME = os.getenv("REPOSITORY_NAME")
BRANCH_NAME = os.getenv("BRANCH_NAME")


def obter_git_client():
    """Helper para centralizar a conexão"""
    credentials = BasicAuthentication("", PERSONAL_ACCESS_TOKEN)
    connection = Connection(base_url=ORGANIZATION_URL, creds=credentials)
    return connection.clients.get_git_client()


def garantir_repositorio(git_client):
    """Função 1: Garante que o repositório existe (Cria se necessário)"""
    try:
        repo = git_client.get_repository(
            repository_id=REPOSITORY_NAME, project=PROJECT_NAME
        )
        print(f"✅ Repositório encontrado: {repo.name}")
        return repo
    except AzureDevOpsServiceError:
        print(f"ℹ️ Repositório '{REPOSITORY_NAME}' não encontrado. Criando...")
        repo_to_create = {"name": REPOSITORY_NAME}
        repo = git_client.create_repository(repo_to_create, project=PROJECT_NAME)
        print(f"✅ Repositório criado com sucesso: {repo.name}")
        return repo


def versionar_arquivo_local(git_client, repo):
    """Função 2: Lê o arquivo readme_Teste.py e faz o commit"""
    nome_arquivo_local = "readme_Teste.py"

    if not os.path.exists(nome_arquivo_local):
        print(f"❌ Erro: O arquivo '{nome_arquivo_local}' não foi encontrado na raiz.")
        return

    # Lendo o conteúdo do arquivo físico
    with open(nome_arquivo_local, "r", encoding="utf-8") as f:
        conteudo = f.read()

    # Obtendo o ID do último commit para evitar conflito de histórico
    old_object_id = "0000000000000000000000000000000000000000"
    try:
        refs = git_client.get_refs(
            repository_id=repo.id, project=PROJECT_NAME, filter="heads/main"
        )
        if refs:
            old_object_id = refs[0].object_id
    except Exception:
        pass

    # Verificando se o arquivo já existe no repo para decidir entre 'add' ou 'edit'
    # Por segurança, vamos usar 'add' para a primeira vez.
    # Se rodar denovo e o arquivo já estiver lá, use 'edit'.
    push = {
        "commits": [
            {
                "comment": f"Upload de {nome_arquivo_local} via SDK",
                "changes": [
                    {
                        "changeType": "add",
                        "item": {"path": f"/{nome_arquivo_local}"},
                        "newContent": {"content": conteudo, "contentType": "rawText"},
                    }
                ],
            }
        ],
        "refUpdates": [{"name": BRANCH_NAME, "oldObjectId": old_object_id}],
    }

    try:
        git_client.create_push(push, repository_id=repo.id, project=PROJECT_NAME)
        print(f"🚀 Sucesso! Arquivo '{nome_arquivo_local}' versionado.")
    except Exception as e:
        print(f"⚠️ Falha no push (pode ser que o arquivo já exista): {e}")


def criar_gitflow_branches(git_client, repo):
    """Função 3: Cria as branches de dev, qas e prod a partir da main"""
    # Lista das branches que queremos criar
    branches_para_criar = ["dev", "qas", "prod"]

    try:
        # 1. Obter o ID do último commit da branch main (base para as novas branches)
        refs = git_client.get_refs(
            repository_id=repo.id, project=PROJECT_NAME, filter="heads/main"
        )
        if not refs:
            print("❌ Erro: Branch 'main' não encontrada para servir de base.")
            return

        main_sha = refs[0].object_id
        print(f"ℹ️ Base para GitFlow (main SHA): {main_sha}")

        # 2. Criar cada branch
        for branch_name in branches_para_criar:
            full_branch_path = f"refs/heads/{branch_name}"

            # Estrutura para criar uma nova referência (branch)
            ref_update = [
                {
                    "name": full_branch_path,
                    "oldObjectId": "0000000000000000000000000000000000000000",  # Indica nova branch
                    "newObjectId": main_sha,
                }
            ]

            try:
                git_client.update_refs(
                    ref_update, repository_id=repo.id, project=PROJECT_NAME
                )
                print(f"✅ Branch criada: {branch_name}")
            except AzureDevOpsServiceError as e:
                # Caso a branch já exista, ele retornará um erro
                if "already exists" in str(e) or "RefUpdateStatus.Exists" in str(e):
                    print(f"ℹ️ Branch '{branch_name}' já existe. Pulando...")
                else:
                    print(f"⚠️ Erro ao criar branch {branch_name}: {e}")

    except Exception as e:
        print(f"❌ Erro ao processar GitFlow: {e}")


def listar_pull_requests(git_client, repo):
    """Função 4: Lista todos os Pull Requests ativos no repositório"""
    print(f"\n🔍 Buscando Pull Requests em: {repo.name}...")

    try:
        # Definimos o critério de busca (por padrão, busca PRs ativos/abertos)
        search_criteria = GitPullRequestSearchCriteria(
            status="active"  # Pode ser 'active', 'completed', 'abandoned' ou 'all'
        )

        pull_requests = git_client.get_pull_requests(
            repository_id=repo.id, search_criteria=search_criteria, project=PROJECT_NAME
        )

        if not pull_requests:
            print("ℹ️ Nenhum Pull Request ativo encontrado.")
            return

        print(f"✅ Encontrados {len(pull_requests)} PR(s):")
        for pr in pull_requests:
            print("---")
            print(f"ID: {pr.pull_request_id}")
            print(f"Título: {pr.title}")
            print(f"Criado por: {pr.created_by.display_name}")
            print(f"De: {pr.source_ref_name} -> Para: {pr.target_ref_name}")
            print(f"Status: {pr.status}")

    except Exception as e:
        print(f"❌ Erro ao listar Pull Requests: {e}")


# --- BLOCO PRINCIPAL ATUALIZADO ---
if __name__ == "__main__":
    client = obter_git_client()

    # 1. Garante a infraestrutura (Repositório)
    repositorio = garantir_repositorio(client)

    if repositorio:
        # 2. Garante a estratégia de branches (GitFlow)
        criar_gitflow_branches(client, repositorio)

        # 3. Sobe o arquivo local (readme_Teste.py)
        versionar_arquivo_local(client, repositorio)

        # 4. Lista os PRs existentes
        listar_pull_requests(client, repositorio)
