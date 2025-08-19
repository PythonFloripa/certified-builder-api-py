# Outputs principais do Terraform

# Informações das tabelas de certificados
output "certificates_table_name" {
  description = "Nome da tabela de certificados"
  value       = module.certificates_table.table_name
}

output "certificates_table_arn" {
  description = "ARN da tabela de certificados"
  value       = module.certificates_table.table_arn
}

# Informações das tabelas de pedidos
output "orders_table_name" {
  description = "Nome da tabela de pedidos"
  value       = module.orders_table.table_name
}

output "orders_table_arn" {
  description = "ARN da tabela de pedidos"
  value       = module.orders_table.table_arn
}

# Informações das tabelas de participantes
output "participants_table_name" {
  description = "Nome da tabela de participantes"
  value       = module.participants_table.table_name
}

output "participants_table_arn" {
  description = "ARN da tabela de participantes"
  value       = module.participants_table.table_arn
}

# Informações das tabelas de produtos
output "products_table_name" {
  description = "Nome da tabela de produtos"
  value       = module.products_table.table_name
}

output "products_table_arn" {
  description = "ARN da tabela de produtos"
  value       = module.products_table.table_arn
}

# Resumo de todas as tabelas
output "all_tables" {
  description = "Resumo de todas as tabelas criadas"
  value = {
    certificates = {
      name = module.certificates_table.table_name
      arn  = module.certificates_table.table_arn
    }
    orders = {
      name = module.orders_table.table_name
      arn  = module.orders_table.table_arn
    }
    participants = {
      name = module.participants_table.table_name
      arn  = module.participants_table.table_arn
    }
    products = {
      name = module.products_table.table_name
      arn  = module.products_table.table_arn
    }
  }
}
