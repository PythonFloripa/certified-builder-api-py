# Certified Builder API

## Descrição

Esta API é responsável por gerenciar a criação, consulta e download de certificados. Ela é construída como uma função Lambda da AWS, utilizando uma arquitetura serverless.

## Tecnologias Utilizadas

- **Python 3.13**
- **AWS Lambda**
- **API Gateway**
- **Boto3**: AWS SDK para Python.
- **Pydantic**: Para validação de dados.
- **Docker**: Para containerização da aplicação.

## Desenvolvimento e Deploy

- **Local**: `docker compose up --build` expõe a Lambda em `http://localhost:9000`.
- **Smoke test**: `python test_local.py` ou `bash test_lambda_container.sh`.
- **Deploy**: o workflow `.github/workflows/workflow_build.yaml` gera um ZIP e atualiza a função `tech-floripa-certificates-api-dev` com `aws lambda update-function-code`.

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

### Criar Certificados em Lote

Cria múltiplos certificados a partir de uma lista de dados recebida diretamente.

- **Endpoint:** `POST /v1/certificate/create-batch`
- **Entrada (body):**
  ```json
  {
    "certificates": [
      {
        "order_id": 1234,
        "first_name": "João",
        "last_name": "Silva",
        "email": "joao.silva@example.com",
        "phone": "(48) 99999-9999",
        "cpf": "123.456.789-00",
        "city": "Florianópolis",
        "product_id": 5678,
        "product_name": "Workshop de Python Avançado",
        "certificate_details": "In recognition of their participation in the Workshop de Python Avançado, held on January 15, 2025, at IFSC – Câmpus Florianópolis, Brazil, with a total duration of 8 hours.",
        "certificate_logo": "https://example.com/logo.png",
        "certificate_background": "https://example.com/background.png",
        "order_date": "2025-01-10 14:30:00",
        "checkin_latitude": "-27.5667",
        "checkin_longitude": "-48.5156",
        "time_checkin": "2025-01-15 09:00:00"
      },
      {
        "order_id": 1235,
        "first_name": "Maria",
        "last_name": "Santos",
        "email": "maria.santos@example.com",
        "phone": "(48) 88888-8888",
        "cpf": "987.654.321-00",
        "city": "São José",
        "product_id": 5678,
        "product_name": "Workshop de Python Avançado",
        "certificate_details": "In recognition of their participation in the Workshop de Python Avançado, held on January 15, 2025, at IFSC – Câmpus Florianópolis, Brazil, with a total duration of 8 hours.",
        "certificate_logo": "https://example.com/logo.png",
        "certificate_background": "https://example.com/background.png",
        "order_date": "2025-01-10 14:35:00",
        "checkin_latitude": "-27.5667",
        "checkin_longitude": "-48.5156",
        "time_checkin": "2025-01-15 09:05:00"
      }
    ]
  }
  ```
- **Campos obrigatórios:**
  - `order_id`: ID único do pedido (integer)
  - `first_name`: Primeiro nome do participante (string)
  - `last_name`: Sobrenome do participante (string)
  - `email`: Email do participante (string)
  - `phone`: Telefone do participante (string)
  - `cpf`: CPF do participante (string, pode ser vazio)
  - `city`: Cidade do participante (string)
  - `product_id`: ID do produto (integer)
  - `product_name`: Nome do produto (string)
  - `certificate_details`: Detalhes do certificado (string)
  - `certificate_logo`: URL do logo do certificado (string)
  - `certificate_background`: URL do background do certificado (string)
  - `order_date`: Data do pedido no formato "YYYY-MM-DD HH:MM:SS" (string)
- **Campos opcionais:**
  - `checkin_latitude`: Latitude do check-in (string, opcional)
  - `checkin_longitude`: Longitude do check-in (string, opcional)
  - `time_checkin`: Data e hora do check-in no formato "YYYY-MM-DD HH:MM:SS" (string, opcional)
    - **Nota:** Certificados sem `time_checkin` serão marcados como inválidos e não serão processados.
- **Saída (sucesso):**
  ```json
  {
    "certificate_quantity": 2,
    "existing_orders": [],
    "new_orders": [1234, 1235],
    "processing_date": "2025-01-20 10:30:45.123456"
  }
  ```
- **Saída (erro):**
  ```json
  {
    "status": 500,
    "message": "Internal Server Error",
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
