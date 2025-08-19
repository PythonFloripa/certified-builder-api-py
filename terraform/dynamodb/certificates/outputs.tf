# Outputs para o módulo de certificados

output "table_name" {
  description = "Nome da tabela de certificados"
  value       = aws_dynamodb_table.certificates.name
}

output "table_arn" {
  description = "ARN da tabela de certificados"
  value       = aws_dynamodb_table.certificates.arn
}

output "table_id" {
  description = "ID da tabela de certificados"
  value       = aws_dynamodb_table.certificates.id
}
