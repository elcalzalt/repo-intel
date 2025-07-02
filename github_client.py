import requests
import base64

class GitHubClient:
    def get_readme(self, url):
        endpoint = "/readme"
        response = requests.get(url + endpoint)

        readme_content = None
        if response.status_code == 200:
            readme_data = response.json()
            readme_content = base64.b64decode(readme_data['content'])
            readme_content = readme_content.decode('utf-8')
        else:
            print("Error:", response.status_code, response.content)

        return readme_content

    def get_latest_commit(self, url, default_branch):
        endpoint = f"/commits/{default_branch}"
        response = requests.get(url + endpoint)

        commit_message = None
        commit_patches = []
        if response.status_code == 200:
            commit_data = response.json()
            commit_message = commit_data['commit']['message']
            for file in commit_data['files']:
                commit_patches.append(file['patch'])
        else:
            print("Error:", response.status_code, response.content)

        if len(commit_patches) == 0:
            commit_patches = None

        return (commit_message, commit_patches)

    def get_open_issues(self, url, has_issues):
        if not has_issues:
            return None
        
        endpoint = "/issues?state=open&sort=created&direction=desc&per_page=5"
        response = requests.get(url + endpoint)

        open_issues = []
        if response.status_code == 200:
            open_issues_data = response.json()
            for issue in open_issues_data:
                open_issues.append((issue['title'], issue['body'], issue['created_at']))
        else:
            print("Error:", response.status_code, response.content)

        return open_issues

    def get_repo_info(self, repo):
        url = f"https://api.github.com/repos/{repo}"
        response = requests.get(url)

        if response.status_code != 200:
            print("Error:", response.status_code, response.content)
            return False

        repo_data = response.json()

        name = repo_data['full_name']

        desc = repo_data['description']

        readme = self.get_readme(url)

        default_branch = repo_data['default_branch']
        latest_commit = self.get_latest_commit(url, default_branch)

        has_issues = repo_data['has_issues']
        open_issues = self.get_open_issues(url, has_issues)

        return (name, desc, readme, latest_commit, open_issues)

    def get_file_contents(self, repo, file_path):
        url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
        response = requests.get(url)

        if response.status_code != 200:
            print("Error:", response.status_code, response.content)
            return False

        file_data = response.json()

        if type(file_data) is list:
            print("Error: Multiple files found at the specified path. Please specify a file path.")
            return False

        file_type = file_data['type']
        if file_type != 'file':
            print("Error: The specified path does not point to a file.")
            return False

        file_content = base64.b64decode(file_data['content'])
        file_content = file_content.decode('utf-8')

        return file_content