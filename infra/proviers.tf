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
  # Como você já deu o 'az account set', ele usará a assinatura 558cda1e...
  subscription_id = "558cda1e-9cc5-47b8-ac22-5f3dcc47d1d7"
}