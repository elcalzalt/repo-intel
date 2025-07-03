from github_client import GitHubClient
from ai_analyzer import AIAnalyzer
from cache_db import CacheDatabase
from rich.markdown import Markdown
from rich.syntax   import Syntax
from rich.box      import DOUBLE, HEAVY
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.box import ROUNDED


import os

class RepoIntelClient:
    def __init__(self, ai_key):
        self.gh = GitHubClient()
        self.ai = AIAnalyzer(ai_key)
        self.db = CacheDatabase()
        self.console = Console()

    def main_menu(self):
        while True:
            self.console.clear()
            table = Table(show_header=False, box=ROUNDED, expand=False)
            table.add_column(justify="center", style="bold cyan")
            table.add_column(justify="left", style="white")
            table.add_row("1", "Repo Summary")
            table.add_row("2", "Vulnerability Check")
            table.add_row("3", "Quit")
            self.console.print(Panel(table, title="[bold green]Main Menu[/]", border_style="green"))

            choice = Prompt.ask(
                "[bold yellow]Select an option[/]",
                choices=["1", "2", "3"]
            )
            if choice == "1":
                self.summarize_repo()
            elif choice == "2":
                self.scan_file()
            else:
                self.console.print("[bold red]Goodbye!")
                break

    def summarize_repo(self):
        repo = Prompt.ask(
            "[bold cyan]Enter repository[/] [dim](e.g. owner/name)[/]"
        )

        cache = self.db.get_recent_cache(repo, self.db.summary_cache)
        summary = cache[0]
        if cache[2] is False:

            contents = self.gh.get_repo_info(repo)

            if not contents:
                self.console.print(f"[bold red]Error:[/] Repository [underline]{repo}[/] not found.")
                Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to return to menu[/]")
                return
                

            summary = self.ai.summarize(contents)

            if cache[1]:
                self.db.delete_entry(repo, self.db.summary_cache)

            self.db.insert_data(self.db.summary_cache, {
                'repo_name': repo,
                'response': summary
            })

        panel = Panel(
            Markdown(summary),
            title=f"[bold green]Summary for [link=https://github.com/{repo}]{repo}[/][/]",
            border_style="bright_magenta",
            box=DOUBLE,
            padding=(1, 2)
        )
        self.console.print(panel)
        Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to return to menu[/]")


    def scan_file(self):
        repo = Prompt.ask(
            "[bold cyan]Enter repository[/] [dim](e.g. owner/name)[/]"
        )
        file_path = Prompt.ask(
            "[bold cyan]Enter file path[/] [dim](e.g. path/to/file)[/]"
        )

        cache = self.db.get_recent_cache(repo, self.db.vulnerability_cache, file_path)
        report = cache[0]
        if cache[2] is False:

            contents = self.gh.get_file_contents(repo, file_path)

            if not contents:
                self.console.print(f"[bold red]Error:[/] File [underline]{file_path}[/] not found in [link=https://github.com/{repo}]{repo}[/].")
                Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to return to menu[/]")
                return

            report = self.ai.scan_file(file_path, contents)

            if cache[1]:
                self.db.delete_entry(repo, self.db.vulnerability_cache, file_path)

            self.db.insert_data(self.db.vulnerability_cache, {
                'repo_name': repo,
                'file_name': file_path,
                'response': report
            })

            panel = Panel(
                Markdown(report),
                title=f"[bold green]Vulnerability report for [underline]{file_path}[/] in [link=https://github.com/{repo}]{repo}[/][/]",
                border_style="bright_magenta",
                box=DOUBLE,
                padding=(1, 2)
            )
        self.console.print(panel)
        Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to return to menu[/]")
        

client = RepoIntelClient(os.environ.get('GENAI_KEY'))
client.main_menu()