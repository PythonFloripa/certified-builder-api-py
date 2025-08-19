# Módulo para tabela de Pedidos - Configuração de Baixo Custo
# Baseado no modelo: src/domain/entity/order.py

resource "aws_dynamodb_table" "orders" {
  name           = var.table_name
  billing_mode   = "PAY_PER_REQUEST"  # Modo mais econômico - paga apenas pelo que usar
  hash_key       = "order_id"

  # Definição dos atributos baseados no modelo Order
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
    Entity      = "Order"
    CostCenter  = "low-cost"
  }
}
