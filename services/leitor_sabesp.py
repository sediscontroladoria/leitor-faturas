from services.leitor import Leitor
from models.fatura_sabesp import FaturaSabesp
from utils.regex_patterns import sabesp_patterns

class LeitorSabesp(Leitor):
    def processar(self, pdf_path):
        texto = self._extrair_texto(pdf_path)
        p = sabesp_patterns
        
        return FaturaSabesp(
            num_fatura=self._get_match(p['num_fatura'], texto),
            rgi=self._get_match(p['rgi'], texto),
            hidrometro=self._get_match(p['hidrometro'], texto),
            valor=self._get_match(p['valor'], texto),
            consumo=self._get_match(p['consumo'], texto),
            vencimento=self._get_match(p['vencimento'], texto),
            debito_automatico='SIM' if 'DÉBITO AUTOMÁTICO' in texto else 'NÃO',
            retencao_ir=self._get_match(p['retencao_ir'], texto),
        )