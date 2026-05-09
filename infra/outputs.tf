# # Para o Cluster All-Purpose
output "cluster_id" {
  value       = databricks_cluster.ml_cluster.id
  description = "O ID do cluster criado para uso no Python"
}

# # # Para o SQL Warehouse (ID é o campo 'id' do endpoint)
# output "warehouse_id" {
#   value       = databricks_sql_endpoint.this.id
#   description = "O ID do SQL Warehouse para conexões BI"
# }

# Output do valor do Token (CUIDADO: Isso aparecerá no console)
output "databricks_token_value" {
  value     = databricks_token.pat_token.token_value
  sensitive = true # Esconde o valor no terminal por segurança
}


output "databricks_host" {
  value       = azurerm_databricks_workspace.this.workspace_url
  description = "A URL do Workspace Databricks para configurar o seu Adapter Python"
}