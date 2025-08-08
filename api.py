#!/usr/bin/env python3
"""
API Flask para o Gerador de Descrição de Conversão de Moeda
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import logging

from invoice_description_generator import generate_conversion_text, get_bb_dollar_rate

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Permite CORS para aplicações frontend

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'invoice_description_generator',
        'version': '1.0.0'
    })

@app.route('/api/convert', methods=['POST'])
def convert_currency():
    """
    Endpoint para gerar texto de conversão de moeda
    
    Request Body:
    {
        "usd_amount": 6774.00,
        "date": "07082025",  # opcional, formato DDMMYYYY
        "show_url": false     # opcional, se deve incluir URL dos dados
    }
    
    Response:
    {
        "success": true,
        "text": "Valor recebido em moeda estrangeira...",
        "data": {
            "usd_amount": 6774.00,
            "brl_amount": 37011.78,
            "rate": 5.4638,
            "date": "07/08/2025",
            "source_url": "https://api.bcb.gov.br/..."  # se show_url=true
        }
    }
    """
    try:
        # Validação dos dados de entrada
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Dados não fornecidos'
            }), 400
        
        # Validação do valor em USD
        usd_amount = data.get('usd_amount')
        if not usd_amount or not isinstance(usd_amount, (int, float)) or usd_amount <= 0:
            return jsonify({
                'success': False,
                'error': 'usd_amount deve ser um número positivo'
            }), 400
        
        # Processamento da data
        date_str = data.get('date')
        date_obj = None
        
        if date_str:
            # Valida formato DDMMYYYY
            if len(date_str) != 8 or not date_str.isdigit():
                return jsonify({
                    'success': False,
                    'error': 'date deve estar no formato DDMMYYYY (ex: 07082025)'
                }), 400
            
            try:
                # Converte DDMMYYYY para datetime
                day = date_str[:2]
                month = date_str[2:4]
                year = date_str[4:8]
                
                # Data de referência (data fornecida)
                reference_date = datetime(int(year), int(month), int(day))
                
                # Data para buscar cotação (dia anterior)
                date_obj = reference_date - timedelta(days=1)
                
            except ValueError as e:
                return jsonify({
                    'success': False,
                    'error': f'Data inválida: {str(e)}'
                }), 400
        
        # Flag para mostrar URL
        show_url = data.get('show_url', False)
        
        # Gera o texto de conversão
        text = generate_conversion_text(usd_amount, date_obj, show_url)
        
        # Busca dados adicionais para a resposta
        rate, date_str, url = get_bb_dollar_rate(date_obj)
        brl_amount = usd_amount * rate
        
        # Monta a resposta
        response_data = {
            'success': True,
            'text': text,
            'data': {
                'usd_amount': usd_amount,
                'brl_amount': round(brl_amount, 2),
                'rate': rate,
                'date': date_str,
                'source': 'SGS - Banco Central do Brasil'
            }
        }
        
        # Adiciona URL se solicitado
        if show_url:
            response_data['data']['source_url'] = url
        
        logger.info(f"Conversão realizada: USD {usd_amount} -> BRL {brl_amount}")
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Erro na conversão: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/api/rate', methods=['GET'])
def get_rate():
    """
    Endpoint para buscar apenas a cotação do dólar
    
    Query Parameters:
    - date: DDMMYYYY (opcional)
    
    Response:
    {
        "success": true,
        "data": {
            "rate": 5.4638,
            "date": "07/08/2025",
            "source_url": "https://api.bcb.gov.br/..."
        }
    }
    """
    try:
        # Processamento da data
        date_str = request.args.get('date')
        date_obj = None
        
        if date_str:
            # Valida formato DDMMYYYY
            if len(date_str) != 8 or not date_str.isdigit():
                return jsonify({
                    'success': False,
                    'error': 'date deve estar no formato DDMMYYYY (ex: 07082025)'
                }), 400
            
            try:
                # Converte DDMMYYYY para datetime
                day = date_str[:2]
                month = date_str[2:4]
                year = date_str[4:8]
                
                # Data de referência (data fornecida)
                reference_date = datetime(int(year), int(month), int(day))
                
                # Data para buscar cotação (dia anterior)
                date_obj = reference_date - timedelta(days=1)
                
            except ValueError as e:
                return jsonify({
                    'success': False,
                    'error': f'Data inválida: {str(e)}'
                }), 400
        
        # Busca a cotação
        rate, date_str, url = get_bb_dollar_rate(date_obj)
        
        response_data = {
            'success': True,
            'data': {
                'rate': rate,
                'date': date_str,
                'source': 'SGS - Banco Central do Brasil',
                'source_url': url
            }
        }
        
        logger.info(f"Cotação buscada: {rate} em {date_str}")
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Erro ao buscar cotação: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/api/info', methods=['GET'])
def get_info():
    """Endpoint para informações sobre a API"""
    return jsonify({
        'name': 'Invoice Description Generator API',
        'version': '1.0.0',
        'description': 'API para geração de descrições de conversão de moeda',
        'endpoints': {
            'POST /api/convert': 'Gerar texto de conversão',
            'GET /api/rate': 'Buscar cotação do dólar',
            'GET /api/info': 'Informações da API',
            'GET /health': 'Health check'
        },
        'source': 'SGS - Banco Central do Brasil',
        'format': 'DDMMYYYY para datas'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint não encontrado'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Erro interno do servidor'
    }), 500

if __name__ == '__main__':
    # Configuração do servidor
    import os
    
    port = int(os.environ.get('PORT', 5001))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
