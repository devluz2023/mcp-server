# providers.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }

    azuredevops = {
      source  = "microsoft/azuredevops"
      version = ">= 0.10.0" 
    }

      random = {
        source  = "hashicorp/random"
        version = "~>3.0"
      }
    
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.0" 
    }
  }
}

provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
}

provider "databricks" {

  host = azurerm_databricks_workspace.this.workspace_url
  

}