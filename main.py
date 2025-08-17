import requests
import json
import os
import time

GITHUB_TOKEN = None
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
    for i, repo_node in enumerate(data, 1):
            owner = repo_node['owner']['login']
            name = repo_node['name']
            
            
            variables = {"owner": owner, "name": name}
            details_result = run_graphql_query(query, variables)
            
            repo_details = details_result['data']['repository']
            all_repo_data.append(repo_details)

            time.sleep(1) 

    return all_repo_data

def get_repo_metrics():
    # função para analisar os repositorios e buscar métricas

def main():
    try:

        list_result = run_graphql_repo_query(GET_TOP_REPOS_LIST_QUERY)
        repo_nodes = list_result['data']['search']['nodes']
        print(f"Lista de {len(repo_nodes)} repositórios obtida com sucesso!\n")

        all_repo_data = get_repo_details(GET_REPO_DETAILS_QUERY, repo_node)
 


    except Exception as e:
        print(f"\nOcorreu um erro: {e}")

if __name__ == '__main__':
    main()