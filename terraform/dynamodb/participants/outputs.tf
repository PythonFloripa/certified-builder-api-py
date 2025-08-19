# Outputs para o módulo de participantes

output "table_name" {
  description = "Nome da tabela de participantes"
  value       = aws_dynamodb_table.participants.name
}

output "table_arn" {
  description = "ARN da tabela de participantes"
  value       = aws_dynamodb_table.participants.arn
}

output "table_id" {
  description = "ID da tabela de participantes"
  value       = aws_dynamodb_table.participants.id
}
