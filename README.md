# Certified Builder API

## Descrição

Esta API é responsável por gerenciar a criação, consulta e download de certificados. Ela é construída como uma função Lambda da AWS, utilizando uma arquitetura serverless.

## Tecnologias Utilizadas

- **Python 3.12**
- **AWS Lambda**
- **API Gateway**
- **Boto3**: AWS SDK para Python.
- **Pydantic**: Para validação de dados.
- **Docker**: Para containerização da aplicação.

## Endpoints

A seguir estão os endpoints disponíveis na API.

### Criar Certificado

Cria um novo certificado para um determinado produto.

- **Endpoint:** `POST /v1/certificate/create`
- **Entrada (body):**
  ```json
  {
    "product_id": "string"
  }
  ```
- **Saída (sucesso):**
  ```json
  {
    "certificate_quantity": "integer",
    "existing_orders": ["integer"],
    "new_orders": ["integer"],
    "processing_date": "string"
  }
  ```
- **Saída (erro):**
  ```json
  {
    "status": "integer",
    "message": "string",
    "details": "string"
  }
  ```

### Consultar Certificado

Consulta certificados com base em diferentes critérios.

- **Endpoint:** `GET /v1/certificate/fetch`
- **Entrada (query parameters):**
  - `order_id` (opcional): ID do pedido.
  - `email` (opcional): Email do participante.
  - `product_id` (opcional): ID do produto.
- **Saída (sucesso):**
  ```json
  [
    {
      "id": "string (uuid)",
      "order_id": "integer",
      "product_id": "integer",
      "participant_name": "string",
      "participant_email": "string",
      "participant_document": "string",
      "certificate_url": "string",
      "created_at": "string",
      "updated_at": "string",
      "success": "boolean",
      "email": "string",
      "product_name": "string",
      "generated_date": "string",
      "time_checkin": "string"
    }
  ]
  ```
- **Saída (erro):**
  ```json
  {
    "status": "integer",
    "message": "string",
    "details": "string"
  }
  ```

### Download do Certificado

Gera uma página para download de um certificado.

- **Endpoint:** `GET /v1/certificate/download`
- **Entrada (query parameters):**
  - `id` (obrigatório): UUID do certificado.
- **Saída (sucesso):**
  - Retorna uma página HTML com o link para download do certificado.
- **Saída (erro):**
  - Retorna uma página HTML indicando o erro (certificado não encontrado, UUID inválido, etc.).