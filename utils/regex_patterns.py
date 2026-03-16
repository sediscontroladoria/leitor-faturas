sabesp_patterns = {
    'num_fatura': r'(SOR\d+)',
    'rgi': r'Pde/Rgi:\s*(\d+)',
    'hidrometro': r'Hidrômetro:\s*([A-Z0-9]+)',
    'valor': r'TOTAL\s*:?\s*R\$\s*[\s\*]*([\d,.]+)',
    'consumo': r'Água:\s*\d{2}/\d{2}/\d{2}\s*\d+(?:\s*\d{2}/\d{2}/\d{2}\s*\d+)?\s*(\d+)',
    'vencimento': r'VENCIMENTO:\s*(\d{2}/\d{2}/\d{4})',
    'retencao_ir': r'\d+,\d+\%\s*-?(\d+,\d+)',
}

edp_patterns = {
    'num_fatura': r'\d{27}(\d{8})',
    'uc': r'(\d[\d.]{5,}-\d{2})',
    'medidor': r'MEDIDOR:\s*0*(\d+)',
    'valor': r'(?:(?:\d{2}/\d{2}/\d{4})\s+|TOTAL\s+)([\d.\s]+,\s*[\d\s]+)',
    'consumo': r'Consumo kWh\s*(\d+[\s\d]*),\d+',
    'vencimento': r'(?:MEDIDOR:|CEP:)\s*.*?\s*(\d{2}/\d{2}/\d{4})',
    'retencao_ir': r'Retenção Imposto de Renda\s*(\d+,\d+\s*\d+)',
}

