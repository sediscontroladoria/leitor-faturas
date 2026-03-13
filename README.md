# Leitor de Faturas - Prefeitura de Taubaté

Este repositório contém o sistema de processamento e organização automatizada de faturas desenvolvido para a Prefeitura Municipal de Taubaté. 

## Descrição do Projeto

O `Leitor-Sedis` é uma aplicação baseada em Python e Streamlit projetada para gerenciar o ciclo completo de tratamento de faturas de concessionárias. 

O sistema resolve o problema de processamento manual de grandes volumes de arquivos PDF, realizando a leitura de dados, separação e organização dos documentos em diretórios baseados nas regras de negócios do projeto.

## Funcionalidades Principais

**1. Extração Automatizada de Dados:** 
- Utiliza a extração de dados com base em expressões regulares (RegEx) para capturar informações críticas de diversas faturas simultaneamente.

**2. Separação de Documentos:** 
- Identifica e segmenta faturas individuais contidas em um único arquivo PDF, garantindo a integridade e a individualização de cada registro documental.

**3. Organização Sistêmica:** 
- Agrupa automaticamente as faturas em pastas nomeadas de acordo com a Ficha (Ação) correspondente, utilizando um mapeamento interno de RGIs que elimina a necessidade de consultas manuais a tabelas externas.

**4. Relatórios Consolidados:** 
- Gera planilhas em formato CSV com todos os dados extraídos, permitindo auditoria rápida e exportação imediata para outros sistemas de gestão municipal.

## Arquitetura de Software

- **Service Factory:** Centraliza a criação de instâncias de serviços, permitindo a expansão do suporte a novas concessionárias com impacto mínimo no código existente.
- **Abstração de Serviços:** Define contratos claros através de classes base abstratas para leitores e separadores, assegurando consistência no comportamento do sistema.
- **Modelagem de Dados Imutável:** Utiliza dataclasses para representar a estrutura das faturas, promovendo a integridade dos dados durante todo o fluxo de processamento.
- **Separação de Preocupações:** Isola componentes de interface, lógica de negócio, modelos de dados e utilitários em diretórios específicos, facilitando o desenvolvimento e futuras manutenções.

## Estrutura do Repositório

- `models`: Definições de estruturas de dados e entidades fundamentais do sistema.
- `services`: Implementações da lógica de negócio, incluindo extração, separação, organização e processamento de dados.
- `pages`: Módulos de interface que compõem as diferentes telas da aplicação web.
- `components`: Widgets e elementos de interface de usuário reutilizáveis.
- `utils`: Armazena constantes, padrões de busca e mapeamentos estáticos de cabeçalhos.

## Requisitos e Tecnologias

- `Python 3.x`: Linguagem base.
- `Streamlit`: Interface de Usuário.
- `Pandas`: Manipulação e estruturação de dados em DataFrames.
- `pdfplumber` e `pypdf`: Processamento e extração de conteúdo de arquivos PDF.