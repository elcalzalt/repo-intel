from github_client import GitHubClient
from ai_analyzer import AIAnalyzer
from cache_db import CacheDatabase
from user_manager import UserManager
from rich.markdown import Markdown
from rich.syntax   import Syntax
from rich.box      import DOUBLE, HEAVY
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.box import ROUNDED
from rich.text import Text

import os

class RepoIntelClient:
    def __init__(self, ai_key):
        self.gh = GitHubClient()
        self.ai = AIAnalyzer(ai_key)
        self.db = CacheDatabase()
        self.user_manager = UserManager()
        self.console = Console()

    def main_menu(self):
        while True:
            self.console.clear()
            
            if self.user_manager.is_logged_in():
                user_info = self.user_manager.get_current_user()
                user_text = Text(f"Logged in as: {user_info[1]}", style="green")
                self.console.print(user_text)
                self.console.print()
            
            table = Table(show_header=False, box=ROUNDED, expand=False)
            table.add_column(justify="center", style="bold cyan")
            table.add_column(justify="left", style="white")

            if self.user_manager.is_logged_in():
                table.add_row("1", "Repo Summary")
                table.add_row("2", "Vulnerability Check")
                table.add_row("3", "Search History")
                table.add_row("4", "Bookmarks")
                table.add_row("5", "Logout")
                table.add_row("6", "Quit")
                choices = ["1", "2", "3", "4", "5", "6"]
            else:
                table.add_row("1", "Repo Summary")
                table.add_row("2", "Vulnerability Check")
                table.add_row("3", "Login")
                table.add_row("4", "Create Account")
                table.add_row("5", "Quit")
                choices = ["1", "2", "3", "4", "5"]
            
            self.console.print(Panel(table, title="[bold green]Main Menu[/]", border_style="green"))

            choice = Prompt.ask(
                "[bold yellow]Select an option[/]",
                choices=choices
            )
            
            if self.user_manager.is_logged_in():
                if choice == "1":
                    self.summarize_repo()
                elif choice == "2":
                    self.scan_file()
                elif choice == "3":
                    self.show_search_history()
                elif choice == "4":
                    self.manage_bookmarks()
                elif choice == "5":
                    self.logout()
                else:
                    self.db.connection.close()
                    self.user_manager.connection.close()
                    self.console.print("[bold red]Goodbye!")
                    break
            else:
                if choice == "1":
                    self.summarize_repo()
                elif choice == "2":
                    self.scan_file()
                elif choice == "3":
                    self.login()
                elif choice == "4":
                    self.create_account()
                else:
                    self.db.connection.close()
                    self.user_manager.connection.close()
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

            if type(contents) is int:
                self.console.print(f"[bold red]Error {contents}:[/] Repository [underline]{repo}[/] not found.")
                Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to return to menu[/]")
                return
                

            summary = self.ai.summarize(contents)

            if cache[1]:
                self.db.delete_entry(repo, self.db.summary_cache)

            self.db.insert_data(self.db.summary_cache, {
                'repo_name': repo,
                'response': summary
            })

        if self.user_manager.is_logged_in():
            self.user_manager.add_to_search_history('summary', repo)

        panel = Panel(
            Markdown(summary),
            title=f"[bold green]Summary for [link=https://github.com/{repo}]{repo}[/][/]",
            border_style="bright_magenta",
            box=DOUBLE,
            padding=(1, 2)
        )
        self.console.print(panel)
        
        if self.user_manager.is_logged_in():
            choice = Prompt.ask(
                f"\n[dim]Press [bold yellow]Enter[/] to return to menu, [bold yellow]B[/] to bookmark[/]",
                choices=["", "b", "B"],
                default=""
            )
            if choice.lower() == "b":
                self.add_repo_bookmark(repo)
        else:
            Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to return to menu[/]")


    def scan_file(self):
        repo = Prompt.ask(
            "[bold cyan]Enter repository[/] [dim](e.g. owner/name)[/]"
        )
        file_path = Prompt.ask(
            "[bold cyan]Enter file path[/] [dim](e.g. path/to/file)[/]"
        )

        user_id = self.user_manager.current_user_id or 0
        cache = self.db.get_recent_cache(repo, self.db.vulnerability_cache, file_path)
        report = cache[0]
        if cache[2] is False:

            contents = self.gh.get_file_contents(repo, file_path)

            if type(contents) is int:
                self.console.print(f"[bold red]Error {contents}:[/] File [underline]{file_path}[/] not found in [link=https://github.com/{repo}]{repo}[/].")
                Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to return to menu[/]")
                return

            if contents is False:
                self.console.print(f"[bold red]Error:[/] File [underline]{file_path}[/] is not a regular file.")
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

        if self.user_manager.is_logged_in():
            self.user_manager.add_to_search_history('vulnerability', repo, file_path)

        panel = Panel(
            Markdown(report),
            title=f"[bold green]Vulnerability report for [underline]{file_path}[/] in [link=https://github.com/{repo}]{repo}[/][/]",
            border_style="bright_magenta",
            box=DOUBLE,
            padding=(1, 2)
        )
        self.console.print(panel)
        
        if self.user_manager.is_logged_in():
            choice = Prompt.ask(
                f"\n[dim]Press [bold yellow]Enter[/] to return to menu, [bold yellow]B[/] to bookmark[/]",
                choices=["", "b", "B"],
                default=""
            )
            if choice.lower() == "b":
                self.add_file_bookmark(repo, file_path)
        else:
            Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to return to menu[/]")

    def login(self):
        self.console.clear()
        self.console.print(Panel("[bold green]User Login[/]", border_style="green"))
        
        username = Prompt.ask("[bold cyan]Username[/]")
        password = Prompt.ask("[bold cyan]Password[/]", password=True)
        
        if self.user_manager.authenticate_user(username, password):
            self.console.print(f"[bold green]Welcome back, {username}![/]")
        else:
            self.console.print("[bold red]Invalid username or password.[/]")
        
        Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to continue[/]")

    def create_account(self):
        self.console.clear()
        self.console.print(Panel("[bold green]Create New Account[/]", border_style="green"))
        
        username = Prompt.ask("[bold cyan]Choose a username[/]")
        email = Prompt.ask("[bold cyan]Email address[/]")
        password = Prompt.ask("[bold cyan]Choose a password[/]", password=True)
        confirm_password = Prompt.ask("[bold cyan]Confirm password[/]", password=True)
        
        if password != confirm_password:
            self.console.print("[bold red]Passwords do not match.[/]")
            Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to continue[/]")
            return
        
        if self.user_manager.create_user(username, email, password):
            self.console.print(f"[bold green]Account created successfully! Welcome, {username}![/]")
            self.user_manager.authenticate_user(username, password)
        else:
            self.console.print("[bold red]Failed to create account. Username or email may already exist.[/]")
        
        Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to continue[/]")

    def logout(self):
        self.user_manager.logout()
        self.console.print("[bold yellow]You have been logged out.[/]")
        Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to continue[/]")

    def show_search_history(self):
        self.console.clear()
        history = self.user_manager.get_search_history()
        
        if not history:
            self.console.print("[bold yellow]No search history found.[/]")
            Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to return to menu[/]")
            return
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Type", style="green", width=12)
        table.add_column("Repository", style="blue", width=30)
        table.add_column("File", style="yellow", width=40)
        table.add_column("Date", style="dim", width=20)
        
        for entry in history:
            search_type = entry[2]
            repo_name = entry[3]
            file_path = entry[4] or "-"
            searched_at = entry[5].strftime("%Y-%m-%d %H:%M")
            table.add_row(search_type, repo_name, file_path, searched_at)
        
        panel = Panel(table, title="[bold green]Search History[/]", border_style="bright_magenta")
        self.console.print(panel)
        Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to return to menu[/]")

    def manage_bookmarks(self):
        while True:
            self.console.clear()
            bookmarks = self.user_manager.get_bookmarks()
            
            table = Table(show_header=False, box=ROUNDED, expand=False)
            table.add_column(justify="center", style="bold cyan")
            table.add_column(justify="left", style="white")
            table.add_row("1", "View Bookmarks")
            table.add_row("2", "Delete Bookmark")
            table.add_row("3", "Back to Main Menu")
            
            self.console.print(Panel(table, title="[bold green]Bookmark Management[/]", border_style="green"))
            
            choice = Prompt.ask(
                "[bold yellow]Select an option[/]",
                choices=["1", "2", "3"]
            )
            
            if choice == "1":
                self.view_bookmarks()
            elif choice == "2":
                self.delete_bookmark()
            else:
                break

    def view_bookmarks(self):
        self.console.clear()
        bookmarks = self.user_manager.get_bookmarks()
        
        if not bookmarks:
            self.console.print("[bold yellow]No bookmarks found.[/]")
            Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to continue[/]")
            return
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Type", style="green", width=8)
        table.add_column("Title", style="blue", width=30)
        table.add_column("Repository", style="yellow", width=25)
        table.add_column("File", style="magenta", width=30)
        table.add_column("Notes", style="dim", width=20)
        
        for bookmark in bookmarks:
            bookmark_id = str(bookmark[0])
            bookmark_type = bookmark[2]
            title = bookmark[5]
            repo_name = bookmark[3]
            file_path = bookmark[4] or "-"
            notes = bookmark[6][:20] + "..." if bookmark[6] and len(bookmark[6]) > 20 else bookmark[6] or ""
            
            table.add_row(bookmark_id, bookmark_type, title, repo_name, file_path, notes)
        
        panel = Panel(table, title="[bold green]Your Bookmarks[/]", border_style="bright_magenta")
        self.console.print(panel)
        Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to continue[/]")

    def delete_bookmark(self):
        bookmarks = self.user_manager.get_bookmarks()
        
        if not bookmarks:
            self.console.print("[bold yellow]No bookmarks to delete.[/]")
            Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to continue[/]")
            return
        
        self.view_bookmarks()
        
        try:
            bookmark_id = int(Prompt.ask("[bold cyan]Enter bookmark ID to delete (or 0 to cancel)[/]"))
            if bookmark_id == 0:
                return
            
            if self.user_manager.remove_bookmark(bookmark_id):
                self.console.print("[bold green]Bookmark deleted successfully![/]")
            else:
                self.console.print("[bold red]Failed to delete bookmark.[/]")
        except ValueError:
            self.console.print("[bold red]Invalid bookmark ID.[/]")
        
        Prompt.ask("\n[dim]Press [bold yellow]Enter[/] to continue[/]")

    def add_repo_bookmark(self, repo_name):
        title = Prompt.ask(f"[bold cyan]Title for bookmark[/] [dim](default: {repo_name})[/]", default=repo_name)
        notes = Prompt.ask("[bold cyan]Notes (optional)[/]", default="")
        
        if self.user_manager.add_bookmark('repo', repo_name, title=title, notes=notes):
            self.console.print("[bold green]Repository bookmarked successfully![/]")
        else:
            self.console.print("[bold red]Failed to bookmark repository (may already exist).[/]")

    def add_file_bookmark(self, repo_name, file_path):
        title = Prompt.ask(f"[bold cyan]Title for bookmark[/] [dim](default: {repo_name}/{file_path})[/]", 
                          default=f"{repo_name}/{file_path}")
        notes = Prompt.ask("[bold cyan]Notes (optional)[/]", default="")
        
        if self.user_manager.add_bookmark('file', repo_name, file_path, title, notes):
            self.console.print("[bold green]File bookmarked successfully![/]")
        else:
            self.console.print("[bold red]Failed to bookmark file (may already exist).[/]")
        

client = RepoIntelClient(os.environ.get('GENAI_KEY'))
client.main_menu()