from pathlib import Path
from services.leitor import Leitor
from models.fatura_edp import FaturaEDP
from utils.regex_patterns import edp_patterns

class LeitorEDP(Leitor):
    def processar(self, pdf_path):
        texto = self._extrair_texto(pdf_path)
        p = edp_patterns
        
        num_fatura_arquivo = Path(pdf_path).stem
        
        uc_raw = self._get_match(p['uc'], texto).replace(' ', '')
        uc_limpa = uc_raw.replace('.', '').replace('-', '').lstrip('0')

        return FaturaEDP(
            num_fatura=num_fatura_arquivo,
            uc=uc_limpa,
            medidor=self._get_match(p['medidor'], texto).replace(' ', ''),
            valor=self._get_match(p['valor'], texto).replace(' ', ''),
            consumo=self._get_match(p['consumo'], texto).replace(' ', ''),
            vencimento=self._get_match(p['vencimento'], texto).replace(' ', ''),
            debito_automatico='SIM' if 'Débito automático' in texto else 'NÃO',
            retencao_ir=self._get_match(p['retencao_ir'], texto).replace(' ', ''),
        )