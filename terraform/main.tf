# Configuração principal do Terraform para Certified Builder API PY
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
        version = "~> 6.0"
    }
  }
}

# Configuração do provider AWS
provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "certified-builder-api"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

# Módulo para tabela de Certificados - Configuração de Baixo Custo
module "certificates_table" {
  source = "./dynamodb/certificates"
  
  table_name           = "${var.project_name}-certificates-${var.environment}"
  environment          = var.environment
  project_name         = var.project_name
}

# Módulo para tabela de Pedidos - Configuração de Baixo Custo
module "orders_table" {
  source = "./dynamodb/orders"
  
  table_name           = "${var.project_name}-orders-${var.environment}"
  environment          = var.environment
  project_name         = var.project_name
}

# Módulo para tabela de Participantes - Configuração de Baixo Custo
module "participants_table" {
  source = "./dynamodb/participants"
  
  table_name           = "${var.project_name}-participants-${var.environment}"
  environment          = var.environment
  project_name         = var.project_name
}

# Módulo para tabela de Produtos - Configuração de Baixo Custo
module "products_table" {
  source = "./dynamodb/products"
  
  table_name           = "${var.project_name}-products-${var.environment}"
  environment          = var.environment
  project_name         = var.project_name
}
