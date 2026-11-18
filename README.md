# Análise de Dados de Varejo com Python

Projeto de análise exploratória e preparação de dados de varejo, desenvolvido em Python e Pandas. O notebook investiga uma base transacional em nível de item, verifica sua estrutura e qualidade, padroniza campos e produz recortes descritivos sobre clientes, compras e categorias de produtos.

> **Objetivo do projeto:** transformar uma base extensa de registros de compras em informações organizadas e indicadores descritivos que possam apoiar a compreensão do comportamento de compra e do mix de produtos.

## Problema de negócio

Uma base de varejo pode conter centenas de milhares de linhas, códigos que exigem interpretação, registros repetidos em diferentes níveis e categorias sem classificação padronizada. Antes de extrair conclusões, é necessário compreender a granularidade dos dados, verificar sua consistência e definir quais indicadores são adequados.

O projeto trabalha com perguntas exploratórias como:

- Qual é a dimensão e a estrutura da base?
- Como os clientes estão distribuídos por gênero, estado civil, número de filhos e segmento?
- Quais categorias de produtos concentram mais registros?
- Como se comporta o volume de compras por cliente e por nota fiscal?
- O que aparece no recorte de clientes classificados no segmento A?

## Base de dados e granularidade

O notebook registra uma base com **830.000 linhas e 10 colunas**. Cada linha representa um registro de item associado a uma compra, e não necessariamente uma compra completa.

| Campo | Descrição documentada |
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

A execução registrada identificou **18.471 identificadores de compra** e **1.000 identificadores de clientes**. Como a base está no nível de item, a repetição de `CO_ID` em várias linhas é esperada quando uma nota contém vários produtos.

## Metodologia

1. **Carregamento:** leitura do CSV com Pandas, utilizando separador ponto e vírgula.
2. **Inspeção inicial:** visualização de amostras, dimensões, nomes de colunas, tipos, memória utilizada e estatísticas descritivas.
3. **Qualidade dos dados:** verificação de valores ausentes, textos vazios e linhas integralmente repetidas.
4. **Interpretação e padronização:** conversão dos códigos de estado civil para rótulos descritivos e substituição do marcador `#N/D` por `ND` na categoria.
5. **Análise descritiva:** funções para identificar os três valores mais frequentes e menos frequentes por coluna, além de estatísticas para número de filhos.
6. **Recorte de negócio:** filtragem do segmento A e agrupamento de registros por categoria e gênero, com contagem de clientes e compras distintas.
7. **Exportação:** gravação da base tratada em CSV.

## Tecnologias e conceitos

- Python
- Pandas
- Google Colab / Jupyter Notebook
- Leitura e exportação de CSV
- Inspeção e preparação de dados
- Tratamento de categorias e tipos
- `value_counts()`, `groupby()`, `agg()`, `nunique()` e estatística descritiva
- Funções reutilizáveis para frequência e representatividade

## Resultados observados no notebook

<details>
<summary><strong>Dimensão e qualidade inicial</strong></summary>

| Verificação | Resultado registrado |
|---|---:|
| Linhas | 830.000 |
| Colunas | 10 |
| Clientes distintos (`CL_ID`) | 1.000 |
| Compras distintas (`CO_ID`) | 18.471 |
| Valores nulos identificados na inspeção inicial | 0 em todas as colunas |
| Linhas integralmente repetidas além da primeira ocorrência | 96.553 |
| Linhas pertencentes a grupos de repetição (`keep=False`) | 184.330 |

**Atenção à interpretação:** o notebook identificou linhas integralmente repetidas, mas não documenta uma regra de negócio suficiente para excluir automaticamente esses registros. Por isso, o projeto não deve afirmar que as duplicidades foram resolvidas. A granularidade de item e a chave de negócio precisam ser validadas antes de qualquer deduplicação.

</details>

<details>
<summary><strong>Distribuição geral por categoria</strong></summary>

| Categoria | Registros |
|---|---:|
| Alimentos | 434.767 |
| Higiene | 155.574 |
| Limpeza | 145.754 |
| Bebidas | 43.299 |
| Pet | 32.399 |
| Acessórios | 14.557 |
| ND (marcador normalizado) | 3.650 |

Alimentos é a categoria com maior volume de registros na base analisada. O marcador `#N/D` foi padronizado para `ND`; isso melhora a consistência textual, mas não recupera a classificação original ausente.

</details>

<details>
<summary><strong>Indicadores descritivos de clientes</strong></summary>

- Distribuição por gênero: 432.576 registros classificados como F (52,12%) e 397.424 como M (47,88%).
- Segmento econômico B: 530.163 registros (63,88%); C: 232.101 (27,96%); A: 67.736 (8,16%).
- Número de filhos: média de 1,1465 por registro; mínimo 0 e máximo 4.

Essas estatísticas descrevem os registros disponíveis e não devem ser interpretadas como estimativas representativas de uma população externa à base.

</details>

<details>
<summary><strong>Recorte do segmento A</strong></summary>

| Categoria | Registros no segmento A |
|---|---:|
| Alimentos | 35.292 |
| Higiene | 12.844 |
| Limpeza | 11.915 |
| Bebidas | 3.601 |
| Pet | 2.620 |
| Acessórios | 1.175 |
| ND | 289 |

No mesmo recorte, o notebook registrou:

| Gênero | Clientes distintos | Compras distintas | Registros de itens |
|---|---:|---:|---:|
| F | 40 | 700 | 32.875 |
| M | 44 | 792 | 34.861 |

</details>

## Como executar

1. Clone ou baixe este repositório.
2. Instale as dependências:

   ```bash
   pip install pandas
   ```

3. Abra `Thiago_Rodrigues_Analise_Varejo_T8.ipynb` no Google Colab ou em Jupyter.
4. Disponibilize o arquivo de dados esperado pelo notebook no ambiente de execução e ajuste o caminho de leitura, se necessário.
5. Execute as células em ordem.

O notebook original utiliza caminhos e recursos do Google Colab/Google Drive. Em execução local, será necessário adaptar esses caminhos.

## Limitações e cuidados de interpretação

- A análise é descritiva; não há modelo preditivo, teste causal ou previsão de vendas neste projeto.
- Os registros estão em nível de item. Contagem de linhas não equivale a quantidade de notas fiscais ou clientes.
- A presença de 96.553 linhas integralmente repetidas foi identificada, mas a decisão de removê-las exige validação da chave e da origem dos dados.
- A categoria `ND` representa informação não classificada; não deve ser tratada como uma categoria comercial conhecida.
- O notebook contém uma etapa de conversão de data para objetos `date`; a validação do tipo final e a padronização de datas devem ser conferidas na versão executada.
- As conclusões refletem a base analisada e não permitem, isoladamente, inferir causalidade ou comportamento de todo o mercado varejista.

## Próximas evoluções

- documentar a origem, licença e dicionário completo da base;
- automatizar a validação de tipos e qualidade com verificações reproduzíveis;
- definir uma chave de negócio para investigar duplicidades;
- construir indicadores por período, cliente, categoria e compra;
- criar visualizações para apoiar a leitura dos resultados;
- organizar o notebook em etapas reutilizáveis e adicionar instruções de execução sem dependência de caminhos pessoais do Colab.

## Escopo e transparência

Este repositório apresenta um estudo demonstrativo de análise exploratória e preparação de dados. Os resultados acima foram extraídos das saídas registradas no notebook. Não são métricas de uma operação comercial própria nem evidência de impacto financeiro real.

---

**Foco do portfólio:** Exploratory Data Analysis · Retail Analytics · Data Quality · Python · Pandas
