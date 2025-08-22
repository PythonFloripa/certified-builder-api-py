#!/bin/bash

# Script para testar o container Lambda localmente
# O container Lambda expõe a API na porta 9000

echo "🧪 Testando Container Lambda na porta 9000..."
echo "================================================"

# URL base do container Lambda
LAMBDA_URL="http://localhost:9000/2015-03-31/functions/function/invocations"

# Função para criar evento do API Gateway
create_api_gateway_event() {
    local method="$1"
    local path="$2"
    local body="$3"
    
    cat << EOF
{
  "httpMethod": "$method",
  "path": "$path",
  "pathParameters": null,
  "queryStringParameters": null,
  "headers": {
    "Content-Type": "application/json",
    "Accept": "application/json"
  },
  "body": "$body",
  "isBase64Encoded": false,
  "requestContext": {
    "httpMethod": "$method",
    "path": "$path",
    "stage": "test",
    "requestId": "test-request-$(date +%s)",
    "identity": {
      "sourceIp": "127.0.0.1"
    }
  }
}
EOF
}

# Teste do endpoint de criação de certificados
echo "📋 Testando POST /api/v1/certificate/create"
echo "Payload: {\"product_id\": \"316\"}"

# Cria o evento
EVENT=$(create_api_gateway_event "POST" "/api/v1/certificate/create" "{\\\"product_id\\\": \\\"316\\\"}")

# Envia requisição para o container Lambda
echo "🚀 Enviando requisição..."
RESPONSE=$(curl -s -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d "$EVENT")

echo "📥 Resposta recebida:"
echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"

echo ""
echo "================================================"
echo "✅ Teste concluído!"
echo ""
echo "💡 Para executar este teste:"
echo "   1. Execute: docker-compose up certified_build_lambda_function"
echo "   2. Em outro terminal: ./test_lambda_container.sh"
echo ""
echo "📚 Documentação AWS Lambda Powertools:"
echo "   https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/"
