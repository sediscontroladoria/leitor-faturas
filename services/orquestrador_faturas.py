import os
import tempfile
from services.factory import ServiceFactory
from services.processador_dados import ProcessadorDados
from services.organizador_faturas import OrganizadorFaturas
from services.exportador_relatorios import ExportadorRelatorios
from utils.mapeamentos import DOTACAO_FIXA, RELACAO_FICHAS_ORCAMENTO

class OrquestradorFaturas:
    @staticmethod
    def processar_lote(
        arquivos_pdf, tipo_fatura, mes_comp, ano_comp, 
        tipo_debito, conta_fatura, complemento, 
        opcoes_saida, config_fatura, tracker=None
    ):
        leitor = config_fatura['leitor']
        separador = config_fatura['separador']
        mapa_fichas = config_fatura['mapa_fichas']
        headers = config_fatura['headers']
        coluna_id = config_fatura['coluna_id']
        lista_ordenacao = config_fatura['lista_ordenacao']
        
        organizador = OrganizadorFaturas()

        if not leitor or not separador:
            raise ValueError(f"Ferramentas para {tipo_fatura} não implementadas.")

        with tempfile.TemporaryDirectory() as pasta_trabalho:
            pasta_uploads = os.path.join(pasta_trabalho, 'uploads')
            pasta_separadas = os.path.join(pasta_trabalho, 'separadas')
            pasta_organizadas = os.path.join(pasta_trabalho, 'organizadas')
            os.makedirs(pasta_uploads)

            caminhos_pdfs = []
            for pdf in arquivos_pdf:
                caminho = os.path.join(pasta_uploads, pdf.name)
                with open(caminho, 'wb') as f:
                    f.write(pdf.getbuffer())
                caminhos_pdfs.append(caminho)

            faturas_lidas = []
            for i, caminho_pdf in enumerate(caminhos_pdfs):
                if tracker:
                    tracker.update(i, len(caminhos_pdfs), os.path.basename(caminho_pdf))
                
                fatura = leitor.processar(caminho_pdf)
                
                if fatura.identificador_ligacao not in lista_ordenacao:
                    continue
                
                if tipo_debito == 'Geral':
                    faturas_lidas.append(fatura)
                elif tipo_debito == 'Débito Automático' and fatura.debito_automatico == 'SIM':
                    faturas_lidas.append(fatura)
                elif tipo_debito == 'Débito Manual' and fatura.debito_automatico == 'NÃO':
                    faturas_lidas.append(fatura)

            if not faturas_lidas:
                return None

            resultados = {}

            if 'Gerar ZIP' in opcoes_saida:
                separador.separar(caminhos_pdfs, pasta_separadas)
                organizador.agrupar_por_mapeamento(
                    faturas_lidas, pasta_separadas, pasta_organizadas, mapa_fichas
                )
                zip_path_base = os.path.join(pasta_trabalho, f'Faturas_{tipo_fatura}')
                caminho_zip = organizador.compactar_saida(pasta_organizadas, zip_path_base)
                with open(caminho_zip, 'rb') as f:
                    resultados['zip'] = f.read()

            if 'Gerar Planilha' in opcoes_saida:
                df_final = ProcessadorDados.preparar_dataframe_faturas(
                    faturas_lidas, mapa_fichas, headers, coluna_id, lista_ordenacao
                )
                resultados['csv'] = ExportadorRelatorios.gerar_csv(df_final)

            if 'Gerar Relatório Final' in opcoes_saida:
                df_relatorio = ProcessadorDados.gerar_relatorio_final(
                    faturas_lidas, mapa_fichas, coluna_id, DOTACAO_FIXA, RELACAO_FICHAS_ORCAMENTO
                )
                
                resultados['relatorio'] = ExportadorRelatorios.gerar_excel_relatorio(
                    df_relatorio, faturas_lidas, tipo_fatura, mes_comp, ano_comp, 
                    tipo_debito, conta_fatura, complemento
                )

            return resultados