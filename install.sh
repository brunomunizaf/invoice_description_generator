#!/bin/bash

# Script de instalação para o Gerador de Descrição de Conversão de Moeda

echo "🚀 Instalando Gerador de Descrição de Conversão de Moeda..."
echo "=================================================="

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale o Python 3.7 ou superior."
    exit 1
fi

# Verifica a versão do Python
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.7"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Versão do Python ($python_version) é menor que a requerida ($required_version)"
    exit 1
fi

echo "✅ Python $python_version encontrado"

# Cria ambiente virtual (opcional)
read -p "Deseja criar um ambiente virtual? (y/n): " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Ambiente virtual criado e ativado"
fi

# Instala dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso"
else
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

# Executa testes
echo "🧪 Executando testes..."
python test_generator.py

if [ $? -eq 0 ]; then
    echo "✅ Todos os testes passaram!"
else
    echo "⚠️  Alguns testes falharam, mas a instalação foi concluída"
fi

# Executa exemplo
echo "📝 Executando exemplo..."
python example.py

echo ""
echo "🎉 Instalação concluída com sucesso!"
echo ""
echo "Para usar o gerador:"
echo "  python invoice_description_generator.py"
echo ""
echo "Para ver exemplos:"
echo "  python example.py"
echo ""
echo "Para executar testes:"
echo "  python test_generator.py"
echo ""
echo "Para usar como módulo:"
echo "  from invoice_description_generator import generate_conversion_text"
echo "  text = generate_conversion_text(6774.00)"
echo "  print(text)"
