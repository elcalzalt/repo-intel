import requests
import base64

class GitHubClient:
    def get_repo(self, repo: str):
        url = "https://api.github.com/repos/" + repo
        response = requests.get(url)

        if response.status_code not in range(200, 300):
            print("Sorry, there was an error processing your request:", response.status_code)
            return False

        repo_data = response.json()
        desc = repo_data['description']

        url = url + "/readme"
        response = requests.get(url, headers={'Accept': 'application/vnd.github+json'})

        if response.status_code not in range(200, 300):
            return (desc, None)

        readme_data = response.json()
        readme_content = base64.b64decode(readme_data['content'])
        readme_content = readme_content.decode('utf-8')

        return (desc, readme_content)

