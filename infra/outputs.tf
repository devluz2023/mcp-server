# # Para o Cluster All-Purpose
# output "cluster_id" {
#   value       = databricks_cluster.this.id
#   description = "O ID do cluster criado para uso no Python"
# }

# # # Para o SQL Warehouse (ID é o campo 'id' do endpoint)
# # output "warehouse_id" {
# #   value       = databricks_sql_endpoint.this.id
# #   description = "O ID do SQL Warehouse para conexões BI"
# # }