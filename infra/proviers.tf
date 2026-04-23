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
    
    # databricks = {
    #   source = "databricks/databricks"
    # }
  }
}

provider "azurerm" {
  features {}
  # A subscription ID pode ser definida via variável de ambiente ARM_SUBSCRIPTION_ID
  # ou via variável terraform (ver variables.tf)
  subscription_id = var.subscription_id
}