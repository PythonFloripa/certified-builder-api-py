# Otimização de Custos - DynamoDB

Este documento explica as estratégias de economia de custos implementadas nas tabelas do DynamoDB.

## Estratégias de Economia Implementadas

### ✅ **1. Modo PAY_PER_REQUEST**
- **Configuração**: Todas as tabelas usam `PAY_PER_REQUEST`
- **Benefício**: Paga apenas pelo que usar, sem custos fixos
- **Economia**: Ideal para desenvolvimento e cargas variáveis

### ✅ **2. Remoção de Índices Secundários Globais (GSI)**
- **Antes**: 3-4 GSI por tabela
- **Agora**: Apenas chave primária
- **Economia**: ~$0.25 por GB/mês por índice removido
- **Impacto**: Consultas limitadas à chave primária

### ✅ **3. Desabilitação do Point-in-Time Recovery**
- **Antes**: Backup automático habilitado
- **Agora**: Backup desabilitado
- **Economia**: ~$0.20 por GB/mês
- **Alternativa**: Backups manuais quando necessário

### ✅ **4. Criptografia Básica**
- **Configuração**: Criptografia no servidor habilitada
- **Custo**: **ZERO** - sem custo adicional
- **Benefício**: Segurança mantida

## Custos Estimados por Tabela

### Cenário de Baixo Uso (Desenvolvimento)
- **Armazenamento**: 1 GB = ~$0.25/mês
- **Operações**: 10.000 operações/mês = ~$0.01/mês
- **Total por tabela**: ~$0.26/mês
- **Total para 4 tabelas**: ~$1.04/mês

### Cenário de Uso Moderado
- **Armazenamento**: 10 GB = ~$2.50/mês
- **Operações**: 100.000 operações/mês = ~$0.13/mês
- **Total por tabela**: ~$2.63/mês
- **Total para 4 tabelas**: ~$10.52/mês

## Comparação de Custos

| Recurso | Configuração Anterior | Configuração Atual | Economia |
|---------|----------------------|-------------------|----------|
| Modo de Cobrança | PROVISIONED (5 RCU/WCU) | PAY_PER_REQUEST | ~$25/mês |
| Índices GSI | 3-4 por tabela | 0 por tabela | ~$3-4/mês por tabela |
| Point-in-Time Recovery | Habilitado | Desabilitado | ~$0.20/GB/mês |
| **Total Economia** | | | **~$40-50/mês** |

## Limitações da Configuração de Baixo Custo

### ❌ **Consultas Limitadas**
- Apenas consultas pela chave primária
- Não é possível consultar por email, CPF, etc.
- Solução: Implementar consultas no código da aplicação

### ❌ **Sem Backup Automático**
- Sem point-in-time recovery
- Solução: Backups manuais periódicos

### ❌ **Sem Replicação Global**
- Tabelas apenas na região configurada
- Solução: Implementar replicação manual se necessário

## Recomendações para Produção

### Para Cargas Baixas (< 1M operações/mês)
- ✅ Manter configuração atual
- ✅ Monitorar custos mensalmente

### Para Cargas Médias (1M-10M operações/mês)
- ✅ Considerar adicionar GSI específicos conforme necessidade
- ✅ Avaliar habilitar point-in-time recovery

### Para Cargas Altas (> 10M operações/mês)
- ⚠️ Considerar modo PROVISIONED
- ⚠️ Implementar DAX para cache
- ⚠️ Adicionar GSI para consultas frequentes

## Monitoramento de Custos

### CloudWatch Metrics
```bash
# Monitorar operações de leitura/escrita
aws cloudwatch get-metric-statistics \
  --namespace AWS/DynamoDB \
  --metric-name ConsumedReadCapacityUnits \
  --dimensions Name=TableName,Value=certified-builder-api-certificates-dev

# Monitorar armazenamento
aws cloudwatch get-metric-statistics \
  --namespace AWS/DynamoDB \
  --metric-name TableSizeBytes \
  --dimensions Name=TableName,Value=certified-builder-api-certificates-dev
```

### AWS Cost Explorer
- Configure alertas de custo
- Monitore gastos por serviço
- Analise tendências de uso

## Comandos Úteis

### Verificar Custos Atuais
```bash
# Listar tabelas e suas configurações
aws dynamodb list-tables

# Descrever tabela específica
aws dynamodb describe-table --table-name certified-builder-api-certificates-dev
```

### Backup Manual (quando necessário)
```bash
# Criar backup sob demanda
aws dynamodb create-backup \
  --table-name certified-builder-api-certificates-dev \
  --backup-name backup-$(date +%Y%m%d)
```

## Conclusão

Esta configuração de baixo custo é ideal para:
- ✅ Desenvolvimento e testes
- ✅ Projetos com orçamento limitado
- ✅ Cargas de trabalho variáveis
- ✅ MVP e protótipos

Para produção com cargas previsíveis e altas, considere ajustar as configurações conforme as recomendações acima.
