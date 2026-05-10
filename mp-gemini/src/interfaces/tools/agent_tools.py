from langchain.tools import tool
from src.application.use_cases.git_automation import GitAutomationUseCase
from src.application.use_cases.job_automation import JobAutomationUseCase

# Dicionário global para armazenar as ferramentas injetadas
_tools_registry = {}


def initialize_tools(git_uc: GitAutomationUseCase, job_uc: JobAutomationUseCase):
    """
    Registra as ferramentas injetando os Use Cases necessários.
    Mantém o padrão original de registro no dicionário global.
    """

    @tool
    def criar_branch_ml(repo_name: str, branch_name: str):
        """Útil para criar uma nova branch de desenvolvimento no Azure DevOps/Git."""
        return git_uc.execute_setup_branch(
            repo_name=repo_name, branch_name=branch_name
        )

    @tool
    def criar_repositorio(repo_name: str):
        """Cria um repositorio."""
        return git_uc.criar_repositorio(repo_name)

    @tool
    def listar_repositorios_azure(dummy_arg: str = ""):
        """Lista todos os repositórios disponíveis no projeto do Azure DevOps."""
        repos = git_uc.list_repositories()
        if not repos:
            return "📂 Nenhum repositório encontrado no projeto."

        lista_formatada = "\n".join([
            f"📁 **Nome:** {r.name} | **ID:** {r.id}"
            for r in repos
        ])
        return f"🚀 **Lista de Repositórios no Azure DevOps:**\n{lista_formatada}"

    @tool
    def listar_jobs_databricks(dummy_arg: str = ""):
        """Lista todos os jobs ativos no Databricks."""
        return job_uc.listar_jobs()

    @tool
    def criar_novo_job(nome: str):
        """Cria um novo job no Databricks."""
        return job_uc.criar_job(nome)

    @tool
    def deletar_job_databricks(job_id: int):
        """Remove um job do Databricks pelo ID."""
        return job_uc.deletar_job(job_id)

    @tool
    def executar_job_agora(job_id: int):
        """Executa um job imediatamente pelo ID."""
        return job_uc.executar_job(job_id)

    @tool
    def listar_modelos_locais(dummy_arg: str = ""):
        """Lista scripts Python na pasta local prontos para deploy."""
        return job_uc.listar_modelos()

    @tool
    def realizar_deploy_modelo(nome_arquivo: str):
        """Faz upload de script e cria Job de deploy no Databricks."""
        return job_uc.deploy_modelo(nome_arquivo)

    @tool
    def deploy_via_yaml(dummy_arg: str = ""):
        """Deploy de jobs usando o arquivo job_model.yaml."""
        return job_uc.bundle_job_yaml()

    @tool
    def analisar_drift_dados(dummy_arg: str = ""):
        """Calcula drift estatístico (KS, PSI) nas tabelas do Lake."""
        return job_uc.show_drift()

    @tool
    def consultar_custo_processamento(run_id: int):
        """Consulta custo via System Tables para um Run ID."""
        return job_uc.calcular_custo(run_id)

    @tool
    def processar_pipeline_feature_store(dummy_arg: str = ""):
        """Executa pipeline: CSV -> Delta -> Feature Store."""
        return job_uc.executar_pipeline_csv_para_feature_store()

    @tool
    def criar_dashboard_monitoramento(dummy_arg: str = ""):
        """Cria dashboard Lakeview para monitorar o agente."""
        return job_uc.criar_dashboard_padrao()

    @tool
    def listar_pull_requests_azure(repo_name: str):
        """Lista todos os Pull Requests ativos em um repositório do Azure DevOps."""
        prs = git_uc.list_prs(repo_name)
        if not prs:
            return f"📂 Nenhum Pull Request ativo encontrado no repositório '{repo_name}'."

        lista_formatada = "\n".join([
            f"🆔 **ID:** {p.id} | **Título:** {p.title} | **Status:** {p.status} | **De:** {p.source_branch} **Para:** {p.target_branch}"
            for p in prs
        ])
        return f"🚀 **Pull Requests Ativos em '{repo_name}':**\n{lista_formatada}"

    @tool
    def aprovar_e_mergear_pr(repo_name: str, pr_id: int):
        """Aprova e faz o merge de um Pull Request no Azure DevOps."""
        success = git_uc.execute_approve_and_merge(repo_name, pr_id)
        if success:
            return f"✅ PR {pr_id} aprovado e mergeado com sucesso no repositório '{repo_name}'."
        else:
            return f"❌ Falha ao aprovar ou mergear o PR {pr_id} no repositório '{repo_name}'."

    # --- Registro no Dicionário (Mantendo o padrão que funcionava) ---
    _tools_registry["criar_branch_ml"] = criar_branch_ml
    _tools_registry["listar_repositorios_azure"] = listar_repositorios_azure
    _tools_registry["listar_pull_requests_azure"] = listar_pull_requests_azure
    _tools_registry["aprovar_e_mergear_pr"] = aprovar_e_mergear_pr
    _tools_registry["listar_jobs_databricks"] = listar_jobs_databricks
    _tools_registry["criar_novo_job"] = criar_novo_job
    _tools_registry["deletar_job_databricks"] = deletar_job_databricks
    _tools_registry["executar_job_agora"] = executar_job_agora
    _tools_registry["listar_modelos_locais"] = listar_modelos_locais
    _tools_registry["realizar_deploy_modelo"] = realizar_deploy_modelo
    _tools_registry["deploy_via_yaml"] = deploy_via_yaml
    _tools_registry["analisar_drift_dados"] = analisar_drift_dados
    _tools_registry["consultar_custo_processamento"] = consultar_custo_processamento
    _tools_registry["processar_pipeline_feature_store"] = (
        processar_pipeline_feature_store
    )
    _tools_registry["criar_dashboard_monitoramento"] = criar_dashboard_monitoramento
    _tools_registry["criar_repositorio"] = criar_repositorio


def get_tools():
    """Retorna o dicionário para que o AgentService use .values() corretamente."""
    return _tools_registry
