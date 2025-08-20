# Análise de Repositórios Populares do GitHub

**Data da Análise:** 20/08/2025
**Total de Repositórios Analisados:** 10

## 1. Introdução e Hipóteses

Este estudo analisa os repositórios mais populares do GitHub para compreender suas características em termos de maturidade, contribuições, releases, atualizações, linguagens e resolução de issues.

### Hipóteses Informais:
- **H1:** Repositórios populares tendem a ser maduros (mais de 1 ano)
- **H2:** Repositórios populares recebem muitas contribuições externas
- **H3:** Repositórios populares lançam releases frequentemente
- **H4:** Repositórios populares são atualizados frequentemente
- **H5:** Repositórios populares usam linguagens mainstream (JavaScript, Python, TypeScript)
- **H6:** Repositórios populares têm alta taxa de resolução de issues (>80%)

## 2. Metodologia

Utilizamos a API GraphQL do GitHub para coletar dados dos 10 repositórios mais populares (ordenados por estrelas). Para cada repositório, coletamos:

- Data de criação e última atualização
- Total de pull requests aceitas
- Número de releases
- Linguagem primária
- Issues totais e fechadas

## 3. Resultados

### RQ01: Sistemas populares são maduros/antigos?
**Métrica:** Idade do repositório em dias

- **Mediana da idade:** 3401.41 dias (9.32 anos)
- **Média da idade:** 3433.50 dias (9.41 anos)
- **Repositórios maduros (>1 ano):** 10 de 10 (100.0%)

**Resultado:** ✅ Hipótese confirmada - A maioria dos repositórios populares são maduros.

### RQ02: Sistemas populares recebem muita contribuição externa?
**Métrica:** Total de pull requests aceitas

- **Mediana de PRs aceitas:** 873
- **Média de PRs aceitas:** 4114.90
- **Repositório com mais PRs:** freeCodeCamp/freeCodeCamp (25,720 PRs)

**Resultado:** ✅ Hipótese confirmada - Repositórios populares recebem contribuições significativas.

### RQ03: Sistemas populares lançam releases com frequência?
**Métrica:** Total de releases

- **Mediana de releases:** 0
- **Média de releases:** 0.10
- **Repositórios com releases:** 1 de 10 (10.0%)

**Resultado:** ❌ Hipótese refutada - Muitos repositórios não usam o sistema de releases do GitHub.

### RQ04: Sistemas populares são atualizados com frequência?
**Métrica:** Tempo até a última atualização

- **Mediana do tempo desde última atualização:** 33.73 dias
- **Média do tempo desde última atualização:** 85.64 dias
- **Repositórios ativos (últimos 30 dias):** 4 de 10 (40.0%)

**Resultado:** ❌ Hipótese refutada - Nem todos os repositórios são atualizados frequentemente.

### RQ05: Sistemas populares são escritos nas linguagens mais populares?
**Métrica:** Linguagem primária

**Distribuição por linguagem:**
- **Python:** 4 repositório(s) (40.0%)
- **TypeScript:** 2 repositório(s) (20.0%)
- **Markdown:** 1 repositório(s) (10.0%)

**Repositórios em linguagens mainstream:** 6 de 10 (60.0%)

**Resultado:** ✅ Hipótese confirmada - A maioria usa linguagens mainstream.

### RQ06: Sistemas populares possuem um alto percentual de issues fechadas?
**Métrica:** Taxa de resolução de issues

- **Mediana da taxa de resolução:** 93.94%
- **Média da taxa de resolução:** 83.77%
- **Repositórios com alta resolução (>80%):** 6 de 8 (75.0%)

**Resultado:** ✅ Hipótese confirmada - Repositórios populares mantêm alta taxa de resolução.

## 4. Análise por Linguagem (RQ07)

**Questão:** Sistemas escritos em linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizados com mais frequência?

### TypeScript
- **Número de repositórios:** 2
- **PRs aceitas (mediana):** 14705
- **Releases (mediana):** 0
- **Dias desde última atualização (mediana):** 0.16

### Markdown
- **Número de repositórios:** 1
- **PRs aceitas (mediana):** 142
- **Releases (mediana):** 0
- **Dias desde última atualização (mediana):** 22.09

### Python
- **Número de repositórios:** 4
- **PRs aceitas (mediana):** 1208
- **Releases (mediana):** 0
- **Dias desde última atualização (mediana):** 62.89

## 5. Discussão

### Descobertas Principais:
1. **Maturidade:** Repositórios populares tendem a ser projetos estabelecidos há vários anos
2. **Contribuições:** Variam drasticamente, com alguns projetos recebendo dezenas de milhares de contribuições
3. **Releases:** Muitos projetos populares não utilizam o sistema formal de releases do GitHub
4. **Atualizações:** A frequência de atualizações varia, com alguns projetos muito ativos e outros menos
5. **Linguagens:** Há uma mistura de linguagens mainstream e especializadas
6. **Issues:** A maioria mantém boa taxa de resolução de issues


### Conclusões:
Os repositórios mais populares do GitHub apresentam características diversas, mas tendem a ser projetos maduros e bem mantidos, com boa gestão de issues e contribuições ativas da comunidade.

