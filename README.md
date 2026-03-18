# Leitor de Faturas - Prefeitura de Taubaté (Leitor-Sedis)

O **Leitor-Sedis** é uma solução de engenharia de software desenvolvida para automatizar o ciclo completo de tratamento de faturas de concessionárias (Sabesp e EDP) para a Prefeitura Municipal de Taubaté. O sistema substitui processos manuais por um fluxo de trabalho otimizado que abrange desde a extração de dados brutos em PDFs até a organização sistêmica de arquivos e geração de relatórios financeiros consolidados.

## 1. Funcionalidades Principais

* **Extração Inteligente de Dados**: Utiliza motores de processamento baseados em Expressões Regulares (RegEx) para capturar informações críticas como número da fatura, consumo, valores e datas de vencimento.
* **Segmentação de Documentos**: Identifica e separa automaticamente faturas individuais contidas em arquivos PDF de múltiplas páginas.
* **Classificação e Organização**: Agrupa automaticamente as faturas em diretórios baseados na **Ficha (Ação)** orçamentária correspondente, utilizando mapeamentos internos de RGI e UC.
* **Relatórios Consolidados**: Gera planilhas CSV detalhadas e relatórios finais com cálculos de retenção de impostos (IR) e totais por dotação orçamentária.

## 2. Arquitetura do Sistema

O sistema utiliza uma arquitetura em camadas e padrões de projeto para garantir escalabilidade e baixa manutenção:

* **Camada de Modelos (`models/`)**: Define entidades de dados abstratas e concretas através de `dataclasses`, garantindo que todas as faturas sigam um contrato rigoroso.
* **Camada de Serviços (`services/`)**:
    * **Orquestrador**: Centraliza o fluxo de trabalho, desacoplando a lógica de processamento da interface do usuário.
    * **Factory Pattern**: A `ServiceFactory` gerencia a criação dinâmica de leitores e separadores específicos para cada concessionária.
    * **Processamento de Dados**: Camada dedicada à manipulação de DataFrames e lógica financeira.
* **Camada de Interface (`pages/` & `components/`)**: Interface modular construída em Streamlit, focada na experiência do usuário e reutilização de componentes.
* **Camada de Utilitários (`utils/`)**: Centraliza constantes, cabeçalhos de exportação e padrões RegEx, permitindo ajustes técnicos sem alteração no núcleo do sistema.

## 3. Tecnologias Utilizadas

* **Linguagem**: Python 3.x
* **Framework de UI**: Streamlit
* **Processamento de Dados**: Pandas
* **Manipulação de PDF**: PDFPlumber e PyPDF
* **Distribuição**: Suporte para empacotamento via PyInstaller.

## 4. Estrutura do Projeto

```text
leitor-sedis/
├── components/          # Componentes de interface reutilizáveis
├── models/              # Definições de classes e entidades (Fatura)
├── pages/               # Telas da aplicação Streamlit
├── services/            # Lógica de negócio (Leitura, Separação, Orquestração)
├── utils/               # Constantes, RegEx e configurações globais
├── tests/               # Amostras e scripts de teste de extração
├── streamlit_app.py     # Ponto de entrada da aplicação
└── requirements.txt     # Dependências do projeto
```

## 5. Como Executar

1.  **Instalação de Dependências**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Execução em Modo Desenvolvimento**:
    ```bash
    streamlit run streamlit_app.py
    ```

3.  **Build do Sistema:**:

    Para fazer a build do sistema em um executável, rode o comando:
    ```bash
    pyinstaller --onefile --noconsole  --name "Leitor de Faturas - Taubate"  --collect-all streamlit  --collect-all pdfplumber  --collect-all pypdf --collect-all openpyxl  --add-data "streamlit_app.py;."  --add-data "pages;pages"  --add-data "components;components"  --add-data "models;models"  --add-data "services;services"  --add-data "utils;utils" --add-data "assets;assets"  .\run_app.py
    ```

    Após o sistema fazer a geração do executável, é possível rodá-lo acessando a basta `./dist`.

## 6. Configurações e Manutenção

* **Atualização de Mapeamentos**: Novos RGIs ou UCs devem ser adicionados em `utils/constants.py` para garantir a correta classificação nas fichas orçamentárias.
* **Ajustes de Extração**: Caso o layout das faturas mude, os padrões de captura devem ser atualizados em `utils/regex_patterns.py`.

*Este projeto é de uso exclusivo para fins administrativos da Prefeitura Municipal de Taubaté.*