

# 2. O Workspace Databricks (Refletindo o seu JSON)
resource "azurerm_databricks_workspace" "this" {
  name                        = "wk_bricks_pock"
  resource_group_name         = azurerm_resource_group.rg_bigdata.name
  location                    = var.location
  sku                         = "premium"
  
  # O seu JSON mostra que o Managed Resource Group chama-se "bricks"
  managed_resource_group_name = "bricks"

  custom_parameters {
    # Refletindo: "enableNoPublicIp": { "value": true }
    no_public_ip             = true
    
    # Refletindo: "storageAccountSkuName": { "value": "Standard_ZRS" }
    storage_account_sku_name = "Standard_ZRS"
    
    # Nome da conta de storage que já foi criada
    storage_account_name     = "dbstoragejikkn7d5j7bcg"
  }

  tags = {
    application            = "databricks"
    databricks-environment = "true"
  }
}


