# Infraestrutura com Terraform

Este diretório contém a infraestrutura como código (IaC) do projeto, utilizando o [Terraform](https://www.terraform.io/).

## Componentes

- **main.tf**: Arquivo principal com a definição dos recursos.
- **variables.tf**: Declaração de variáveis utilizadas na infraestrutura.
- **proviers.tf**: Configuração dos provedores (ex: Azure, AWS, GCP).
- **azurevm.tf**: Exemplo de provisionamento de máquina virtual na Azure.
- **poc.tfvars**: Valores de variáveis para ambiente de prova de conceito.
- **terraform.tfstate / terraform.tfstate.backup**: Arquivos de estado do Terraform (não editar manualmente).
- **agent.yaml**: Arquivo de configuração adicional (se aplicável).

## Pré-requisitos

- [Terraform instalado](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- Credenciais do provedor configuradas (ex: Azure CLI logado)

## Como subir a infraestrutura

1. Acesse o diretório `infra`:
   ```sh
   cd infra
   ```
2. Inicialize o Terraform:
   ```sh
   terraform init
   ```
3. (Opcional) Visualize o plano de execução:
   ```sh
   terraform plan -var-file=poc.tfvars
   ```
4. Aplique as mudanças para criar/atualizar a infraestrutura:
   ```sh
   terraform apply -var-file=poc.tfvars
   ```
5. Confirme a execução digitando `yes` quando solicitado.

## Observações

- Sempre revise o plano antes de aplicar.
- Os arquivos de estado (`.tfstate`) não devem ser versionados.
- Para destruir a infraestrutura:
  ```sh
  terraform destroy -var-file=poc.tfvars
  ```

---

Dúvidas? Consulte a documentação oficial do Terraform ou o responsável pelo projeto.