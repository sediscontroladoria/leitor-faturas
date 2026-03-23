# Leitor Automatizado de Faturas - Leitor SEDIS

O **Leitor SEDIS** é uma plataforma de automação especializada, desenvolvida para a **Prefeitura Municipal de Taubaté**. Sua missão é transformar o processamento penoso de faturas de concessionárias (Sabesp e EDP) em um fluxo de trabalho digital, ágil e à prova de erros.

Através de motores de extração baseados em **RegEx** e uma arquitetura robusta, o sistema realiza o ciclo completo: extração de metadados, classificação orçamentária automática, organização física de arquivos e geração de inteligência financeira consolidada.

## Funcionalidades

* **Extração de dados**: Identificação precisa de RGIs, UCs, consumos, valores e retenções de IR em PDFs complexos.
* **Segmentação inteligente**: Separação automática de faturas individuais a partir de arquivos PDF consolidados (múltiplas páginas).
* **Inteligência orçamentária**: Classificação automática baseada na **Ficha (Ação)**, correlacionando o identificador da fatura com a dotação correta.
* **Exportação multiformato**: Geração de planilhas CSV para auditoria, arquivos ZIP organizados e relatórios finais em Excel (.XLSX) formatados para uso administrativo.

## Arquitetura e engenharia de software

O sistema adota uma arquitetura em camadas e segue rigorosamente os princípios de **Clean Code** e **Injeção de Dependências**:

| Camada | Responsabilidade |
| :--- | :--- |
| **`models/`** | Define as entidades de dados (`FaturaSabesp`, `FaturaEDP`) via `dataclasses` e contratos abstratos. |
| **`services/`** | O núcleo lógico. Contém o **Orquestrador** (fluxo), a **Factory** (instanciação dinâmica), o **Processador** (cálculos) e o **Exportador** (geração de arquivos). |
| **`components/`** | Widgets modulares de interface que garantem consistência visual e reusabilidade. |
| **`utils/`** | Gestão de metadados. Isola as regras de negócio (mapeamentos) das configurações de interface e padrões RegEx. |

---

## Configuração e execução

### Pré-requisitos
* Python 3.10+
* Dependências listadas em `requirements.txt`

### Ambiente de desenvolvimento
1.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
2.  Inicie a aplicação:
    ```bash
    streamlit run streamlit_app.py
    ```

### Distribuição (build)
Para gerar um executável independente (.EXE) com todas as dependências incluídas:
```bash
pyinstaller --onefile --noconsole --name "Leitor de Faturas - Taubate" --add-data "streamlit_app.py;." --add-data "pages;pages" --add-data "components;components" --add-data "models;models" --add-data "services;services" --add-data "utils;utils" --add-data "assets;assets" --collect-all streamlit .\run_app.py
```

## Manutenção e evolução

O sistema foi projetado para ser sustentável a longo prazo sem necessidade de alteração no código-fonte principal:

1.  **Atualização Orçamentária**: Para novos anos ou mudanças de fichas, altere apenas `utils/mapeamentos.py`.
2.  **Ajustes de Layout**: Se as concessionárias alterarem o design das faturas, atualize os padrões em `utils/regex_patterns.py`.
3.  **Configurações de Interface**: Opções de menus e listas suspensas são geridas em `utils/config_ui.py`.

## Stack tecnológica

* **Core**: Python 3
* **Interface**: Streamlit
* **Dados**: Pandas
* **PDF Engine**: PDFPlumber & PyPDF
* **Exportação**: OpenPyXL

> *Este software é um ativo de uso exclusivo administrativo da Secretaria de Desenvolvimento e Inclusão Social (SEDIS) da Prefeitura Municipal de Taubaté.*