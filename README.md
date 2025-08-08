# Gerador de descrição para NFs (USD-BRL)

Este projeto Python busca a cotação do dólar na API do SGS (Sistema Gerenciador de Séries Temporais) do Banco Central do Brasil e gera um texto de conversão de moeda estrangeira para reais, conforme a IN RFB nº 1.312/2012.

## Funcionalidades

- Busca automática da cotação do dólar na API do SGS (Sistema Gerenciador de Séries Temporais) do Banco Central
- Cálculo automático do valor em reais
- Geração de texto formatado com valores e datas atualizadas
- Suporte para diferentes valores em USD
- Interface de linha de comando com flags para facilitar o uso
- **API REST**: Endpoints para integração com outras aplicações
- Fonte oficial do Banco Central do Brasil
- Transparência total com URL dos dados quando usando `--verbose`

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

Ou use o script de instalação automática:
```bash
chmod +x install.sh
./install.sh
```

## Uso

### API REST

O projeto inclui uma API REST para integração com outras aplicações:

#### **Endpoints Disponíveis:**

- **Health Check**: `GET /health`
- **API Info**: `GET /api/info`
- **Buscar Cotação**: `GET /api/rate?date=07082025`
- **Gerar Texto**: `POST /api/convert`

#### **Exemplo de Uso da API:**

```bash
# Health check
curl https://seu-app.onrender.com/health

# Gerar texto de conversão
curl -X POST https://seu-app.onrender.com/api/convert \
  -H "Content-Type: application/json" \
  -d '{
    "usd_amount": 6774.00,
    "date": "07082025",
    "show_url": true
  }'

# Buscar cotação
curl "https://seu-app.onrender.com/api/rate?date=07082025"
```

#### **Deploy no Render:**

O projeto está configurado para deploy automático no Render:

1. **Faça push para o GitHub:**
   ```bash
   git push origin main
   ```

2. **Acesse o Render:**
   - Vá para [render.com](https://render.com)
   - Faça login/cadastro
   - Clique em "New +" → "Web Service"

3. **Conecte com GitHub:**
   - Selecione seu repositório
   - O Render detectará automaticamente a configuração

4. **Configure o serviço:**
   - **Name**: `invoice-description-generator-api`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api:app`

5. **Clique em "Create Web Service"**

Após o deploy, sua API estará disponível em: `https://seu-app.onrender.com`

### Interface de Linha de Comando

```bash
# Uso básico (cotação de ontem)
python invoice_description_generator.py --input 6774.00

# Com data específica (formato DDMMYYYY)
python invoice_description_generator.py --input 6774.00 --date 07082025

# Com informações detalhadas (inclui URL dos dados)
python invoice_description_generator.py --input 6774.00 --date 02012025 --verbose

# Ver ajuda
python invoice_description_generator.py --help
```

### Como Módulo Python

```python
from invoice_description_generator import generate_conversion_text

# Gerar texto de conversão para USD 6.774,00
text = generate_conversion_text(6774.00)
print(text)
```

## Lógica de Datas

- **Flag `--date` opcional**: Se não fornecida, usa hoje como referência
- **Formato da data**: DDMMYYYY (ex: 07082025 para 07/08/2025)
- **Data da cotação**: Sempre o dia anterior à data de referência
- **Exemplo**: `--date 07082025` busca cotação de 06/08/2025

## API do SGS

O projeto utiliza a API oficial do SGS (Sistema Gerenciador de Séries Temporais) do Banco Central:

- **URL Base**: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados`
- **Código 1**: Taxa de câmbio - Dólar americano (venda) - Ajuste pro-rata
- **Formato**: JSON
- **Fonte**: Oficial do Banco Central do Brasil

## Exemplos de Saída

```bash
# Comando: python invoice_description_generator.py --input 6774.00
# Saída: Valor recebido em moeda estrangeira (USD 6.774,00), convertido conforme PTAX de venda de 07/08/2025 (R$ 5,4638), conforme IN RFB nº 1.312/2012. Valor total em reais: R$ 37.011,78.

# Comando: python invoice_description_generator.py --input 6774.00 --date 07082025 --verbose
# Saída: 
# Data de referência: 07/08/2025
# Buscando cotação de: 06/08/2025
# Gerador de Descrição de Conversão de Moeda
# ==================================================
# Valor em USD: 6,774.00
# 
# Texto gerado:
# ------------------------------
# Valor recebido em moeda estrangeira (USD 6.774,00), convertido conforme PTAX de venda de 06/08/2025 (R$ 5,4802), conforme IN RFB nº 1.312/2012. Valor total em reais: R$ 37.122,87.
# 
# 🔗 Fonte dos dados: https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json&dataInicial=06/08/2025&dataFinal=06/08/2025
```

## Estrutura do Projeto

- `invoice_description_generator.py`: Módulo principal com as funções de busca de cotação e geração de texto
- `api.py`: API REST Flask para integração com outras aplicações
- `requirements.txt`: Dependências do projeto
- `example.py`: Exemplo de uso do módulo
- `test_generator.py`: Testes automatizados
- `test_api.py`: Testes da API REST
- `setup.py`: Configuração de instalação
- `install.sh`: Script de instalação automática
- `render.yaml`: Configuração para deploy no Render
- `Procfile`: Configuração para deploy no Render
- `API_DOCUMENTATION.md`: Documentação detalhada da API

## Testes

Execute os testes para verificar se tudo está funcionando:

```bash
python test_generator.py
```

## Exemplos

Veja mais exemplos de uso:

```bash
python example.py
```

## Características Técnicas

- **Python 3.7+**: Compatível com versões modernas do Python
- **Dependências**: requests, beautifulsoup4, python-dateutil
- **API**: SGS do Banco Central do Brasil
- **Formatação**: Padrão brasileiro de moeda
- **Testes**: Cobertura completa com unittest
- **Documentação**: README detalhado com exemplos

## Transparência

O projeto oferece transparência total sobre a fonte dos dados:

- **URL Completa**: Quando usando `--verbose`, mostra a URL exata da API
- **Dados Oficiais**: Utiliza apenas dados oficiais do Banco Central
- **Auditoria**: Permite verificar diretamente na API a origem dos dados
- **Sem Hardcoding**: Não utiliza valores fixos ou simulados
