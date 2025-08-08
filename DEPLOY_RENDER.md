# Deploy no Render - Guia Completo

## 🚀 Como Fazer Deploy no Render

### 1. **Preparação do Projeto**

O projeto já está configurado com todos os arquivos necessários:

- ✅ `render.yaml` - Configuração do Render
- ✅ `Procfile` - Comando de inicialização
- ✅ `requirements.txt` - Dependências Python
- ✅ `api.py` - API Flask
- ✅ `invoice_description_generator.py` - Módulo principal

### 2. **Passos para Deploy**

#### **Opção A: Deploy via GitHub (Recomendado)**

1. **Faça push para o GitHub:**
   ```bash
   git add .
   git commit -m "feat: Adiciona API Flask para deploy no Render"
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

#### **Opção B: Deploy Manual**

1. **Crie uma conta no Render**
2. **Crie um novo Web Service**
3. **Conecte com seu repositório GitHub**
4. **Configure:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api:app`

### 3. **Configuração Automática**

O arquivo `render.yaml` já está configurado:

```yaml
services:
  - type: web
    name: invoice-description-generator-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn api:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

### 4. **Endpoints Disponíveis**

Após o deploy, sua API estará disponível em:
`https://seu-app.onrender.com`

#### **Endpoints:**

- **Health Check**: `GET /health`
- **API Info**: `GET /api/info`
- **Buscar Cotação**: `GET /api/rate?date=07082025`
- **Gerar Texto**: `POST /api/convert`

### 5. **Testando a API**

#### **Health Check:**
```bash
curl https://seu-app.onrender.com/health
```

#### **Gerar Texto de Conversão:**
```bash
curl -X POST https://seu-app.onrender.com/api/convert \
  -H "Content-Type: application/json" \
  -d '{
    "usd_amount": 6774.00,
    "date": "07082025",
    "show_url": true
  }'
```

#### **Buscar Cotação:**
```bash
curl "https://seu-app.onrender.com/api/rate?date=07082025"
```

### 6. **Exemplo de Resposta**

```json
{
  "success": true,
  "text": "Valor recebido em moeda estrangeira (USD 6.774,00), convertido conforme PTAX de venda de 06/08/2025 (R$ 5,4802), conforme IN RFB nº 1.312/2012. Valor total em reais: R$ 37.122,87.",
  "data": {
    "usd_amount": 6774.0,
    "brl_amount": 37122.87,
    "rate": 5.4802,
    "date": "06/08/2025",
    "source": "SGS - Banco Central do Brasil",
    "source_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json&dataInicial=06/08/2025&dataFinal=06/08/2025"
  }
}
```

### 7. **Monitoramento**

- **Logs**: Acesse a aba "Logs" no Render
- **Métricas**: Monitore o uso de recursos
- **Deploy**: Deploy automático a cada push no GitHub

### 8. **Limites do Plano Gratuito**

- **750 horas/mês** (suficiente para uso contínuo)
- **512 MB RAM**
- **0.1 CPU**
- **SSL automático**
- **Domínio `.onrender.com`**

### 9. **Troubleshooting**

#### **Erro de Build:**
- Verifique se todas as dependências estão em `requirements.txt`
- Confirme se o Python 3.11 está sendo usado

#### **Erro de Runtime:**
- Verifique os logs no Render
- Confirme se a porta está sendo usada corretamente

#### **Timeout:**
- O plano gratuito pode ter timeouts em requisições longas
- Considere otimizar as chamadas para a API do BCB

### 10. **Próximos Passos**

1. **Deploy**: Siga os passos acima
2. **Teste**: Use os comandos curl para testar
3. **Integre**: Use a API em suas aplicações
4. **Monitore**: Acompanhe os logs e métricas

## 🎉 Sucesso!

Após o deploy, você terá uma API REST completa e funcional para gerar descrições de conversão de moeda!
