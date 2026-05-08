src/
├── domain/                  # NÚCLEO: O que o sistema é e faz
│   ├── entities/            # Objetos puros: DatabricksJob, Agent, Prompt, DriftResult
│   ├── repositories/        # Interfaces (Contratos): JobRepositoryPort, LLMProviderPort
│   └── use_cases/           # Regras de orquestração: ExecutarFluxoAgente, ValidarDrift
│
├── application/             # CAMADA DE APLICAÇÃO: O maestro do fluxo
│   ├── services/            # Serviços: JobService, DriftAnalysisService, AgentService
│   └── ports/               # Portas (Interfaces): ToolPort, LLMProviderPort
│
├── infrastructure/          # CAMADA EXTERNA: Onde o sistema toca no "mundo real"
│   ├── llm_gateways/        # Wrappers de APIs: OpenAIGateway, AnthropicGateway
│   ├── repositories/        # Implementações reais: DatabricksJobRepository, SQLRepository
│   ├── tools/               # Ferramentas de Agente (concretas):
│   │   ├── drift_tool.py    # Implementação da lógica de drift (scipy/spark)
│   │   ├── job_tool.py      # Execução de jobs no Databricks
│   │   └── registry.py      # Registrador central de ferramentas
│   └── mcp_server/          # Adaptador de entrada: Implementação do FastMCP
│
├── interfaces/              # ADAPTADORES: Como o usuário/sistema entra
│   ├── api/                 # Endpoints FastAPI/REST
│   ├── cli/                 # Comandos CLI
│   └── streamlit_app/       # View (UI) do Streamlit
│       ├── main.py          # Entrypoint da interface
│       └── components/      # Widgets de visualização
│
└── tests/                   # QUALIDADE: Evals e Testes
    ├── unit/                # Testes de Entidades e Services (mocks)
    ├── integration/         # Testes de Gateway e Repositories (reais)
    └── evals/               # Evals de LLM (Golden Datasets para prompts)