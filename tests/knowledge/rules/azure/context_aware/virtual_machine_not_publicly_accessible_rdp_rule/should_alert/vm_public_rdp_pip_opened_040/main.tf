# using Application security group as a destination

provider "azurerm" {
  features {}
}

locals {
  resource_prefix = "cr24600"
  environment = "Tests"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "${local.resource_prefix}-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_subnet" "snet" {
  name                 = "${local.resource_prefix}-snet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.23.0/24"]
}

resource "azurerm_network_security_group" "snetnsg" {
  name                = "${local.resource_prefix}-snetnsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_network_security_rule" "snetnsgrule" {
  name                       = "${local.resource_prefix}-rule401"
  priority                   = 401
  direction                  = "Inbound"
  access                     = "Allow"
  protocol                   = "Tcp"
  source_port_range          = "*"
  destination_port_range     = "*"
  source_address_prefix      = "*"
  destination_address_prefix = "*"
  resource_group_name         = azurerm_resource_group.rg.name
  network_security_group_name = azurerm_network_security_group.snetnsg.name
}

resource "azurerm_subnet_network_security_group_association" "associate" {
  subnet_id                 = azurerm_subnet.snet.id
  network_security_group_id = azurerm_network_security_group.snetnsg.id
}

resource "azurerm_public_ip" "pip" {
  name                = "${local.resource_prefix}-pip"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  allocation_method   = "Dynamic"
}

resource "azurerm_application_security_group" "asg" {
  name                = "${local.resource_prefix}asg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_network_interface" "nic" {
  name                = "${local.resource_prefix}-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "ipconfig001"
    subnet_id                     = azurerm_subnet.snet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id = azurerm_public_ip.pip.id
  }
}

//https://github.com/terraform-providers/terraform-provider-azurerm/issues/5591

resource "azurerm_network_interface_application_security_group_association" "associate" {
  network_interface_id          = azurerm_network_interface.nic.id
  application_security_group_id = azurerm_application_security_group.asg.id

  depends_on = [azurerm_network_interface.nic]
}

resource "azurerm_network_security_group" "nicnsg" {
  name                = "${local.resource_prefix}-nicnsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_network_security_rule" "nicnsgrule" {
  name                       = "${local.resource_prefix}-rule201"
  priority                   = 201
  direction                  = "Inbound"
  access                     = "Allow"
  protocol                   = "Tcp"
  source_port_range          = "*"
  destination_port_range     = "*"
  source_address_prefix      = "*"
  destination_application_security_group_ids = [azurerm_application_security_group.asg.id]
  resource_group_name         = azurerm_resource_group.rg.name
  network_security_group_name = azurerm_network_security_group.nicnsg.name
}

resource "azurerm_network_interface_security_group_association" "associate" {
  network_interface_id      = azurerm_network_interface.nic.id
  network_security_group_id = azurerm_network_security_group.nicnsg.id
}

resource "azurerm_windows_virtual_machine" "main" {
  name                  = "${local.resource_prefix}-vm"
  location              = azurerm_resource_group.rg.location
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.nic.id]
  size                  = "Standard_B2s"
  admin_username      = "adminuser"
  admin_password      = "P@$$w0rd1234!"

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2019-Datacenter"
    version   = "latest"
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

}
