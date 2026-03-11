from pathlib import Path
from dataclasses import asdict
from pandas import DataFrame

def generate_sheet(faturas_list, folder_path, filename='faturas.csv'):
    output_dir = Path(folder_path)    
    output_dir.mkdir(parents=True, exist_ok=True)
    final_path = output_dir / filename
    
    dados = [asdict(f) for f in faturas_list]
    df = DataFrame(dados)
    
    df.columns = [col.replace('_', ' ').title() for col in df.columns]
    
    df.to_csv(final_path, index=False, encoding='utf-8-sig', sep=';')    
    print(f'\nPlanilha "{filename}" gerada com sucesso em: {output_dir.absolute()}')