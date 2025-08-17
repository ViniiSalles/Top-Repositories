import requests
import os

TOKEN = "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"
URL = "https://api.github.com/graphql"

def get_top_repositories():
    data = {"query": """query {
  __type(name: "Repository") {
    name
    kind
    description
    fields {
      name
    }
  }
}"""}

    response = requests.post(URL, json=data, headers={"Authorization": f"Bearer {TOKEN}"})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
    

def main():
    repositorios = get_top_repositories()
    print(repositorios)


if __name__ == "__main__":
    main()