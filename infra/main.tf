# # 1. Grupo de Recursos principal (onde o Workspace vive)
# resource "azurerm_resource_group" "bricks_rg" {
#   name     = var.resource_group_name 
#   location = var.location
# }

# # 2. O Workspace Databricks (Refletindo o seu JSON)
# resource "azurerm_databricks_workspace" "this" {
#   name                        = "wk_bricks_pock"
#   resource_group_name         = azurerm_resource_group.bricks_rg.name
#   location                    = "eastus"
#   sku                         = "premium"
  
#   # O seu JSON mostra que o Managed Resource Group chama-se "bricks"
#   managed_resource_group_name = "bricks"

#   custom_parameters {
#     # Refletindo: "enableNoPublicIp": { "value": true }
#     no_public_ip             = true
    
#     # Refletindo: "storageAccountSkuName": { "value": "Standard_ZRS" }
#     storage_account_sku_name = "Standard_ZRS"
    
#     # Nome da conta de storage que já foi criada
#     storage_account_name     = "dbstoragejikkn7d5j7bcg"
#   }

#   tags = {
#     application            = "databricks"
#     databricks-environment = "true"
#   }
# }



# resource "azurerm_kubernetes_cluster" "aks" {
#   name                = "aks-simples-spot"
#   resource_group_name         = azurerm_resource_group.bricks_rg.name
#   location                    =  var.location
#   dns_prefix          = "akspoc"
  
#   # Tier gratuito do plano de controle
#   sku_tier = "Free"

#   default_node_pool {
#     name       = "spotpool"
#     node_count = 1
#     vm_size    = "Standard_B2s" # Econômica
    
#     # Habilitando Instância Spot para reduzir preço em até 90%
#     # priority        = "Spot"
#     # # eviction_policy = "Delete"
#     # spot_max_price  = -1 # Preço de mercado atual
#   }

#   # Identidade simples para o cluster
#   identity {
#     type = "SystemAssigned"
#   }

#   # Desabilita o Log Analytics para economizar custo de ingestão de dados
#   run_command_enabled = true
# }

# output "client_certificate" {
#   value     = azurerm_kubernetes_cluster.aks.kube_config.0.client_certificate
#   sensitive = true
# }

# output "kube_config" {
#   value     = azurerm_kubernetes_cluster.aks.kube_config_raw
#   sensitive = true
# }


# # Azure Container Registry (ACR)
# resource "azurerm_container_registry" "acr" {
#   name                = "registry${replace(var.name, "_", "")}"
#   resource_group_name = azurerm_resource_group.bricks_rg.name
#   location            = azurerm_resource_group.bricks_rg.location
#   sku                 = "Basic"
#   admin_enabled       = true
# }

# # 4. Conexão Direta (Sem índices [0])
# resource "azurerm_role_assignment" "aks_to_acr" {
#   scope                = azurerm_container_registry.acr.id
#   role_definition_name = "AcrPull"
#   principal_id         = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
# }

# # 5. Outputs Simplificados
# output "acr_login_server" {
#   value = azurerm_container_registry.acr.login_server
# }

# # output "kube_config" {
# #   value     = azurerm_kubernetes_cluster.aks.kube_config_raw
# #   sensitive = true
# # }



# # Rede Virtual

