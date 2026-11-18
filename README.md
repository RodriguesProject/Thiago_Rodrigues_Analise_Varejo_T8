# Análise Exploratória de Dados de Varejo com Python

[![Python](https://img.shields.io/badge/Python-EDA-blue)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Biblioteca-Pandas-150458)](https://pandas.pydata.org/)
[![Notebook](https://img.shields.io/badge/Ambiente-Google%20Colab%20%7C%20Jupyter-orange)](https://jupyter.org/)

Projeto de **análise exploratória e preparação de dados (Exploratory Data Analysis — EDA)** aplicado a uma base transacional de varejo. O estudo utiliza Python e Pandas para compreender a estrutura dos dados, avaliar aspectos de qualidade, padronizar campos e produzir recortes descritivos sobre clientes, compras e categorias de produtos.

> **Em uma frase:** transformar uma base extensa de registros de itens de compra em uma visão organizada, documentada e passível de análise, sem extrapolar o que os dados efetivamente permitem concluir.

## 1. Contexto e problema de negócio

Bases transacionais de varejo podem reunir grande volume de registros, códigos que exigem interpretação, categorias não padronizadas e repetições que precisam ser avaliadas à luz da granularidade dos dados. Uma análise confiável começa antes dos gráficos ou indicadores: é necessário entender o que cada linha representa, verificar a consistência dos campos e distinguir repetição legítima de possível duplicidade.

Este projeto investiga questões exploratórias como:

- Qual é a dimensão da base e qual é a granularidade dos registros?
- Existem valores ausentes, campos em branco ou linhas integralmente repetidas?
- Como os registros se distribuem por categoria, gênero e segmento econômico?
- Quais categorias concentram maior volume de itens registrados?
- O que o recorte do segmento A revela quando observado por categoria e gênero?

**Decisão analítica importante:** a base está em nível de item. Portanto, a contagem de linhas não equivale à quantidade de notas fiscais, clientes ou unidades vendidas.

## 2. Base de dados e dicionário resumido

A execução registrada no notebook analisou **830.000 linhas e 10 colunas**, com **1.000 identificadores de clientes** e **18.471 identificadores de compra**.

| Campo | Significado documentado |
|---|---|
| `DATA` | Data da compra |
| `CO_ID` | Identificador da compra / nota fiscal |
| `CL_ID` | Identificador do cliente |
| `CL_GENERO` | Gênero informado na base |
| `CL_EC` | Código do estado civil |
| `CL_FHL` | Número de filhos |
| `CL_SEG` | Segmento econômico (A, B ou C) |
| `PR_ID` | Código do produto (SKU) |
| `PR_CAT` | Categoria do produto |
| `PR_NOME` | Nome do produto |

O arquivo de dados utilizado na execução não está versionado como CSV aberto neste repositório; há um arquivo compactado com a base tratada. A origem, licença e condições de redistribuição da base devem ser confirmadas antes de republicá-la ou utilizá-la fora do contexto de estudo.

## 3. Metodologia

O notebook está organizado em etapas de exploração, preparação e análise:

1. **Carregamento:** leitura de arquivo CSV com Pandas, considerando o delimitador ponto e vírgula.
2. **Inspeção estrutural:** amostras, dimensões, nomes de colunas, tipos, memória utilizada e estatísticas descritivas.
3. **Diagnóstico de qualidade:** verificação de valores nulos, textos vazios ou compostos por espaços e linhas integralmente repetidas.
4. **Interpretação e padronização:** conversão dos códigos de estado civil para rótulos descritivos e normalização do marcador `#N/D` para `ND` na categoria.
5. **Análise descritiva:** frequências, valores mais e menos frequentes, estatísticas de número de filhos e funções auxiliares para resumir colunas.
6. **Recorte analítico:** filtragem do segmento A e agrupamento por categoria e gênero, com contagem de registros, clientes distintos e compras distintas.
7. **Exportação:** gravação da base preparada em CSV.

## 4. Tecnologias e competências demonstradas

- **Python** e **Pandas**
- Google Colab / Jupyter Notebook
- Leitura e exportação de arquivos CSV
- Inspeção de estrutura, tipos e qualidade de dados
- Tratamento de categorias e conversão de campos
- Análise de frequência e estatística descritiva
- Agrupamentos com `groupby()`, agregações, `value_counts()` e `nunique()`
- Criação de funções auxiliares para reutilização de análises

## 5. Resultados observados na execução registrada

Os números abaixo foram transcritos das saídas registradas no notebook. São resultados descritivos da base analisada, não indicadores de uma operação própria.

### 5.1. Estrutura e qualidade inicial

| Verificação | Resultado |
|---|---:|
| Registros (linhas) | 830.000 |
| Colunas | 10 |
| Clientes distintos (`CL_ID`) | 1.000 |
| Compras distintas (`CO_ID`) | 18.471 |
| Valores nulos identificados | 0 em todas as colunas |
| Linhas integralmente repetidas além da primeira ocorrência | 96.553 |
| Linhas que pertencem a grupos repetidos (`keep=False`) | 184.330 |

**Interpretação das repetições:** o notebook identifica linhas integralmente repetidas, mas não estabelece uma chave de negócio nem comprova a causa de cada repetição. Por isso, não foi feita uma afirmação de que as duplicidades foram resolvidas ou removidas. A investigação exige validação da origem e da regra de unicidade antes de qualquer exclusão.

### 5.2. Distribuição de registros por categoria

| Categoria | Registros |
|---|---:|
| Alimentos | 434.767 |
| Higiene | 155.574 |
| Limpeza | 145.754 |
| Bebidas | 43.299 |
| Pet | 32.399 |
| Acessórios | 14.557 |
| ND | 3.650 |

Alimentos concentra o maior volume de registros na base analisada. `ND` representa o marcador originalmente identificado como `#N/D`; a padronização melhora a consistência textual, mas não recupera a classificação ausente.

### 5.3. Distribuição descritiva de características dos clientes

- **Gênero:** 432.576 registros classificados como F (52,12%) e 397.424 como M (47,88%).
- **Segmento econômico:** B — 530.163 registros (63,88%); C — 232.101 (27,96%); A — 67.736 (8,16%).
- **Número de filhos:** média de 1,1465 por registro, mínimo 0 e máximo 4.

Essas proporções descrevem os registros da base, não estimativas representativas de uma população externa. Como há várias linhas associadas a clientes e compras, não se deve interpretar automaticamente percentuais calculados sobre linhas como percentuais de pessoas.

### 5.4. Recorte do segmento A

| Categoria | Registros |
|---|---:|
| Alimentos | 35.292 |
| Higiene | 12.844 |
| Limpeza | 11.915 |
| Bebidas | 3.601 |
| Pet | 2.620 |
| Acessórios | 1.175 |
| ND | 289 |

O notebook também registrou o seguinte agrupamento por gênero no segmento A:

| Gênero | Clientes distintos | Compras distintas | Registros de itens |
|---|---:|---:|---:|
| F | 40 | 700 | 32.875 |
| M | 44 | 792 | 34.861 |

## 6. Como executar

1. Clone ou baixe este repositório.
2. Instale a dependência principal:

   ```bash
   pip install pandas
   ```

3. Abra `Thiago_Rodrigues_Analise_Varejo_T8.ipynb` no Google Colab ou Jupyter.
4. Disponibilize o arquivo de dados esperado pelo notebook no ambiente de execução.
5. Revise e ajuste o caminho de leitura no notebook e execute as células em ordem.

**Observação de reprodutibilidade:** o notebook original utiliza recursos e caminhos do Google Colab/Google Drive. Uma execução local exige adaptar esses caminhos. Os resultados apresentados neste README correspondem às saídas já registradas no notebook; não significam que uma execução limpa e independente tenha sido validada em todos os ambientes.

## 7. Limitações e cuidados de interpretação

- A análise é exploratória e descritiva. Não há modelo preditivo, teste causal ou previsão de vendas.
- O conjunto de colunas documentado não contém preço, custo ou valor monetário. Portanto, este projeto **não calcula faturamento, margem, ticket médio ou rentabilidade**.
- A base está no nível de item; contagem de linhas não equivale a quantidade de compras ou clientes.
- As 96.553 linhas integralmente repetidas além da primeira ocorrência foram identificadas, mas não devem ser removidas sem regra de negócio validada.
- `ND` significa categoria não classificada, e não uma categoria comercial.
- A conversão de `DATA` para objetos `date` deve ser validada na execução, inclusive quanto ao tipo final e à consistência temporal.
- A origem e a licença da base precisam ser confirmadas para fins de redistribuição.
- Os resultados descrevem somente a base utilizada e não comprovam impacto financeiro ou operacional real.

## 8. Próximas evoluções técnicas

- Tornar a leitura dos dados independente de caminhos pessoais do Colab.
- Registrar fonte, licença e dicionário completo da base.
- Automatizar verificações de qualidade e tipos de dados.
- Investigar as repetições com uma chave de negócio validada.
- Criar indicadores por período, cliente, categoria e compra, respeitando a granularidade.
- Adicionar visualizações e testes de consistência reproduzíveis.
- Separar funções de preparação e análise em módulos reutilizáveis.

## 9. Escopo do projeto

Estudo demonstrativo de **Retail Analytics, Exploratory Data Analysis e Data Quality**, desenvolvido em contexto de aprendizagem aplicada. Os resultados numéricos são os que constam das saídas registradas no notebook. Não representam dados de uma empresa própria, resultado de consultoria ou impacto financeiro comprovado.

---

**Portfolio focus:** Retail Analytics · Exploratory Data Analysis · Data Quality · Python · Pandas


## Pipeline reproduzível e testes automatizados

Foi acrescentado o módulo `analise_varejo.py`, que separa carregamento, validação estrutural, preparação, diagnóstico de qualidade, tabelas descritivas, exportação e gráficos. O fluxo preserva os dados de origem e não remove duplicidades automaticamente.

### Instalação e execução

```bash
pip install -r requirements.txt
python analise_varejo.py --input "Base Varejo.csv" --output-dir outputs
```

Parâmetros opcionais: `--sep` (padrão `;`) e `--encoding` (padrão `utf-8-sig`). A base deve conter as dez colunas descritas neste README.

### Arquivos gerados

- `resumo_analise.json`: dimensões e indicadores de qualidade.
- `relatorio_qualidade.csv`: valores nulos e textos vazios por coluna.
- `categorias.csv`, `segmento_a_categorias.csv` e `segmento_a_genero.csv`: tabelas descritivas.
- `registros_por_categoria.png` e `registros_por_segmento.png`: visualizações.

### Testes

Execute `python -m unittest -v`. Os testes utilizam uma amostra sintética pequena para verificar a lógica e as exportações; não substituem a execução da base original de 830 mil linhas.

O conjunto original de dados não está incluído no repositório. Assim, os resultados históricos da seção anterior continuam sendo os resultados registrados no notebook original; a reprodução independente desses números depende de executar o pipeline com a mesma base.
