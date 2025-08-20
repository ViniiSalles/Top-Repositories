import requests
import time
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

GITHUB_TOKEN = os.getenv("TOKEN")
GITHUB_API_URL = 'https://api.github.com/graphql'

GET_TOP_REPOS_LIST_QUERY = """
query GetTopRepos {
  search(query: "is:public sort:stars-desc", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        owner {
          login
        }
        name
      }
    }
  }
}
"""

GET_REPO_DETAILS_QUERY = """
query GetRepoDetails($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    nameWithOwner
    createdAt
    pushedAt
    primaryLanguage {
      name
    }
    releases {
      totalCount
    }
    pullRequests(states: MERGED) {
      totalCount
    }
    totalIssues: issues {
      totalCount
    }
    closedIssues: issues(states: CLOSED) {
      totalCount
    }
  }
}
"""

def run_graphql_repo_query(query, variables=None):
    if not GITHUB_TOKEN:
        raise Exception("Token do GitHub não encontrado. Configure a variável de ambiente GITHUB_TOKEN.")

    headers = {
        'Authorization': f'bearer {GITHUB_TOKEN}',
        'Content-Type': 'application/json',
    }
    
    request_body = {'query': query, 'variables': variables or {}}
    
    response = requests.post(GITHUB_API_URL, headers=headers, json=request_body, timeout=30)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query falhou com o código {response.status_code}:\n{response.text}")
    
def get_repo_details(query, data):
  all_repo_data = []
  total_repos = len(data)
  
  for i, repo_node in enumerate(data, 1):
    owner = repo_node['owner']['login']
    name = repo_node['name']
    
    variables = {"owner": owner, "name": name}
    details_result = run_graphql_repo_query(query, variables)
    
    repo_details = details_result['data']['repository']
    all_repo_data.append(repo_details)
    
    # Indicador de progresso
    progress = (i / total_repos) * 100
    print(f"\rCarregando {progress:.1f}%", end='', flush=True)

    time.sleep(0.05)
  
  print()  # Nova linha após completar
  return all_repo_data

def get_repo_metrics(repo_data):
  
  # Criar DataFrame a partir dos dados dos repositórios
  df_data = []
  for repo in repo_data:
    # Converter strings ISO para timestamp
    created_at = datetime.fromisoformat(repo['createdAt'].replace('Z', '+00:00')).timestamp()
    pushed_at = datetime.fromisoformat(repo['pushedAt'].replace('Z', '+00:00')).timestamp()
    
    # Calcular métricas individuais para cada repositório
    idade_repositorio = (time.time() - created_at) / (60 * 60 * 24)  # em dias
    tempo_ate_ultima_atualizacao = (time.time() - pushed_at) / (60 * 60 * 24)  # em dias
    pull_requests_aceitas = repo['pullRequests']['totalCount']
    releases = repo['releases']['totalCount']
    issues_fechadas = repo['closedIssues']['totalCount']
    total_issues = repo['totalIssues']['totalCount']
    taxa_resolucao_issues = (issues_fechadas / total_issues * 100) if total_issues > 0 else 0
    
    df_data.append({
      'nameWithOwner': repo['nameWithOwner'],
      'idade_repositorio_dias': round(idade_repositorio, 2),
      'pull_requests_aceitas': pull_requests_aceitas,
      'releases': releases,
      'tempo_ate_ultima_atualizacao_dias': round(tempo_ate_ultima_atualizacao, 2),
      'linguagem_primaria': repo['primaryLanguage']['name'] if repo['primaryLanguage'] else 'N/A',
      'issues_fechadas': issues_fechadas,
      'total_issues': total_issues,
      'taxa_resolucao_issues_pct': round(taxa_resolucao_issues, 2),
      'atividade_recente': 'Ativo' if tempo_ate_ultima_atualizacao <= 30 else 'Inativo',
      'maturidade': 'Maduro' if idade_repositorio > 365 else 'Jovem'
    })

  # Criar DataFrame e salvar em CSV
  df = pd.DataFrame(df_data)
  df.to_csv("repo_metrics.csv", index=False)
  
  return df

def get_df_metrics():
    df = pd.read_csv("repo_metrics.csv")

    # Calcular métricas usando pandas
    issues_fechadas_por_total = df['issues_fechadas'].sum() / df['total_issues'].sum() if df['total_issues'].sum() > 0 else 0

    return {
      "idade_repositorio": f"{df['idade_repositorio_dias'].mean():.2f} Dias",
      "total_pull_requests_aceitas": f"{df['pull_requests_aceitas'].mean():.2f}",
      "total_releases": f"{df['releases'].mean():.2f}",
      "tempo_ate_ultima_atualizacao": f"{df['tempo_ate_ultima_atualizacao_dias'].mean():.2f} Dias",
      "linguagem_primaria": df['linguagem_primaria'].mode().iloc[0] if not df['linguagem_primaria'].mode().empty else 'N/A',
      "issues_fechadas": f"{df['issues_fechadas'].sum()}",
      "total_issues": f"{df['total_issues'].sum()}",
      "issues_fechadas_por_total": f"{issues_fechadas_por_total:.2f}%",
      "taxa_resolucao_media": f"{df['taxa_resolucao_issues_pct'].mean():.2f}%",
      "repos_ativos": f"{len(df[df['atividade_recente'] == 'Ativo'])} de {len(df)}",
      "repos_maduros": f"{len(df[df['maturidade'] == 'Maduro'])} de {len(df)}"
    }

def metrics_analysis():
    """Análise detalhada para responder às questões de pesquisa"""
    df = pd.read_csv("repo_metrics.csv")
    
    print("="*80)
    print("ANÁLISE DAS QUESTÕES DE PESQUISA")
    print("="*80)
    
    # RQ01: Sistemas populares são maduros/antigos?
    print("\nRQ01: Sistemas populares são maduros/antigos?")
    print("-" * 50)
    idade_mediana = df['idade_repositorio_dias'].median()
    idade_media = df['idade_repositorio_dias'].mean()
    print(f"Mediana da idade: {idade_mediana:.2f} dias ({idade_mediana/365:.2f} anos)")
    print(f"Média da idade: {idade_media:.2f} dias ({idade_media/365:.2f} anos)")
    print(f"Repositórios maduros (>1 ano): {len(df[df['maturidade'] == 'Maduro'])} de {len(df)}")
    
    # RQ02: Sistemas populares recebem muita contribuição externa?
    print("\nRQ02: Sistemas populares recebem muita contribuição externa?")
    print("-" * 50)
    prs_mediana = df['pull_requests_aceitas'].median()
    prs_media = df['pull_requests_aceitas'].mean()
    print(f"Mediana de PRs aceitas: {prs_mediana:.0f}")
    print(f"Média de PRs aceitas: {prs_media:.2f}")
    
    # RQ03: Sistemas populares lançam releases com frequência?
    print("\nRQ03: Sistemas populares lançam releases com frequência?")
    print("-" * 50)
    releases_mediana = df['releases'].median()
    releases_media = df['releases'].mean()
    print(f"Mediana de releases: {releases_mediana:.0f}")
    print(f"Média de releases: {releases_media:.2f}")
    repos_com_releases = len(df[df['releases'] > 0])
    print(f"Repositórios com releases: {repos_com_releases} de {len(df)} ({repos_com_releases/len(df)*100:.1f}%)")
    
    # RQ04: Sistemas populares são atualizados com frequência?
    print("\nRQ04: Sistemas populares são atualizados com frequência?")
    print("-" * 50)
    atualizacao_mediana = df['tempo_ate_ultima_atualizacao_dias'].median()
    atualizacao_media = df['tempo_ate_ultima_atualizacao_dias'].mean()
    print(f"Mediana do tempo desde última atualização: {atualizacao_mediana:.2f} dias")
    print(f"Média do tempo desde última atualização: {atualizacao_media:.2f} dias")
    print(f"Repositórios ativos (atualizados nos últimos 30 dias): {len(df[df['atividade_recente'] == 'Ativo'])} de {len(df)}")
    
    # RQ05: Sistemas populares são escritos nas linguagens mais populares?
    print("\nRQ05: Sistemas populares são escritos nas linguagens mais populares?")
    print("-" * 50)
    linguagens_count = df['linguagem_primaria'].value_counts()
    print("Contagem por linguagem:")
    for linguagem, count in linguagens_count.items():
        print(f"  {linguagem}: {count} repositório(s) ({count/len(df)*100:.1f}%)")
    
    # RQ06: Sistemas populares possuem um alto percentual de issues fechadas?
    print("\nRQ06: Sistemas populares possuem um alto percentual de issues fechadas?")
    print("-" * 50)

    # Filtrar repositórios que têm issues (evitar divisão por zero)
    df_com_issues = df[df['total_issues'] > 0]
    if len(df_com_issues) > 0:
        taxa_mediana = df_com_issues['taxa_resolucao_issues_pct'].median()
        taxa_media = df_com_issues['taxa_resolucao_issues_pct'].mean()
        print(f"Mediana da taxa de resolução: {taxa_mediana:.2f}%")
        print(f"Média da taxa de resolução: {taxa_media:.2f}%")
        print(f"Repositórios com alta resolução (>80%): {len(df_com_issues[df_com_issues['taxa_resolucao_issues_pct'] > 80])} de {len(df_com_issues)}")
    else:
        print("Nenhum repositório com issues encontrado.")
    
    return df

def per_language_analysis():
    """Análise bônus: RQ07 - Análise por linguagem"""
    df = pd.read_csv("repo_metrics.csv")
    
    print("\n" + "="*80)
    print("RQ07: ANÁLISE POR LINGUAGEM (BÔNUS)")
    print("="*80)
    
    print("\nEstatísticas por linguagem:")
    print("-" * 50)
    
    for linguagem in df['linguagem_primaria'].unique():
        if linguagem == 'N/A' or pd.isna(linguagem):
            continue
            
        subset = df[df['linguagem_primaria'] == linguagem]
        linguagem_safe = str(linguagem) if linguagem is not None else 'Unknown'
        print(f"\n{linguagem_safe.upper()}:")
        print(f"  Número de repositórios: {len(subset)}")
        print(f"  PRs aceitas - Mediana: {subset['pull_requests_aceitas'].median():.0f}, Média: {subset['pull_requests_aceitas'].mean():.2f}")
        print(f"  Releases - Mediana: {subset['releases'].median():.0f}, Média: {subset['releases'].mean():.2f}")
        print(f"  Dias desde última atualização - Mediana: {subset['tempo_ate_ultima_atualizacao_dias'].median():.2f}, Média: {subset['tempo_ate_ultima_atualizacao_dias'].mean():.2f}")
    
    print(f"\nAnálise por linguagem concluída!")
    
    return df

def main():
    
    if not os.path.exists("repo_metrics.csv"):
      try:
          # Obter lista de repositórios
          list_result = run_graphql_repo_query(GET_TOP_REPOS_LIST_QUERY)
          repo_nodes = list_result['data']['search']['nodes']
          print(f"Lista de {len(repo_nodes)} repositórios obtida com sucesso!\n")

          # Obter detalhes dos repositórios
          repo_data = get_repo_details(GET_REPO_DETAILS_QUERY, repo_nodes)
          print("\nDetalhes dos repositórios obtidos com sucesso!\n")

          # Obter métricas dos repositórios
          get_repo_metrics_result = get_repo_metrics(repo_data)
          print("\nDataFrame com métricas dos repositórios criado com sucesso!\n")
          print(get_repo_metrics_result.head())

      except Exception as e:
          print(f"\nOcorreu um erro: {e}")
    
    # Análise básica
    df_metrics = get_df_metrics()
    print("\nMétricas dos repositórios obtidas com sucesso a partir do CSV!\n")
    for key, value in df_metrics.items():
        print(f"{key}: {value}")
    
    # Análise detalhada das questões de pesquisa
    metrics_analysis()
    
    # Análise bônus por linguagem
    per_language_analysis()
    
    print("\n" + "="*80)
    print("ANÁLISE COMPLETA FINALIZADA!")
    print("Arquivos gerados:")
    print("- repo_metrics.csv: Dados detalhados de cada repositório")
    print("- relatorio_final.md: Relatório completo da análise")
    print("="*80)

if __name__ == '__main__':
    main()