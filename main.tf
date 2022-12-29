resource "azurerm_resource_group" "this" {
  name     = "${var.prefix}-resource-group"
  location = var.location
}

resource "random_string" "this" {
  length  = 32
  lower   = true
  numeric = true
  special = false
  upper   = true
}

resource "random_password" "this" {
  length           = 32
  lower            = true
  min_lower        = 1
  min_numeric      = 1
  min_special      = 1
  min_upper        = 1
  numeric          = true
  override_special = "_" # Make compatible with bash and PostgreSQL URL
  special          = true
  upper            = true
}

resource "azurerm_postgresql_flexible_server" "this" {
  name                   = "${var.prefix}-postgresql-flexible-server"
  resource_group_name    = azurerm_resource_group.this.name
  location               = azurerm_resource_group.this.location
  administrator_login    = random_string.this.result
  administrator_password = random_password.this.result
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
  version                = "14"
  zone                   = "1"
}

resource "azurerm_postgresql_flexible_server_database" "prod" {
  name      = "prod"
  server_id = azurerm_postgresql_flexible_server.this.id
}

resource "azurerm_postgresql_flexible_server_database" "test" {
  name      = "test"
  server_id = azurerm_postgresql_flexible_server.this.id
}

# Equivalent to "Allow access to Azure services"
resource "azurerm_postgresql_flexible_server_firewall_rule" "this" {
  name             = "${var.prefix}-postgresql-flexible-server-firewall-rule"
  server_id        = azurerm_postgresql_flexible_server.this.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

resource "azurerm_container_registry" "this" {
  name                = replace("${var.prefix}-container-registry", "-", "")
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  sku                 = "Standard"
  admin_enabled       = true
}

resource "azurerm_container_registry_task" "this" {
  name                  = "${var.prefix}-container-registry-task"
  container_registry_id = azurerm_container_registry.this.id

  platform {
    os = "Linux"
  }

  docker_step {
    context_access_token = var.project_repository_token
    context_path         = var.project_repository_url
    dockerfile_path      = "Dockerfile"
    image_names          = ["${azurerm_container_registry.this.login_server}/${var.prefix}:${var.docker_image_tag}"]
  }
}

resource "azurerm_container_registry_task_schedule_run_now" "this" {
  container_registry_task_id = azurerm_container_registry_task.this.id
}

resource "azurerm_container_group" "this" {
  name                = "${var.prefix}-container-instance"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  os_type             = "Linux"
  dns_name_label      = var.prefix
  ip_address_type     = "Public"

  image_registry_credential {
    server   = azurerm_container_registry.this.login_server
    username = azurerm_container_registry.this.admin_username
    password = azurerm_container_registry.this.admin_password
  }

  container {
    name   = var.prefix
    image  = azurerm_container_registry_task.this.docker_step[0].image_names[0]
    cpu    = "1"
    memory = "1"

    ports {
      port     = 80
      protocol = "TCP"
    }

    secure_environment_variables = {
      DATABASE_USERNAME = azurerm_postgresql_flexible_server.this.administrator_login
      DATABASE_PASSWORD = azurerm_postgresql_flexible_server.this.administrator_password
      DATABASE_FQDN     = azurerm_postgresql_flexible_server.this.fqdn
    }
  }
}
