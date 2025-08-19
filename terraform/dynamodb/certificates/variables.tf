# Variáveis para o módulo de certificados

variable "table_name" {
  description = "Nome da tabela de certificados"
  type        = string
}

# Configuração de Baixo Custo - PAY_PER_REQUEST fixo

variable "environment" {
  description = "Ambiente de deploy"
  type        = string
}

variable "project_name" {
  description = "Nome do projeto"
  type        = string
}
