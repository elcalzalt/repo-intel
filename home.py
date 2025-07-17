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
            "name": repo["name"],
            "stars": repo["stargazers_count"],
            "description": repo["description"] or "",
            "url": repo["html_url"]
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
            "stars": repo["stargazers_count"],
            "description": repo["description"] or "",
            "url": repo["html_url"]
        }
        for repo in data.get("items", [])
    ]