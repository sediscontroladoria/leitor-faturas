sabesp_patterns = {
    'num_documento': r'(SOR\d+)',
    'rgi': r'Pde/Rgi:\s*(\d+)',
    'hidrometro': r'Hidrômetro:\s*([A-Z0-9]+)',
    'valor': r'TOTAL\s*:?\s*R\$\s*[\s\*]*([\d,.]+)',
    'consumo': r'Água:\s*\d{2}/\d{2}/\d{2}\s*\d+\s*\d{2}/\d{2}/\d{2}\s*\d+\s*(\d+)',
    'vencimento': r'VENCIMENTO:\s*(\d{2}/\d{2}/\d{4})',
    'retencao_ir': r'\d+,\d+\%\s*(\d+,\d+)',
}