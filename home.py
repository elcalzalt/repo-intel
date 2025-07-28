import requests, re
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

def clean_user_query(raw_query):
    cleaned = raw_query.strip()
    cleaned = re.sub(r'[\"\'\\;:{}\[\]]+', '', cleaned)
    return cleaned

def validate_filters(filters):
    valid = {}
    for key, value in filters.items():
        if not value:
            continue
        if key in {"created", "pushed"}:
            if re.match(r"\d{4}-\d{2}-\d{2}", value):
                valid[key] = value
        elif key == "stars":
            if re.match(r"^(\d+\.\.\d+|[<>]=?\d+|\d+)$", value):
                valid[key] = value
        else:
            valid[key] = re.sub(r'[\"\'\\;:{}\[\]]+', '', value)
    return valid

def search(query, filters):
    query = clean_user_query(query)
    filters = validate_filters(filters)

    if filters:
        parts = [query]
        for key, value in filters.items():
            if key in {"created", "pushed"}:
                parts.append(f"{key}:>={value}")
            else:
                parts.append(f"{key}:{value}")
        query = "+".join(parts) + '~'

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