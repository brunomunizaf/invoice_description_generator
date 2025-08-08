#!/usr/bin/env python3
"""
Exemplo de uso do Gerador de Descrição de Conversão de Moeda
"""

from invoice_description_generator import generate_conversion_text, get_bb_dollar_rate
from datetime import datetime


def exemplo_basico():
    """Exemplo básico com o valor fornecido no enunciado."""
    print("=== Exemplo Básico ===")
    usd_value = 6774.00
    text = generate_conversion_text(usd_value)
    print(text)
    print()


def exemplo_diferentes_valores():
    """Exemplo com diferentes valores em USD."""
    print("=== Diferentes Valores ===")
    
    valores = [1000.00, 5000.00, 10000.00, 25000.00]
    
    for valor in valores:
        text = generate_conversion_text(valor)
        print(f"USD {valor:,.2f}: {text}")
        print()


def exemplo_data_especifica():
    """Exemplo com data específica (simulado)."""
    print("=== Data Específica ===")
    
    # Simula uma data específica (usando valor simulado)
    data_especifica = datetime(2025, 8, 7)  # 07/08/2025
    usd_value = 6774.00
    
    text = generate_conversion_text(usd_value, data_especifica)
    print(text)
    print()


def exemplo_busca_cotacao():
    """Exemplo de busca direta da cotação."""
    print("=== Busca de Cotação ===")
    
    rate, date = get_bb_dollar_rate()
    print(f"Cotação PTAX de venda em {date}: R$ {rate:.4f}")
    print()


def main():
    """Função principal que executa todos os exemplos."""
    print("Gerador de Descrição de Conversão de Moeda - Exemplos")
    print("=" * 60)
    print()
    
    try:
        exemplo_basico()
        exemplo_diferentes_valores()
        exemplo_data_especifica()
        exemplo_busca_cotacao()
        
        print("Todos os exemplos executados com sucesso!")
        
    except Exception as e:
        print(f"Erro durante a execução dos exemplos: {e}")


if __name__ == "__main__":
    main()
