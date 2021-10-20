
locals {
  resource_prefix = "cr2460"
  environment = "Tests"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_network_interface" "nic" {
  name                = "${local.resource_prefix}-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "ipconfig001"
    subnet_id                     = azurerm_subnet.snet.id
    private_ip_address_allocation = "Dynamic"
  }
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

resource "azurerm_storage_account" "storacc" {
  name                     = "${local.resource_prefix}tstsa"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "container" {
  name                  = "vhds"
  storage_account_name  = azurerm_storage_account.storacc.name
  container_access_type = "private"
}

resource "azurerm_virtual_machine" "main" {
  name                  = "${local.resource_prefix}-vm"
  location              = azurerm_resource_group.rg.location
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.nic.id]
  vm_size               = "Standard_B2s"

  delete_os_disk_on_termination = true
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
    vhd_uri = "${azurerm_storage_account.storacc.primary_blob_endpoint}${azurerm_storage_container.container.name}/myosdisk1.vhd"
  }
 
  storage_data_disk{
    name = "testdatadisk"
    create_option = "empty"
    lun = 10
    disk_size_gb = 1
    vhd_uri = "${azurerm_storage_account.storacc.primary_blob_endpoint}${azurerm_storage_container.container.name}/testdatadisk.vhd"
  }

  os_profile {
    computer_name  = "hostname"
    admin_username = "testadmin"
    admin_password = "Passw0rd78234!"
  }
  os_profile_windows_config {
  }
}


