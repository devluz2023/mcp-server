# Generate random resource group name
resource "random_pet" "rg_name" {
  prefix = var.resource_group_name_prefix
}

resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = random_pet.rg_name.id
}



resource "azurerm_network_interface" "desafio-osa" {
  name                = "desafio-osa-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name =  azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "desafio-osa-ipconfig"
    subnet_id                     = azurerm_subnet.desafio-osa.id
    public_ip_address_id          = azurerm_public_ip.desafio-osa.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_virtual_network" "desafio-osa" {
  name                = "my-virtual-network"
  address_space       = ["10.0.0.0/16"]
  location            =  azurerm_resource_group.rg.location
  resource_group_name =  azurerm_resource_group.rg.name

}

resource "azurerm_subnet" "desafio-osa" {
  name                 = "desafio-osa-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.desafio-osa.name
  address_prefixes     = ["10.0.1.0/24"]
}


resource "azurerm_public_ip" "desafio-osa" {
  name                = "desafio-osa-started-ip"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Dynamic"
}

resource "azurerm_network_security_group" "desafio-osa" {
  name                = "desafio-osa-get-started-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# Generate random text for a unique storage account name
resource "random_id" "random_id" {
  keepers = {
    # Generate a new ID only when a new resource group is defined
    resource_group = azurerm_resource_group.rg.name
  }

  byte_length = 8
}

# Create storage account for boot diagnostics
resource "azurerm_storage_account" "my_storage_account" {
  name                     = "diag${random_id.random_id.hex}"
  location                 = azurerm_resource_group.rg.location
  resource_group_name      = azurerm_resource_group.rg.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "tls_private_key" "desafio-osa_ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "azurerm_network_security_rule" "ssh" {
  name                        = "allow-ssh"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.rg.name
  network_security_group_name = azurerm_network_security_group.desafio-osa.name
}
  
resource "azurerm_network_security_rule" "security_roles" {
  name                        = "allow-http"
  priority                    = 1010
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "8080"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.rg.name
  network_security_group_name = azurerm_network_security_group.desafio-osa.name
}

resource "azurerm_linux_virtual_machine" "desafio-osa_vm" {
  name                  = "desafio-osa-vm"
  location              = azurerm_resource_group.rg.location
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.desafio-osa.id]
   size               = "Standard_DS1_v2"

   source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  os_disk {
    name              = "desafio-osa-osdisk"
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  computer_name                   = "jenkinvm"
  admin_username                  = "azureuser"
  disable_password_authentication = true

  admin_ssh_key {
    username   = "azureuser"
    public_key = file("chavepublicausopessoal2.pub")
  }

  boot_diagnostics {
    storage_account_uri = azurerm_storage_account.my_storage_account.primary_blob_endpoint
  }

   tags = {
     environment = "staging"
   }
}