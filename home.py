import requests, re
from datetime import datetime, timedelta

def getTrendy():
    from app import cache
    ch = cache.check_trendy()
    if ch[1] is True:
        return ch[0]
    
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
        "Accept": "application/vnd.github+json",
        'Authorization': 'Bearer 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'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    repos = [
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

    cache.insert_data(cache.trendy_cache, {
        "repo_list": repos
    })

    return repos

def clean_user_query(raw_query):
    cleaned = raw_query.strip()
    cleaned = re.sub(r'[\"\'\\;:{}\[\]]+', '', cleaned)
    return cleaned

def validate_filters(filters):
    valid = {}
    for key, value in filters.items():
        if isinstance(value, list):
            cleaned_list = [
                re.sub(r'[\"\'\\;:{}\[\]]+', '', v)
                for v in value
                if isinstance(v, str) and v.strip()
            ]
            if cleaned_list:
                valid[key] = cleaned_list
        elif isinstance(value, str) and value.strip():
            valid[key] = re.sub(r'[\"\'\\;:{}\[\]]+', '', value)
    return valid

def search(query, filters):
    query = clean_user_query(query)
    filters = validate_filters(filters)

    parts = [query] if query else []

    for key, value in filters.items():
        if key in {"created", "pushed"}:
            parts.append(f"{key}:>={value}")
        elif key == "in":
            if isinstance(value, list):
                for item in value:
                    parts.append(f"in:{item}")
            else:
                parts.append(f"in:{value}")
        elif key in {"user", "org", "license", "language", "topic", "archived", "mirror", "size", "stars", "forks"}:
            parts.append(f"{key}:{value}")

    final_query = " ".join(parts)
    print("Final GitHub query:", final_query)

    url = "https://api.github.com/search/repositories"
    params = {
        "q": final_query,
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