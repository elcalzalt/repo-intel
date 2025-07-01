import requests
import base64

class GitHubClient:
    def get_readme(url):
        endpoint = "/readme"
        response = requests.get(url + endpoint, headers={'Accept': 'application/vnd.github+json'})

        readme_content = None
        if response.status_code == 200:
            readme_data = response.json()
            readme_content = base64.b64decode(readme_data['content'])
            readme_content = readme_content.decode('utf-8')
        else:
            print("Error:", response.status_code, response.content)

        return readme_content

    def get_latest_commit(url, default_branch):
        endpoint = f"/commits/{default_branch}"
        response = requests.get(url + endpoint, headers={'Accept': 'application/vnd.github+json'})

        commit_message = None
        commit_patch = None
        if response.status_code == 200:
            commit_data = response.json()
            commit_message = commit_data['message']
            commit_patch = commit_data['patch']
        else:
            print("Error:", response.status_code, response.content)

        return (commit_message, commit_patch)

    def get_open_issues():
        test = None

    def get_repo_info(self, repo: str):
        url = f"https://api.github.com/repos/{repo}"
        response = requests.get(url)

        if response.status_code != 200:
            print("Error:", response.status_code, response.content)
            return False

        repo_data = response.json()
        desc = repo_data['description']

        readme = get_readme(url)

        return (desc, readme_content)