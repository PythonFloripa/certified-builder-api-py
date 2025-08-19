# Variáveis para configuração do Terraform

# Região AWS onde os recursos serão criados
variable "aws_region" {
  description = "Região AWS para deploy dos recursos"
  type        = string
  default     = "us-east-1"
}

# Ambiente de deploy (dev, staging, prod)
variable "environment" {
  description = "Ambiente de deploy"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "O ambiente deve ser: dev, staging ou prod."
  }
}

# Nome do projeto
variable "project_name" {
  description = "Nome do projeto"
  type        = string
  default     = "certified-builder-api"
}

# Configuração do DynamoDB - Modo de Baixo Custo
# Todas as tabelas usam PAY_PER_REQUEST por padrão (paga apenas pelo que usar)
