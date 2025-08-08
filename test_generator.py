#!/usr/bin/env python3
"""
Testes para o Gerador de Descrição de Conversão de Moeda
"""

import unittest
from invoice_description_generator import format_currency, generate_conversion_text
from datetime import datetime


class TestCurrencyFormatter(unittest.TestCase):
    """Testes para a função de formatação de moeda."""
    
    def test_format_brl(self):
        """Testa formatação de valores em BRL."""
        self.assertEqual(format_currency(1234.56, "BRL"), "R$ 1.234,56")
        self.assertEqual(format_currency(1000000.00, "BRL"), "R$ 1.000.000,00")
        self.assertEqual(format_currency(0.50, "BRL"), "R$ 0,50")
    
    def test_format_usd(self):
        """Testa formatação de valores em USD."""
        self.assertEqual(format_currency(1234.56, "USD"), "USD 1.234,56")
        self.assertEqual(format_currency(6774.00, "USD"), "USD 6.774,00")
    
    def test_format_default(self):
        """Testa formatação sem especificar moeda."""
        self.assertEqual(format_currency(1234.56), "R$ 1.234,56")


class TestConversionText(unittest.TestCase):
    """Testes para a função de geração de texto de conversão."""
    
    def test_generate_text_basic(self):
        """Testa geração básica de texto."""
        text = generate_conversion_text(6774.00)
        
        # Verifica se o texto contém elementos essenciais
        self.assertIn("Valor recebido em moeda estrangeira", text)
        self.assertIn("USD 6.774,00", text)
        self.assertIn("PTAX de venda", text)
        self.assertIn("IN RFB nº 1.312/2012", text)
        self.assertIn("Valor total em reais", text)
    
    def test_generate_text_different_amounts(self):
        """Testa geração com diferentes valores."""
        amounts = [1000.00, 5000.00, 10000.00]
        
        for amount in amounts:
            text = generate_conversion_text(amount)
            self.assertIn(f"USD {amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), text)
    
    def test_generate_text_with_date(self):
        """Testa geração com data específica."""
        specific_date = datetime(2025, 8, 7)
        text = generate_conversion_text(6774.00, specific_date)
        
        self.assertIn("07/08/2025", text)


class TestIntegration(unittest.TestCase):
    """Testes de integração."""
    
    def test_complete_flow(self):
        """Testa o fluxo completo de geração de texto."""
        # Simula um cenário real
        usd_amount = 6774.00
        text = generate_conversion_text(usd_amount)
        
        # Verifica se o texto está bem formatado
        self.assertTrue(len(text) > 50)  # Texto deve ter pelo menos 50 caracteres
        self.assertIn("R$", text)  # Deve conter símbolo do real
        self.assertIn("USD", text)  # Deve conter símbolo do dólar


def run_tests():
    """Executa todos os testes."""
    print("Executando testes do Gerador de Descrição de Conversão de Moeda")
    print("=" * 60)
    
    # Cria uma suíte de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adiciona os testes
    suite.addTests(loader.loadTestsFromTestCase(TestCurrencyFormatter))
    suite.addTests(loader.loadTestsFromTestCase(TestConversionText))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Executa os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    if success:
        print("\n✅ Todos os testes passaram!")
    else:
        print("\n❌ Alguns testes falharam!")
