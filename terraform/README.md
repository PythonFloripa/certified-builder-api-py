# Infraestrutura Terraform - Certified Builder API PY

Este diretório contém a configuração do Terraform para criar as tabelas do DynamoDB baseadas nos modelos das entidades do projeto, **otimizada para custo mínimo**.

## Estrutura do Projeto

```
terraform/
├── main.tf                    # Arquivo principal com módulos
├── variables.tf               # Definição de variáveis
├── outputs.tf                 # Outputs das tabelas criadas
├── terraform.tfvars.example   # Exemplo de configuração
├── README.md                  # Esta documentação
└── dynamodb/                  # Módulos das tabelas
    ├── certificates/          # Tabela de certificados
    ├── orders/               # Tabela de pedidos
    ├── participants/         # Tabela de participantes
    └── products/            # Tabela de produtos
```

## Tabelas Criadas

### 1. Certificates (Certificados)
- **Chave Primária**: `id` (UUID) + `order_id` (Number)
- **Modo de Cobrança**: PAY_PER_REQUEST (paga apenas pelo que usar)
- **Índices**: Apenas chave primária (sem índices secundários para economizar)

### 2. Orders (Pedidos)
- **Chave Primária**: `order_id` (Number)
- **Modo de Cobrança**: PAY_PER_REQUEST (paga apenas pelo que usar)
- **Índices**: Apenas chave primária (sem índices secundários para economizar)

### 3. Participants (Participantes)
- **Chave Primária**: `id` (UUID)
- **Modo de Cobrança**: PAY_PER_REQUEST (paga apenas pelo que usar)
- **Índices**: Apenas chave primária (sem índices secundários para economizar)

### 4. Products (Produtos)
- **Chave Primária**: `product_id` (Number)
- **Modo de Cobrança**: PAY_PER_REQUEST (paga apenas pelo que usar)
- **Índices**: Apenas chave primária (sem índices secundários para economizar)

## Como Usar

### 1. Configuração Inicial

```bash
# Copie o arquivo de exemplo
cp terraform.tfvars.example terraform.tfvars

# Edite as variáveis conforme necessário
nano terraform.tfvars
```

### 2. Inicialização do Terraform

```bash
# Inicialize o Terraform
terraform init

# Verifique o plano de execução
terraform plan
```

### 3. Aplicação da Infraestrutura

```bash
# Aplique as configurações
terraform apply

# Confirme digitando 'yes' quando solicitado
```

### 4. Verificação dos Recursos

```bash
# Veja os outputs das tabelas criadas
terraform output

# Veja o estado atual
terraform show
```

## Configurações Disponíveis

### Variáveis de Ambiente
- `aws_region`: Região AWS (padrão: us-east-1)
- `environment`: Ambiente (dev, staging, prod)
- `project_name`: Nome do projeto

### Configurações do DynamoDB (Baixo Custo)
- **Modo de Cobrança**: PAY_PER_REQUEST (fixo - paga apenas pelo que usar)
- **Sem configurações de capacidade** (não necessário no modo PAY_PER_REQUEST)

## Recursos Criados (Otimizados para Baixo Custo)

Cada tabela inclui:
- ✅ Criptografia básica no servidor (sem custo adicional)
- ✅ Modo PAY_PER_REQUEST (custo mínimo)
- ✅ Tags para organização


## Limpeza

Para remover todos os recursos criados:

```bash
terraform destroy
```

## Mapeamento com Entidades

As tabelas foram criadas seguindo exatamente os modelos das entidades:

- `src/domain/entity/certificate.py` → `certificates`
- `src/domain/entity/order.py` → `orders`
- `src/domain/entity/participant.py` → `participants`
- `src/domain/entity/product.py` → `products`
