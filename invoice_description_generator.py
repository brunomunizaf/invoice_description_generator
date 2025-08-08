import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import locale
import re


def get_bb_dollar_rate(date=None):
    """
    Busca a cotação PTAX de venda do dólar no Banco Central do Brasil para uma data específica.
    Se não for fornecida uma data, usa o dia anterior.
    
    Args:
        date (datetime): Data para buscar a cotação (opcional)
    
    Returns:
        tuple: (cotação, data_formatada, url_completa) ou (None, None, None) se erro
    """
    if date is None:
        date = datetime.now() - timedelta(days=1)
    
    # Formata a data para o formato esperado
    date_str = date.strftime("%d/%m/%Y")
    
    try:
        # API do SGS - Sistema Gerenciador de Séries Temporais
        # Código 1 = Taxa de câmbio - Dólar americano (venda) - Ajuste pro-rata
        # Formato da data para a API: DD/MM/YYYY
        api_date = date.strftime("%d/%m/%Y")
        
        # URL da API do SGS
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Parâmetros para buscar cotação de venda do dólar
        params = {
            'formato': 'json',
            'dataInicial': api_date,
            'dataFinal': api_date
        }
        
        # Constrói a URL completa para mostrar
        param_str = '&'.join([f"{k}={v}" for k, v in params.items()])
        full_url = f"{url}?{param_str}"
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Busca pela cotação de venda nos dados retornados
        ptax_venda = None
        
        if isinstance(data, list):
            # Estrutura da API do SGS: lista de objetos com 'valor' e 'data'
            for item in data:
                if isinstance(item, dict):
                    if 'valor' in item:
                        ptax_venda = float(item['valor'])
                        break
        elif isinstance(data, dict):
            # Estrutura alternativa
            if 'valor' in data:
                ptax_venda = float(data['valor'])
        
        # Se não encontrou cotação, falha
        if ptax_venda is None:
            raise Exception("Não foi possível obter cotação do SGS. Verifique a data ou sua conexão com a internet.")
        
        return ptax_venda, date_str, full_url
        
    except Exception as e:
        raise Exception(f"Erro ao buscar cotação do SGS: {e}")


def format_currency(value, currency="BRL"):
    """
    Formata valor monetário no padrão brasileiro.
    
    Args:
        value (float): Valor a ser formatado
        currency (str): Moeda (BRL ou USD)
    
    Returns:
        str: Valor formatado
    """
    if currency == "BRL":
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    elif currency == "USD":
        return f"USD {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def generate_conversion_text(usd_amount, date=None, show_url=False):
    """
    Gera texto de conversão de moeda estrangeira para reais.
    
    Args:
        usd_amount (float): Valor em dólares
        date (datetime): Data para buscar cotação (opcional)
        show_url (bool): Se deve mostrar a URL dos dados
    
    Returns:
        str: Texto formatado de conversão
    """
    # Busca a cotação do dólar
    rate, date_str, url = get_bb_dollar_rate(date)
    
    # Calcula o valor em reais
    brl_amount = usd_amount * rate
    
    # Formata os valores
    usd_formatted = format_currency(usd_amount, "USD")
    rate_formatted = f"R$ {rate:.4f}".replace(".", ",")
    brl_formatted = format_currency(brl_amount, "BRL")
    
    # Gera o texto
    text = f"Valor recebido em moeda estrangeira ({usd_formatted}), convertido conforme PTAX de venda de {date_str} ({rate_formatted}), conforme IN RFB nº 1.312/2012. Valor total em reais: {brl_formatted}."
    
    # Adiciona a URL se solicitado
    if show_url:
        text += f"\n\n🔗 Fonte dos dados: {url}"
    
    return text


import sys
import argparse


def main():
    """
    Função principal que aceita argumentos da linha de comando.
    """
    parser = argparse.ArgumentParser(
        description="Gerador de Descrição de Conversão de Moeda",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python invoice_description_generator.py --input 6774.00
  python invoice_description_generator.py --input 1000.00 --date 02012025
  python invoice_description_generator.py --input 50000.00 --date 07082025
        """
    )
    
    parser.add_argument(
        "--input",
        type=float,
        required=True,
        help="Valor em dólares (ex: 6774.00)"
    )
    
    parser.add_argument(
        "--date",
        type=str,
        help="Data no formato DDMMYYYY (opcional, padrão: hoje). A cotação será buscada do dia anterior."
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostra informações detalhadas"
    )
    
    args = parser.parse_args()
    
    try:
        # Processa a data
        if args.date:
            # Valida formato DDMMYYYY
            if len(args.date) != 8 or not args.date.isdigit():
                print("❌ Erro: Data deve estar no formato DDMMYYYY (ex: 02012025)")
                sys.exit(1)
            
            try:
                # Converte DDMMYYYY para datetime
                day = args.date[:2]
                month = args.date[2:4]
                year = args.date[4:8]
                
                # Data de referência (data fornecida)
                reference_date = datetime(int(year), int(month), int(day))
                
                # Data para buscar cotação (dia anterior)
                quote_date = reference_date - timedelta(days=1)
                
                if args.verbose:
                    print(f"Data de referência: {reference_date.strftime('%d/%m/%Y')}")
                    print(f"Buscando cotação de: {quote_date.strftime('%d/%m/%Y')}")
                
            except ValueError as e:
                print(f"❌ Erro: Data inválida - {e}")
                sys.exit(1)
        else:
            # Se não foi fornecida data, usa hoje como referência e busca cotação de ontem
            reference_date = datetime.now()
            quote_date = reference_date - timedelta(days=1)
            
            if args.verbose:
                print(f"Data de referência: {reference_date.strftime('%d/%m/%Y')}")
                print(f"Buscando cotação de: {quote_date.strftime('%d/%m/%Y')}")
        
        if args.verbose:
            print("Gerador de Descrição de Conversão de Moeda")
            print("=" * 50)
            print(f"Valor em USD: {args.input:,.2f}")
            print()
        
        # Gera o texto usando a data de cotação (dia anterior)
        text = generate_conversion_text(args.input, quote_date, args.verbose)
        
        if args.verbose:
            print("Texto gerado:")
            print("-" * 30)
        
        print(text)
        
    except ValueError as e:
        print(f"❌ Erro: Valor inválido - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao gerar texto: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
