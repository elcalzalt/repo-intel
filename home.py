import requests
from datetime import datetime, timedelta

# api_key = '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'

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
        # "Authorization": f"Bearer {api_key}" 
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    result = [
        {
            "name": repo["name"],
            "stars": repo["stargazers_count"],
            "description": repo["description"] or "",
            "link": repo["html_url"]
        }
        for repo in data.get("items", [])
    ]
    return result