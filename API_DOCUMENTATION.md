# API Documentation - Gerador de Descrição de Conversão de Moeda

## Visão Geral

Esta API fornece endpoints para gerar descrições de conversão de moeda estrangeira para reais, conforme a IN RFB nº 1.312/2012. Utiliza dados oficiais do SGS (Sistema Gerenciador de Séries Temporais) do Banco Central do Brasil.

## Base URL

```
http://localhost:5000
```

## Endpoints

### 1. Health Check

**GET** `/health`

Verifica se a API está funcionando.

**Response:**
```json
{
  "status": "healthy",
  "service": "invoice_description_generator",
  "version": "1.0.0"
}
```

### 2. Informações da API

**GET** `/api/info`

Retorna informações sobre a API.

**Response:**
```json
{
  "name": "Invoice Description Generator API",
  "version": "1.0.0",
  "description": "API para geração de descrições de conversão de moeda",
  "endpoints": {
    "POST /api/convert": "Gerar texto de conversão",
    "GET /api/rate": "Buscar cotação do dólar",
    "GET /api/info": "Informações da API",
    "GET /health": "Health check"
  },
  "source": "SGS - Banco Central do Brasil",
  "format": "DDMMYYYY para datas"
}
```

### 3. Buscar Cotação

**GET** `/api/rate`

Busca apenas a cotação do dólar para uma data específica.

**Query Parameters:**
- `date` (opcional): Data no formato DDMMYYYY (ex: 07082025)

**Response:**
```json
{
  "success": true,
  "data": {
    "rate": 5.4638,
    "date": "07/08/2025",
    "source": "SGS - Banco Central do Brasil",
    "source_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json&dataInicial=07/08/2025&dataFinal=07/08/2025"
  }
}
```

### 4. Gerar Texto de Conversão

**POST** `/api/convert`

Gera o texto completo de conversão de moeda.

**Request Body:**
```json
{
  "usd_amount": 6774.00,
  "date": "07082025",  // opcional, formato DDMMYYYY
  "show_url": false    // opcional, se deve incluir URL dos dados
}
```

**Response:**
```json
{
  "success": true,
  "text": "Valor recebido em moeda estrangeira (USD 6.774,00), convertido conforme PTAX de venda de 07/08/2025 (R$ 5,4638), conforme IN RFB nº 1.312/2012. Valor total em reais: R$ 37.011,78.",
  "data": {
    "usd_amount": 6774.00,
    "brl_amount": 37011.78,
    "rate": 5.4638,
    "date": "07/08/2025",
    "source": "SGS - Banco Central do Brasil",
    "source_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json&dataInicial=07/08/2025&dataFinal=07/08/2025"
  }
}
```

## Códigos de Status

- `200`: Sucesso
- `400`: Erro de validação (dados inválidos)
- `404`: Endpoint não encontrado
- `500`: Erro interno do servidor

## Exemplos de Uso

### cURL

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Buscar Cotação:**
```bash
curl "http://localhost:5000/api/rate?date=07082025"
```

**Gerar Texto de Conversão:**
```bash
curl -X POST http://localhost:5000/api/convert \
  -H "Content-Type: application/json" \
  -d '{
    "usd_amount": 6774.00,
    "date": "07082025",
    "show_url": true
  }'
```

### JavaScript

**Health Check:**
```javascript
fetch('http://localhost:5000/health')
  .then(response => response.json())
  .then(data => console.log(data));
```

**Buscar Cotação:**
```javascript
fetch('http://localhost:5000/api/rate?date=07082025')
  .then(response => response.json())
  .then(data => console.log(data));
```

**Gerar Texto de Conversão:**
```javascript
fetch('http://localhost:5000/api/convert', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    usd_amount: 6774.00,
    date: '07082025',
    show_url: true
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Python

**Health Check:**
```python
import requests

response = requests.get('http://localhost:5000/health')
print(response.json())
```

**Buscar Cotação:**
```python
import requests

response = requests.get('http://localhost:5000/api/rate?date=07082025')
print(response.json())
```

**Gerar Texto de Conversão:**
```python
import requests

data = {
    'usd_amount': 6774.00,
    'date': '07082025',
    'show_url': True
}

response = requests.post('http://localhost:5000/api/convert', json=data)
print(response.json())
```

## Validações

### Parâmetros Obrigatórios

- `usd_amount`: Deve ser um número positivo

### Parâmetros Opcionais

- `date`: Deve estar no formato DDMMYYYY (ex: 07082025)
- `show_url`: Boolean (true/false)

### Tratamento de Erros

**Valor inválido:**
```json
{
  "success": false,
  "error": "usd_amount deve ser um número positivo"
}
```

**Data inválida:**
```json
{
  "success": false,
  "error": "date deve estar no formato DDMMYYYY (ex: 07082025)"
}
```

**Erro interno:**
```json
{
  "success": false,
  "error": "Erro interno: Não foi possível obter cotação do SGS..."
}
```

## Lógica de Datas

- Se `date` não for fornecida, usa hoje como referência
- A cotação é sempre buscada do dia anterior à data de referência
- Exemplo: `date=07082025` busca cotação de 06/08/2025

## Fonte dos Dados

- **API**: SGS (Sistema Gerenciador de Séries Temporais) do Banco Central
- **URL**: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados`
- **Código**: 1 (Taxa de câmbio - Dólar americano - venda)
- **Formato**: JSON

## CORS

A API suporta CORS para permitir requisições de aplicações frontend.

## Logs

A API registra logs de todas as operações para facilitar o debug e monitoramento.
