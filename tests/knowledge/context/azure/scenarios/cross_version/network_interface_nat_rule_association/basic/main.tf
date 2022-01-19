locals {
  name = "cr3765"
}

resource "azurerm_resource_group" "test" {
  name     = "${local.name}-rg"
  location = "West Europe"
}

resource "azurerm_virtual_network" "test" {
  name                = "${local.name}-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.test.location
  resource_group_name = azurerm_resource_group.test.name
}

resource "azurerm_subnet" "test" {
  name                 = "${local.name}-subnet"
  resource_group_name  = azurerm_resource_group.test.name
  virtual_network_name = azurerm_virtual_network.test.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_public_ip" "test" {
  name                = "${local.name}-publicIP"
  location            = azurerm_resource_group.test.location
  resource_group_name = azurerm_resource_group.test.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_public_ip_prefix" "test" {
  name                = "${local.name}-publicIPPrefix"
  location            = azurerm_resource_group.test.location
  resource_group_name = azurerm_resource_group.test.name
  prefix_length       = 31
}

resource "azurerm_lb" "gateway" {
  name                = "${local.name}-lbGateway"
  location            = azurerm_resource_group.test.location
  resource_group_name = azurerm_resource_group.test.name
  sku                 = "Gateway"

  frontend_ip_configuration {
    name      = "${local.name}-lbGateway-front"
    subnet_id = azurerm_subnet.test.id
  }
}

resource "azurerm_lb" "test3" {
  name                = "${local.name}-lb3"
  resource_group_name = azurerm_resource_group.test.name
  location            = azurerm_resource_group.test.location
  sku                 = "Standard"
  sku_tier            = "Regional"

  frontend_ip_configuration {
    name                                               = "${local.name}-lb-front3"
    gateway_load_balancer_frontend_ip_configuration_id = azurerm_lb.gateway.frontend_ip_configuration.0.id
    public_ip_address_id                               = azurerm_public_ip.test.id
  }

  tags = {
    "environment" = "production"
  }
}

resource "azurerm_lb_nat_rule" "test31" {
  name                           = "${local.name}-natrule1"
  resource_group_name            = azurerm_resource_group.test.name
  loadbalancer_id                = azurerm_lb.test3.id
  frontend_ip_configuration_name = azurerm_lb.test3.frontend_ip_configuration.0.name
  protocol                       = "Tcp"
  frontend_port                  = 3389
  backend_port                   = 3389
  idle_timeout_in_minutes        = 4
  enable_floating_ip             = false
  enable_tcp_reset               = false
}


resource "azurerm_virtual_machine" "main" {
  name                  = "${local.name}-vm"
  location              = azurerm_resource_group.test.location
  resource_group_name   = azurerm_resource_group.test.name
  network_interface_ids = [azurerm_network_interface.nic.id]
  vm_size               = "Standard_B2s"

  delete_os_disk_on_termination    = true
  delete_data_disks_on_termination = true

  storage_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2019-Datacenter"
    version   = "latest"
  }

  storage_os_disk {
    name              = "myosdisk1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }
  os_profile {
    computer_name  = "hostname"
    admin_username = "testadmin"
    admin_password = "Passw0rd78234!"
  }
  os_profile_windows_config {
  }
}

resource "azurerm_network_interface" "nic" {
  name                = "${local.name}-nic"
  location            = azurerm_resource_group.test.location
  resource_group_name = azurerm_resource_group.test.name

  ip_configuration {
    name                          = "ipconfig001"
    subnet_id                     = azurerm_subnet.test.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_network_interface_nat_rule_association" "example" {
  network_interface_id  = azurerm_network_interface.nic.id
  ip_configuration_name = "ipconfig001"
  nat_rule_id           = azurerm_lb_nat_rule.test31.id
}
