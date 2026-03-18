import os
import io
import tempfile
from services.factory import ServiceFactory
from services.processador_dados import ProcessadorDados
from services.organizador_faturas import OrganizadorFaturas

class OrquestradorFaturas:
    @staticmethod
    def processar_lote(
        arquivos_pdf, tipo_fatura, mes_comp, ano_comp, 
        tipo_debito, conta_fatura, complemento, 
        mapa_fichas, headers, coluna_id, 
        opcoes_saida, tracker=None
    ):
        leitor = ServiceFactory.get_leitor(tipo_fatura)
        separador = ServiceFactory.get_separador(tipo_fatura)
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
                    faturas_lidas, mapa_fichas, headers, coluna_id
                )
                csv_buffer = io.StringIO()
                df_final.to_csv(csv_buffer, index=False, sep=';', encoding='utf-8-sig')
                resultados['csv'] = csv_buffer.getvalue().encode('utf-8-sig')

            if 'Gerar Relatório Final' in opcoes_saida:
                df_relatorio = ProcessadorDados.gerar_relatorio_final(
                    faturas_lidas, mapa_fichas, coluna_id
                )
                rel_buffer = io.StringIO()
                venc_ref = faturas_lidas[0].vencimento if faturas_lidas else 'N/A'
                
                vl_total = sum(ProcessadorDados._converter_para_float(f.valor) for f in faturas_lidas)
                ir_total = sum(ProcessadorDados._converter_para_float(f.retencao_ir) for f in faturas_lidas)
                vb_total = vl_total + ir_total
                
                def fmt_br(v): return f'R$ {v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

                rel_buffer.write(f'Relatório das faturas {tipo_fatura} referentes a {mes_comp}/{ano_comp};;;;;;;\n')
                rel_buffer.write(f'{tipo_debito} - {conta_fatura} - Vencimento {venc_ref} - {complemento};;;;;;;\n')
                df_relatorio.to_csv(rel_buffer, index=False, sep=';', encoding='utf-8-sig')
                rel_buffer.write(f'Total Geral;;;;;{fmt_br(vl_total)};{fmt_br(ir_total)};{fmt_br(vb_total)}')
                resultados['relatorio'] = rel_buffer.getvalue().encode('utf-8-sig')

            return resultados