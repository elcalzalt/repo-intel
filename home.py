import requests
from datetime import datetime, timedelta

def getTrendy():
    six_months_ago = (datetime.now() - timedelta(days=183)).strftime('%Y-%m-%d')
    query = f"created:>{six_months_ago}"
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 20
    }

    headers = {
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return [
        {
            "name": repo["full_name"],
            "description": repo["description"],
            "url": repo["html_url"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "updated_at": repo["updated_at"]
        }
        for repo in data.get("items", [])
    ]

def search(query):
    query += "~"
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "order": "desc",
        "per_page": 20
    }
    headers = {
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return [
        {
            "name": repo["full_name"],
            "description": repo["description"],
            "url": repo["html_url"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "updated_at": repo["updated_at"]
        }
        for repo in data.get("items", [])
    ]