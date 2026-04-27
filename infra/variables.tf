variable "resource_group_name" {
  type = string
}

variable "subscription_id" {
  type        = string
  description = "Azure Subscription ID"
  default     = ""  # Defina via variável de ambiente ARM_SUBSCRIPTION_ID ou no arquivo .tfvars
}

variable "location" {
  type = string
}

variable "name" {
  type = string
}


variable "deploy_aks" {
  type    = bool
  default = false
}

variable "deploy_databricks" {
  type    = bool
  default = false
}

variable "deploy_acr" {
  type    = bool
  default = false
}

variable "azdo_pat" {
  type      = string
  sensitive = true
}

variable "azdo_org_url" {
  type = string
}

variable "ssh_public_key" {
  default = "id_rsa.pub"
}
variable "resource_group_location" {
 default     = "eastus"
  description = "Location of the resource group."
}

variable "resource_group_name_prefix" {
  default     = "rg"
  description = "Prefix of the resource group name that's combined with a random ID so name is unique in your Azure subscription."
}