import requests
import base64

class GitHubClient:
    def get_readme(self, url):
        # Fetches and decodes the README content from the GitHub repository at the specified API URL endpoint.
        endpoint = "/readme"
        response = requests.get(url + endpoint)

        readme_content = None
        if response.status_code == 200:
            readme_data = response.json()
            readme_content = base64.b64decode(readme_data['content'])
            readme_content = readme_content.decode('utf-8')

        return readme_content

    def get_latest_commit(self, url, default_branch):
        # Retrieves the latest commit message and patch diffs from the default branch of the repository.
        endpoint = f"/commits/{default_branch}"
        response = requests.get(url + endpoint)

        commit_message = None
        commit_patches = []
        if response.status_code == 200:
            commit_data = response.json()
            commit_message = commit_data['commit']['message']
            for f in commit_data.get('files', []):
                patch = f.get('patch')
                if patch:
                    commit_patches.append(patch)

        if len(commit_patches) == 0:
            commit_patches = None

        return (commit_message, commit_patches)

    def get_open_issues(self, url, has_issues):
        # Returns a list of the most recent open issues (up to 5), each as a tuple of title, body, and creation date, if issues are enabled.
        if not has_issues:
            return None
        
        endpoint = "/issues?state=open&sort=created&direction=desc&per_page=5"
        response = requests.get(url + endpoint)

        open_issues = []
        if response.status_code == 200:
            open_issues_data = response.json()
            for issue in open_issues_data:
                open_issues.append((issue['title'], issue['body'], issue['created_at']))

        return open_issues

    def get_repo_info(self, repo):
        # Gathers repository metadata including full name, description, README, latest commit info, and open issues, returning them as a tuple.
        url = f"https://api.github.com/repos/{repo}"
        response = requests.get(url)

        if response.status_code != 200:
            return response.status_code

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
        # Fetches and decodes the contents of a specific file in the repository, or returns status code or False for directories.
        url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
        response = requests.get(url)

        if response.status_code != 200:
            return response.status_code

        file_data = response.json()

        if type(file_data) is list:
            return False

        file_type = file_data['type']
        if file_type != 'file':
            return False

        file_content = base64.b64decode(file_data['content'])
        file_content = file_content.decode('utf-8')

        return file_content
    
    def get_update_date(self, repo):
        # Retrieves and returns the last updated timestamp for the repository.
        url = f"https://api.github.com/repos/{repo}"
        response = requests.get(url)

        if response.status_code != 200:
            return response.status_code

        repo_data = response.json()

        return repo_data['updated_at']
    
    def get_directory(self, repo, path):
        # Retrieves and returns the directory contents in JSON format for the specified path in the repository.
        url = f"https://api.github.com/repos/{repo}/contents/{path}"
        response = requests.get(url)

        if response.status_code != 200:
            return response.status_code
        
        return response.json()