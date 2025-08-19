# Módulo para tabela de Certificados - Configuração de Baixo Custo
# Baseado no modelo: src/domain/entity/certificate.py

resource "aws_dynamodb_table" "certificates" {
  name           = var.table_name
  billing_mode   = "PAY_PER_REQUEST"  # Modo mais econômico - paga apenas pelo que usar
  hash_key       = "id"
  range_key      = "order_id"

  # Definição dos atributos baseados no modelo Certificate
  attribute {
    name = "id"
    type = "S"  # String para UUID
  }
  
  attribute {
    name = "order_id"
    type = "N"  # Number para order_id
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
    Entity      = "Certificate"
    CostCenter  = "low-cost"
  }
}
