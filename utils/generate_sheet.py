from pathlib import Path
from dataclasses import asdict
from pandas import DataFrame

HEADERS = {
        'num_documento': 'Nº Documento',
        'rgi': 'RGI',
        'hidrometro': 'Hidrômetro',
        'vencimento': 'Vencimento',
        'valor': 'Valor (R$)',
        'consumo': 'Consumo (m³)',
        'retencao_ir': 'Retenção IR'
    }

def generate_sheet(faturas_list, folder_path, filename):
    output_dir = Path(folder_path)    
    output_dir.mkdir(parents=True, exist_ok=True)
    final_path = output_dir / filename
    
    data = [asdict(f) for f in faturas_list]
    df = DataFrame(data)
    
    
    
    df.columns = [HEADERS.get(col, col.replace('_', ' ').title()) for col in df.columns]
    
    df.to_csv(
        final_path, 
        index=False, 
        encoding='utf-8-sig', 
        sep=';', 
        decimal=','
    )    
    
    print(f'\nPlanilha "{filename}" gerada com sucesso em: {output_dir.absolute()}')