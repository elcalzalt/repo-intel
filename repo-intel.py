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
2) Latest Commit Info\n\
3) Open Issues Info\n\
4) Quit\n"
            )
            if choice == "1":
                self.summarize_repo()
            elif choice == "2":
                print("choice 2")
            elif choice == "3":
                print("choice 3")
            else:
                break

    def summarize_repo(self):
        repo = input("Repo (owner/name): ")

        contents = self.gh.get_repo(repo)
        if not contents:
            return

        summary = self.ai.summarize_repo(contents)

        self.console.print(summary)

client = RepoIntelClient(os.environ.get('GENAI_KEY'))
client.main_menu()