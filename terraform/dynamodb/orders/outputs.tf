# Outputs para o módulo de pedidos

output "table_name" {
  description = "Nome da tabela de pedidos"
  value       = aws_dynamodb_table.orders.name
}

output "table_arn" {
  description = "ARN da tabela de pedidos"
  value       = aws_dynamodb_table.orders.arn
}

output "table_id" {
  description = "ID da tabela de pedidos"
  value       = aws_dynamodb_table.orders.id
}
