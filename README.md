# MCP Server

## Visão geral

Este repositório contém uma solução de monitoramento e análise para um pipeline de SKU Analytics com dois serviços principais:

- `server1`: serviço de monitoramento, análise de logs e alertas.
- `server2`: serviço de logística/analytics com interface de controle e execução de testes.

A aplicação é composta por três serviços Docker orquestrados no `docker-compose.yaml`.

## Estrutura do projeto

- `docker-compose.yaml`: define os serviços Docker.
- `server1/`
  - `app.py`: aplicação principal em Streamlit para interface de controle e análise.
  - `monitor_server.py`: servidor MCP que expõe ferramentas para buscar logs e executar testes.
  - `alert_worker.py`: monitor de contêiner que envia alertas quando o serviço cai.
  - `rag_engine.py`: motor de análise de logs usando embeddings para diagnóstico de problemas.
  - `requirements.txt`: dependências do serviço de monitoramento.
- `server2/`
  - `src/main.py`: implementação do pipeline/logística e controle via Streamlit.
  - `tests/`: testes unitários para a aplicação.
  - `requirements.txt`: dependências do serviço de analytics.
- `requirements.txt`: dependências protótipo do repositório.

## Componentes principais

### server1

Este serviço inclui:

- uma interface Streamlit para análise de status de containers e execução de ações;
- um servidor MCP (`monitor_server.py`) que fornece ferramentas de diagnóstico;
- um worker de monitoramento (`alert_worker.py`) que verifica o estado do container `logistica-sku-analytics` e gera alertas.

### server2

Este serviço representa o pipeline de SKU Analytics e contém:

- `src/main.py`: interface de entrada para o container alvo e invocação de diagnóstico e testes;
- `tests/`: conjunto de testes unitários rodados pelo serviço de monitoramento.

## Dependências

As dependências usadas incluem:

- `mcp`
- `streamlit`
- `sentence-transformers`
- `docker`
- `numpy`
- `torchvision`
- `pytest`

## Como executar

1. Certifique-se de ter Docker instalado e rodando.
2. No diretório raiz do projeto, execute:

```bash
docker compose up --build
```

3. Acesse a interface de monitoramento em:

- `http://localhost:8501`

4. O serviço `logistica-sku-analytics` está configurado para ser exposto como `8502:8501`.

## Uso

- O serviço Streamlit principal exibe o status do container `logistica-sku-analytics`.
- Você pode acionar a análise de logs e receber um diagnóstico automático via `rag_engine.py`.
- Também é possível executar testes unitários do serviço de análise usando o botão correspondente.

## Observações

- `server1/monitor_server.py` utiliza `docker` para inspecionar containers e `pytest` para executar testes.
- `server1/rag_engine.py` realiza uma análise simples de similaridade de logs usando embeddings.
- `server1/alert_worker.py` envia alertas via console e pode ser adaptado para webhooks externos.

## Melhorias futuras

- adicionar documentação de endpoints e APIs internas;
- implementar alertas em Slack/Teams/Discord via webhook;
- expandir a base de conhecimento em `rag_engine.py` para diagnósticos mais precisos;
- melhorar a execução de `server2/src/main.py` para rodar Streamlit corretamente em container.




melhorar rag
testes unitarios nos agentes
arquietura limpa
codigo limpo
pool de llm
gerenciamento de concorrencia
gerenciamento de custo
