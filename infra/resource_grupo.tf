resource "azurerm_resource_group" "rg_bigdata" {
  name     = var.resource_group_name 
  location = var.location
}