output "database_username" {
  value       = azurerm_postgresql_flexible_server.this.administrator_login
  description = "The database's username"
}

output "database_password" {
  value       = azurerm_postgresql_flexible_server.this.administrator_password
  description = "The database's password"
  sensitive   = true
}

output "database_fqdn" {
  value       = azurerm_postgresql_flexible_server.this.fqdn
  description = "The database's FQND"
}

output "app_fqdn" {
  value       = azurerm_container_group.this.fqdn
  description = "The app's FQDN"
}
