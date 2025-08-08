#!/usr/bin/env python3
"""
Script de teste para a API do Gerador de Descrição de Conversão de Moeda
"""

import requests
import json
import time

# Configuração da API
BASE_URL = "http://localhost:5001"

def test_health_check():
    """Testa o endpoint de health check"""
    print("🔍 Testando health check...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_api_info():
    """Testa o endpoint de informações da API"""
    print("\n🔍 Testando informações da API...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/info")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_get_rate():
    """Testa o endpoint de busca de cotação"""
    print("\n🔍 Testando busca de cotação...")
    
    try:
        # Teste sem data (cotação de ontem)
        response = requests.get(f"{BASE_URL}/api/rate")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Teste com data específica
        response = requests.get(f"{BASE_URL}/api/rate?date=07082025")
        print(f"\nStatus (com data): {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_convert_currency():
    """Testa o endpoint de conversão de moeda"""
    print("\n🔍 Testando conversão de moeda...")
    
    # Teste básico
    data = {
        "usd_amount": 6774.00
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/convert", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Teste com data específica
        data_with_date = {
            "usd_amount": 1000.00,
            "date": "07082025",
            "show_url": True
        }
        
        response = requests.post(f"{BASE_URL}/api/convert", json=data_with_date)
        print(f"\nStatus (com data e URL): {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_error_handling():
    """Testa o tratamento de erros"""
    print("\n🔍 Testando tratamento de erros...")
    
    # Teste com valor inválido
    data = {
        "usd_amount": -100
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/convert", json=data)
        print(f"Status (valor negativo): {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Teste com data inválida
        data_invalid_date = {
            "usd_amount": 1000.00,
            "date": "123"
        }
        
        response = requests.post(f"{BASE_URL}/api/convert", json=data_invalid_date)
        print(f"\nStatus (data inválida): {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Função principal que executa todos os testes"""
    print("🧪 Testando API do Gerador de Descrição de Conversão de Moeda")
    print("=" * 60)
    
    # Aguarda um pouco para o servidor inicializar
    print("⏳ Aguardando servidor inicializar...")
    time.sleep(2)
    
    tests = [
        ("Health Check", test_health_check),
        ("API Info", test_api_info),
        ("Get Rate", test_get_rate),
        ("Convert Currency", test_convert_currency),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name}: PASS")
            else:
                print(f"❌ {test_name}: FAIL")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Resumo dos resultados
    print(f"\n{'='*60}")
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram!")
    else:
        print("⚠️  Alguns testes falharam!")

if __name__ == "__main__":
    main()
