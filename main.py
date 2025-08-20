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
  search(query: "is:public sort:stars-desc", type: REPOSITORY, first: 10) {
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
    
    df_data.append({
      'nameWithOwner': f"{repo['nameWithOwner']}",
      'idade_repositorio': f"{(time.time() - created_at) / (60 * 60 * 24):.2f}",  # em dias
      'pull_requests_aceitas': f"{repo['pullRequests']['totalCount']:.2f}",
      'releases': f"{repo['releases']['totalCount']:.2f}",
      'tempo_ate_ultima_atualizacao': f"{(time.time() - pushed_at) / (60 * 60 * 24):.2f}",  # em dias
      'linguagem_primaria': repo['primaryLanguage']['name'] if repo['primaryLanguage'] else 'N/A',
      'issues_fechadas': f"{repo['closedIssues']['totalCount']:.2f}",
      'total_issues': f"{repo['totalIssues']['totalCount']:.2f}"
    })

  df = pd.DataFrame(df_data)
  df.to_csv("repo_metrics.csv")

  # Calcular métricas usando pandas
  issues_fechadas_por_total = df['issues_fechadas'].sum() / df['total_issues'].sum() if df['total_issues'].sum() > 0 else 0

  return {
    "idade_repositorio": f"{df['idade_repositorio'].mean()}",
    "total_pull_requests_aceitas": f"{df['pull_requests_aceitas'].mean()}",
    "total_releases": f"{df['releases'].mean()}",
    "tempo_ate_ultima_atualizacao": f"{df['tempo_ate_ultima_atualizacao'].mean()}",
    "linguagem_primaria": df['linguagem_primaria'].mode().iloc[0] if not df['linguagem_primaria'].mode().empty else 'N/A',
    "issues_fechadas": f"{df['issues_fechadas'].sum()}",
    "total_issues": f"{df['total_issues'].sum()}",
    "issues_fechadas_por_total": f"{issues_fechadas_por_total}"
  }

def get_df_metrics():
    df = pd.read_csv("repo_metrics.csv")

    # Calcular métricas usando pandas
    issues_fechadas_por_total = df['issues_fechadas'].sum() / df['total_issues'].sum() if df['total_issues'].sum() > 0 else 0

    return {
      "idade_repositorio": f"{df['idade_repositorio'].mean()}",
      "total_pull_requests_aceitas": f"{df['pull_requests_aceitas'].mean()}",
      "total_releases": f"{df['releases'].mean()}",
      "tempo_ate_ultima_atualizacao": f"{df['tempo_ate_ultima_atualizacao'].mean()}",
      "linguagem_primaria": df['linguagem_primaria'].mode().iloc[0] if not df['linguagem_primaria'].mode().empty else 'N/A',
      "issues_fechadas": f"{df['issues_fechadas'].sum()}",
      "total_issues": f"{df['total_issues'].sum()}",
      "issues_fechadas_por_total": f"{issues_fechadas_por_total}"
    }

def main():
    
    if not os.path.exists("repo_metrics.csv"):
      try:

          list_result = run_graphql_repo_query(GET_TOP_REPOS_LIST_QUERY)
          repo_nodes = list_result['data']['search']['nodes']
          print(f"Lista de {len(repo_nodes)} repositórios obtida com sucesso!\n")

          repo_data = get_repo_details(GET_REPO_DETAILS_QUERY, repo_nodes)
          print("\nDetalhes dos repositórios obtidos com sucesso!\n")

          get_repo_metrics_result = get_repo_metrics(repo_data)
          print("\nMétricas dos repositórios obtidas com sucesso!\n")
          for key, value in get_repo_metrics_result.items():
              print(f"{key}: {value}")

      except Exception as e:
          print(f"\nOcorreu um erro: {e}")
    
    df_metrics = get_df_metrics()
    print("\nMétricas dos repositórios obtidas com sucesso a partir do CSV!\n")
    for key, value in df_metrics.items():
        print(f"{key}: {value}")

if __name__ == '__main__':
    main()