from github_client import GitHubClient
from ai_analyzer import AIAnalyzer
from rich.console import Console
import os

# TO DO:
# 1) Merge commit info and issue info into summary
# 2) Allow for specific file scanning (vulnerability detection)

class RepoIntelClient:
    def __init__(self, ai_key):
        self.gh = GitHubClient()
        self.ai = AIAnalyzer(ai_key)
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
                print("choice 2")
            else:
                break

    def summarize_repo(self):
        repo = input("Repo (owner/name): ")

        contents = self.gh.get_repo_info(repo)
        if not contents:
            return

        summary = self.ai.summarize(contents)

        self.console.print(f"\n{summary}\n")

client = RepoIntelClient(os.environ.get('GENAI_KEY'))
client.main_menu()