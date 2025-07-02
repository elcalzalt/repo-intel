from github_client import GitHubClient
from ai_analyzer import AIAnalyzer
from cache_db import CacheDatabase
from rich.console import Console
import os

# TO DO:
# 1) Allow for specific file scanning (vulnerability detection)

class RepoIntelClient:
    def __init__(self, ai_key):
        self.gh = GitHubClient()
        self.ai = AIAnalyzer(ai_key)
        self.db = CacheDatabase()
        self.console = Console()

    def main_menu(self):
        while True:
            choice = input(
                "1) Repo Summary\n\
2) Vulnerability Check\n\
3) Quit\n"
            )
            if choice == "1":
                self.summarize_repo()
            elif choice == "2":
                self.scan_file()
            else:
                break

    def summarize_repo(self):
        repo = input("Repo (owner/name): ")

        cache = self.db.get_recent_cache(repo, self.db.summary_cache)
        summary = cache[0]
        if cache[2] is False:

            contents = self.gh.get_repo_info(repo)

            if not contents:
                return

            summary = self.ai.summarize(contents)

            if cache[1]:
                self.db.delete_entry(repo, self.db.summary_cache)

            self.db.insert_data(self.db.summary_cache, {
                'repo_name': repo,
                'response': summary
            })
        self.console.print(f"\n{summary}\n")

    def scan_file(self):
        repo = input("Repo (owner/name): ")
        file_path = input("File path: ")

        cache = self.db.get_recent_cache(repo, self.db.vulnerability_cache, file_path)
        report = cache[0]
        if cache[2] is False:

            contents = self.gh.get_file_contents(repo, file_path)

            if not contents:
                return

            report = self.ai.scan_file(file_path, contents)

            if cache[1]:
                self.db.delete_entry(repo, self.db.vulnerability_cache, file_path)

            self.db.insert_data(self.db.vulnerability_cache, {
                'repo_name': repo,
                'file_name': file_path,
                'response': report
            })
        self.console.print(f"\n{report}\n")

client = RepoIntelClient(os.environ.get('GENAI_KEY'))
client.main_menu()