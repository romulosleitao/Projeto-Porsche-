import pandas as pd
import json

caminho_excel = "C:/Users/romul/Desktop/py.files/Projeto_Porsche/scr/porsche_database_sanitized.xlsx"
caminho_json = "C:/Users/romul/Desktop/py.files/Projeto_Porsche/scr/kpis_dashboard.json"

print("Lendo a planilha sanitizada completa...")
df = pd.read_excel(caminho_excel, sheet_name="Sanitized")

# Limpeza e conversão dos tipos de dados
df['SalesPriceSanitized'] = pd.to_numeric(df['SalesPriceSanitized'], errors='coerce')
df['SaleDateSanitized'] = pd.to_datetime(df['SaleDateSanitized'], errors='coerce')
df = df.dropna(subset=['SalesPriceSanitized', 'SaleDateSanitized'])

# Extração de períodos
df['Ano'] = df['SaleDateSanitized'].dt.year
df['Mes'] = df['SaleDateSanitized'].dt.strftime('%Y-%m') # Ex: 2023-01

# --- 1. KPIs de Alta Performance ---
faturamento_total = float(df['SalesPriceSanitized'].sum())
lucro_operacional = faturamento_total * 0.18 # Margem Porsche simulada
total_unidades = int(df.shape[0])
ticket_medio = faturamento_total / total_unidades if total_unidades > 0 else 0

# --- 2. Análise Temporal (Receita por Mês/Ano) ---
faturamento_mensal = df.groupby('Mes')['SalesPriceSanitized'].sum().to_dict()

# --- 3. Análise de Produto (Modelos) ---
modelos_vendas = df['PorscheModelSanitized'].value_counts().to_dict()

# --- 4. Análise Geográfica (Top 5 Estados) ---
vendas_estado = df['StateSanitized'].value_counts().head(5).to_dict()

# --- 5. Logística e Pagamento ---
status_entrega = df['DeliveryStatusSanitized'].value_counts().to_dict()
metodos_pagamento = df['PayMethodSanitized'].value_counts().to_dict()

# Empacotando o JSON Complexo
dados_json = {
    "kpis": {
        "faturamento_total": faturamento_total,
        "lucro_operacional": lucro_operacional,
        "total_unidades": total_unidades,
        "ticket_medio": ticket_medio
    },
    "graficos": {
        "tendencia_mensal": {
            "labels": list(faturamento_mensal.keys()),
            "valores": list(faturamento_mensal.values())
        },
        "mix_produtos": modelos_vendas,
        "mapa_estados": vendas_estado,
        "operacional": {
            "status_entrega": status_entrega,
            "metodos_pagamento": metodos_pagamento
        }
    }
}

print("Gerando JSON corporativo...")
with open(caminho_json, "w", encoding="utf-8") as arquivo:
    json.dump(dados_json, arquivo, ensure_ascii=False, indent=4)

print("SUCESSO! JSON gerado com dados reais da base Porsche.")