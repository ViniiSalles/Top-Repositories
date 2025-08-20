import pandas as pd
from datetime import datetime

def generate_research_report():
    """Gera um relatório final estruturado em markdown"""
    df = pd.read_csv("repo_metrics.csv")
    
    report = f"""# Análise de Repositórios Populares do GitHub

**Data da Análise:** {datetime.now().strftime("%d/%m/%Y")}
**Total de Repositórios Analisados:** {len(df)}

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

"""
    
    # Calcular estatísticas para RQ01
    idade_mediana = df['idade_repositorio_dias'].median()
    idade_media = df['idade_repositorio_dias'].mean()
    repos_maduros = len(df[df['maturidade'] == 'Maduro'])
    
    report += f"""- **Mediana da idade:** {idade_mediana:.2f} dias ({idade_mediana/365:.2f} anos)
- **Média da idade:** {idade_media:.2f} dias ({idade_media/365:.2f} anos)
- **Repositórios maduros (>1 ano):** {repos_maduros} de {len(df)} ({repos_maduros/len(df)*100:.1f}%)

**Resultado:** {"✅ Hipótese confirmada" if repos_maduros/len(df) > 0.7 else "❌ Hipótese refutada"} - A maioria dos repositórios populares são maduros.

### RQ02: Sistemas populares recebem muita contribuição externa?
**Métrica:** Total de pull requests aceitas

"""
    
    # Calcular estatísticas para RQ02
    prs_mediana = df['pull_requests_aceitas'].median()
    prs_media = df['pull_requests_aceitas'].mean()
    
    report += f"""- **Mediana de PRs aceitas:** {prs_mediana:.0f}
- **Média de PRs aceitas:** {prs_media:.2f}
- **Repositório com mais PRs:** {df.loc[df['pull_requests_aceitas'].idxmax(), 'nameWithOwner']} ({df['pull_requests_aceitas'].max():,.0f} PRs)

**Resultado:** {"✅ Hipótese confirmada" if prs_mediana > 500 else "⚠️ Hipótese parcialmente confirmada"} - Repositórios populares recebem contribuições significativas.

### RQ03: Sistemas populares lançam releases com frequência?
**Métrica:** Total de releases

"""
    
    # Calcular estatísticas para RQ03
    releases_mediana = df['releases'].median()
    releases_media = df['releases'].mean()
    repos_com_releases = len(df[df['releases'] > 0])
    
    report += f"""- **Mediana de releases:** {releases_mediana:.0f}
- **Média de releases:** {releases_media:.2f}
- **Repositórios com releases:** {repos_com_releases} de {len(df)} ({repos_com_releases/len(df)*100:.1f}%)

**Resultado:** {"❌ Hipótese refutada" if releases_mediana == 0 else "✅ Hipótese confirmada"} - {"Muitos repositórios não usam o sistema de releases do GitHub" if releases_mediana == 0 else "Repositórios populares fazem releases regularmente"}.

### RQ04: Sistemas populares são atualizados com frequência?
**Métrica:** Tempo até a última atualização

"""
    
    # Calcular estatísticas para RQ04
    atualizacao_mediana = df['tempo_ate_ultima_atualizacao_dias'].median()
    atualizacao_media = df['tempo_ate_ultima_atualizacao_dias'].mean()
    repos_ativos = len(df[df['atividade_recente'] == 'Ativo'])
    
    report += f"""- **Mediana do tempo desde última atualização:** {atualizacao_mediana:.2f} dias
- **Média do tempo desde última atualização:** {atualizacao_media:.2f} dias
- **Repositórios ativos (últimos 30 dias):** {repos_ativos} de {len(df)} ({repos_ativos/len(df)*100:.1f}%)

**Resultado:** {"✅ Hipótese confirmada" if repos_ativos/len(df) > 0.5 else "❌ Hipótese refutada"} - {"A maioria dos repositórios é atualizada frequentemente" if repos_ativos/len(df) > 0.5 else "Nem todos os repositórios são atualizados frequentemente"}.

### RQ05: Sistemas populares são escritos nas linguagens mais populares?
**Métrica:** Linguagem primária

"""
    
    # Calcular estatísticas para RQ05
    linguagens_count = df['linguagem_primaria'].value_counts()
    
    report += "**Distribuição por linguagem:**\n"
    for linguagem, count in linguagens_count.items():
        report += f"- **{linguagem}:** {count} repositório(s) ({count/len(df)*100:.1f}%)\n"
    
    linguagens_mainstream = ['JavaScript', 'Python', 'TypeScript', 'Java', 'C++', 'C#']
    repos_mainstream = len(df[df['linguagem_primaria'].isin(linguagens_mainstream)])
    
    report += f"""
**Repositórios em linguagens mainstream:** {repos_mainstream} de {len(df)} ({repos_mainstream/len(df)*100:.1f}%)

**Resultado:** {"✅ Hipótese confirmada" if repos_mainstream/len(df) > 0.5 else "❌ Hipótese refutada"} - {"A maioria usa linguagens mainstream" if repos_mainstream/len(df) > 0.5 else "Há diversidade de linguagens"}.

### RQ06: Sistemas populares possuem um alto percentual de issues fechadas?
**Métrica:** Taxa de resolução de issues

"""
    
    # Calcular estatísticas para RQ06
    df_com_issues = df[df['total_issues'] > 0]
    if len(df_com_issues) > 0:
        taxa_mediana = df_com_issues['taxa_resolucao_issues_pct'].median()
        taxa_media = df_com_issues['taxa_resolucao_issues_pct'].mean()
        repos_alta_resolucao = len(df_com_issues[df_com_issues['taxa_resolucao_issues_pct'] > 80])
        
        report += f"""- **Mediana da taxa de resolução:** {taxa_mediana:.2f}%
- **Média da taxa de resolução:** {taxa_media:.2f}%
- **Repositórios com alta resolução (>80%):** {repos_alta_resolucao} de {len(df_com_issues)} ({repos_alta_resolucao/len(df_com_issues)*100:.1f}%)

**Resultado:** {"✅ Hipótese confirmada" if taxa_mediana > 80 else "❌ Hipótese refutada"} - {"Repositórios populares mantêm alta taxa de resolução" if taxa_mediana > 80 else "A taxa de resolução varia significativamente"}.

"""
    
    # Análise por linguagem (RQ07)
    report += """## 4. Análise por Linguagem (RQ07)

**Questão:** Sistemas escritos em linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizados com mais frequência?

"""
    
    # Estatísticas por linguagem
    for linguagem in df['linguagem_primaria'].unique():
        if linguagem == 'N/A' or df[df['linguagem_primaria'] == linguagem].empty:
            continue
            
        subset = df[df['linguagem_primaria'] == linguagem]
        report += f"""### {linguagem}
- **Número de repositórios:** {len(subset)}
- **PRs aceitas (mediana):** {subset['pull_requests_aceitas'].median():.0f}
- **Releases (mediana):** {subset['releases'].median():.0f}
- **Dias desde última atualização (mediana):** {subset['tempo_ate_ultima_atualizacao_dias'].median():.2f}

"""
    
    report += """## 5. Discussão

### Descobertas Principais:
1. **Maturidade:** Repositórios populares tendem a ser projetos estabelecidos há vários anos
2. **Contribuições:** Variam drasticamente, com alguns projetos recebendo dezenas de milhares de contribuições
3. **Releases:** Muitos projetos populares não utilizam o sistema formal de releases do GitHub
4. **Atualizações:** A frequência de atualizações varia, com alguns projetos muito ativos e outros menos
5. **Linguagens:** Há uma mistura de linguagens mainstream e especializadas
6. **Issues:** A maioria mantém boa taxa de resolução de issues


### Conclusões:
Os repositórios mais populares do GitHub apresentam características diversas, mas tendem a ser projetos maduros e bem mantidos, com boa gestão de issues e contribuições ativas da comunidade.

"""
    
    # Salvar relatório
    with open("relatorio_final.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("Relatório final gerado: relatorio_final.md")
    return report

if __name__ == "__main__":
    generate_research_report()
