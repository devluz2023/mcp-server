

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




resource "databricks_cluster" "ml_cluster" {
  cluster_name            = "FABIO DA LUZ's Cluster 2026-05-09"
  spark_version           = "18.2.x-cpu-ml-scala2.13" # Usando a versão ML efetiva do seu JSON
  node_type_id            = "Standard_DS3_v2"
  autotermination_minutes = 4320 # Cuidado: isso são 3 dias ligado! 
  
  # Configuração de Single Node (conforme seu spark_conf)
  spark_conf = {
    "spark.databricks.cluster.profile" : "singleNode"
    "spark.master"                     : "local[*, 4]"
  }

  custom_tags = {
    "ResourceClass" = "SingleNode"
  }

  # Azure specific (ON_DEMAND conforme seu JSON)
  azure_attributes {
    availability       = "ON_DEMAND_AZURE"
    first_on_demand    = 1
    spot_bid_max_price = -1
  }

  # Segurança e Usuário Único
  data_security_mode = "SINGLE_USER"
  single_user_name   = "fabio.jdluz@gmail.com"
}
