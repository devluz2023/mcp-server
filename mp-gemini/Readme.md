src/
├── domain/                # Núcleo do sistema (Regras de negócio puras)
│   ├── entities/          # Agentes, Prompts, Conversas (POJOs/Dataclasses)
│   ├── repositories/      # Interfaces (Abstrações para persistência)
│   └── use_cases/         # Lógica de orquestração (ex: ExecutarFluxoAgente)
├── application/           # Camada de aplicação (Orquestradores de fluxo)
│   ├── services/          # Serviços de coordenação de agentes
│   └── ports/             # Definição das interfaces de saída
├── infrastructure/        # Implementações concretas (Camada externa)
│   ├── llm_gateways/      # Wrappers de APIs (OpenAI, Anthropic, LocalLLMs)
│   ├── repositories/      # Implementação de DBs vetoriais (Chroma, Pinecone)
│   └── tools/             # Implementações de ferramentas para agentes
├── interfaces/            # Adaptadores (Camada de entrada)
│   ├── api/               # FastAPI/REST Controllers
│   └── cli/               # Comandos de CLI
└── tests/                 # Testes unitários, comportamentais e Evals
    ├── unit/
    └── integration/