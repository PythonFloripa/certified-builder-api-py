"""
Teste local simplificado usando apenas AWS Lambda Powertools.

Este script simula eventos do API Gateway e testa diretamente
o handler da Lambda sem dependências externas.
"""

import json
from lambda_function import lambda_handler


def create_api_gateway_event(method: str, path: str, body: dict = None, query_string_parameters: dict = None) -> dict:
    """
    Cria um evento simulado do API Gateway REST.
    
    Args:
        method: Método HTTP (GET, POST, etc.)
        path: Caminho da requisição
        body: Corpo da requisição (opcional)
        
    Returns:
        Evento formatado para API Gateway REST
    """
    return {
        "httpMethod": method,
        "path": path,
        "pathParameters": None,
        "queryStringParameters": query_string_parameters,
        "headers": {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        "body": json.dumps(body) if body else None,
        "isBase64Encoded": False,
        "requestContext": {
            "httpMethod": method,
            "path": path,
            "stage": "test",
            "requestId": "test-request-id-123",
            "identity": {
                "sourceIp": "127.0.0.1"
            }
        }
    }


class MockLambdaContext:
    """Contexto Lambda simulado para testes locais."""
    
    def __init__(self):
        self.function_name = "certified-builder-local-test"
        self.function_version = "$LATEST"
        self.invoked_function_arn = "arn:aws:lambda:local:123456789012:function:test"
        self.memory_limit_in_mb = 128
        self.remaining_time_in_millis = 300000
        self.log_group_name = "/aws/lambda/test"
        self.log_stream_name = "test-stream"
        self.aws_request_id = "test-request-id-123"


def test_create_certificate():
    """Testa o endpoint de criação de certificados."""
    print("🧪 Testando endpoint de criação de certificados...")
    
    # Dados de teste
    request_data = {
        "product_id": "316"
    }
    
    # Cria evento simulado
    event = create_api_gateway_event(
        method="POST",
        path="/api/v1/certificate/create",
        body=request_data
    )
    
    # Contexto simulado
    context = MockLambdaContext()
    
    try:
        # Chama o handler da Lambda
        print(f"Enviando requisição: {json.dumps(request_data, indent=2)}")
        response = lambda_handler(event, context)
        
        # Exibe resposta
        print("Resposta recebida:")
        print(f"Status Code: {response.get('statusCode', 'N/A')}")
        
        # Tenta fazer parse do body se for string
        body = response.get('body', {})
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                pass
        
        print(f"   Body: {json.dumps(body, indent=2, ensure_ascii=False)}")
        
        # Verifica se foi sucesso
        status_code = response.get('statusCode', 500)
        if 200 <= status_code < 300:
            print("Teste executado com sucesso!")
        else:
            print("Teste falhou!")
            
        return response
        
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        return None

def test_fetch_certificate_by_order_id():
    """Testa o endpoint de busca de certificados."""
    print("🧪 Testando endpoint de busca de certificados...")
    
    # Dados de teste (query params devem ser strings)
    request_data = {
        "order_id": "1826"
    }
    
    # Cria evento simulado
    event = create_api_gateway_event(
        method="GET",
        path="/api/v1/certificate/fetch",
        query_string_parameters=request_data
    )
    
    # Contexto simulado
    context = MockLambdaContext()
    
    try:
        # Chama o handler da Lambda
        print(f"Enviando requisição: {json.dumps(request_data, indent=2)}")
        response = lambda_handler(event, context)
        
        # Exibe resposta
        print("Resposta recebida:")
        print(f"Status Code: {response.get('statusCode', 'N/A')}")
        
        # Tenta fazer parse do body se for string
        body = response.get('body', {})
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                pass
        
        print(f"   Body: {json.dumps(body, indent=2, ensure_ascii=False)}")
        
        # Verifica se foi sucesso
        status_code = response.get('statusCode', 500)
        if 200 <= status_code < 300:
            print("Teste executado com sucesso!")
        else:
            print("Teste falhou!")
            
        return response
        
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        return None

def test_fetch_certificate_by_product_id():
    """Testa o endpoint de busca de certificados por product_id."""
    print("🧪 Testando endpoint de busca de certificados por product_id...")
    
    # Dados de teste (query params devem ser strings)
    request_data = {
        "product_id": "1678"
    }
    
    # Cria evento simulado
    event = create_api_gateway_event(
        method="GET",
        path="/api/v1/certificate/fetch",
        query_string_parameters=request_data
    )
    
    # Contexto simulado
    context = MockLambdaContext()
    
    try:
        # Chama o handler da Lambda
        print(f"Enviando requisição: {json.dumps(request_data, indent=2)}")
        response = lambda_handler(event, context)
        
        # Exibe resposta
        print("Resposta recebida:")
        print(f"Status Code: {response.get('statusCode', 'N/A')}")
        
        # Tenta fazer parse do body se for string
        body = response.get('body', {})
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                pass
        
        print(f"   Body: {json.dumps(body, indent=2, ensure_ascii=False)}")
        
        # Verifica se foi sucesso
        status_code = response.get('statusCode', 500)
        if 200 <= status_code < 300:
            print("Teste executado com sucesso!")
        else:
            print("Teste falhou!")
            
        return response
        
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        return None

def test_fetch_certificate_by_email():
    """Testa o endpoint de busca de certificados por email."""
    print("🧪 Testando endpoint de busca de certificados por email...")
    
    # Dados de teste
    request_data = {
        "email": "suzi.harima94@gmail.com"
    }
    
    # Cria evento simulado
    event = create_api_gateway_event(
        method="GET",
        path="/api/v1/certificate/fetch",
        query_string_parameters=request_data
    )
    
    # Contexto simulado
    context = MockLambdaContext()
    
    try:
        # Chama o handler da Lambda
        print(f"Enviando requisição: {json.dumps(request_data, indent=2)}")
        response = lambda_handler(event, context)
        
        # Exibe resposta
        print("Resposta recebida:")
        print(f"Status Code: {response.get('statusCode', 'N/A')}")
        
        # Tenta fazer parse do body se for string
        body = response.get('body', {})
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                pass
        
        print(f"   Body: {json.dumps(body, indent=2, ensure_ascii=False)}")
        
        # Verifica se foi sucesso
        status_code = response.get('statusCode', 500)
        if 200 <= status_code < 300:
            print("Teste executado com sucesso!")
        else:
            print("Teste falhou!")
            
        return response
        
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        return None

def test_fetch_certificate_by_email_and_product_id():
    """Testa o endpoint de busca de certificados por email e product_id."""
    print("🧪 Testando endpoint de busca de certificados por email e product_id...")
    
    # Dados de teste
    request_data = {
        "email": "suzi.harima94@gmail.com",
        "product_id": "1678"
    }
    
    # Cria evento simulado
    event = create_api_gateway_event(
        method="GET",
        path="/api/v1/certificate/fetch",
        query_string_parameters=request_data
    )
    
    # Contexto simulado
    context = MockLambdaContext()
    
    try:
        # Chama o handler da Lambda
        print(f"Enviando requisição: {json.dumps(request_data, indent=2)}")
        response = lambda_handler(event, context)
        
        # Exibe resposta
        print("Resposta recebida:")
        print(f"Status Code: {response.get('statusCode', 'N/A')}")
        
        # Tenta fazer parse do body se for string
        body = response.get('body', {})
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                pass
        
        print(f"   Body: {json.dumps(body, indent=2, ensure_ascii=False)}")
        
        # Verifica se foi sucesso
        status_code = response.get('statusCode', 500)
        if 200 <= status_code < 300:
            print("Teste executado com sucesso!")
        else:
            print("Teste falhou!")
            
        return response
        
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        return None


if __name__ == "__main__":
    # Executa os testes
    # test_create_certificate()
    test_fetch_certificate_by_order_id()
    test_fetch_certificate_by_product_id()
    test_fetch_certificate_by_email()
    test_fetch_certificate_by_email_and_product_id()
