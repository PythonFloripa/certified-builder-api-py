# Outputs para o módulo de produtos

output "table_name" {
  description = "Nome da tabela de produtos"
  value       = aws_dynamodb_table.products.name
}

output "table_arn" {
  description = "ARN da tabela de produtos"
  value       = aws_dynamodb_table.products.arn
}

output "table_id" {
  description = "ID da tabela de produtos"
  value       = aws_dynamodb_table.products.id
}
