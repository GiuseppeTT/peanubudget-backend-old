output "database_username" {
  value       = data.tfe_outputs.this.values.database_username
  description = "The database's username"
  sensitive   = true
}

output "database_password" {
  value       = data.tfe_outputs.this.values.database_password
  description = "The database's password"
  sensitive   = true
}

output "database_fqdn" {
  value       = data.tfe_outputs.this.values.database_fqdn
  description = "The database's FQND"
  sensitive   = true
}

output "app_fqdn" {
  value       = data.tfe_outputs.this.values.app_fqdn
  description = "The app's FQDN"
  sensitive   = true
}
