import requests

class GitHubClient:
    def __init__(self, token: str):
        self.gh = token

    def get_repo(self, repo: str):
        url = "https://api.github.com/repos/" + repo
        response = requests.get(url)

        if response.status_code not in range(200, 300):
            print("Sorry, there was an error processing your request:", response.status_code)
            return False

        repo_data = response.json()
        desc = repo_data['description']
        print(desc)

        return True

