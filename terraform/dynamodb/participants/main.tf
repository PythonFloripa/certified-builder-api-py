# Módulo para tabela de Participantes - Configuração de Baixo Custo
# Baseado no modelo: src/domain/entity/participant.py

resource "aws_dynamodb_table" "participants" {
  name           = var.table_name
  billing_mode   = "PAY_PER_REQUEST"  # Modo mais econômico - paga apenas pelo que usar
  hash_key       = "id"

  # Definição dos atributos baseados no modelo Participant
  attribute {
    name = "id"
    type = "S"  # String para UUID
  }

  # Criptografia básica (sem custo adicional)
  server_side_encryption {
    enabled = true
  }

  # Tags para organização
  tags = {
    Name        = var.table_name
    Environment = var.environment
    Project     = var.project_name
    Entity      = "Participant"
    CostCenter  = "low-cost"
  }
}
