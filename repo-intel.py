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

    def summarize_repo(self, repo):
        updated_at = self.gh.get_update_date(repo)

        if type(updated_at) is int:
            return updated_at

        cache = self.db.get_recent_cache(repo, self.db.summary_cache, updated_at)
        summary = cache[0]
        if cache[2] is False:

            contents = self.gh.get_repo_info(repo)

            if type(contents) is int:
                return contents

            summary = self.ai.summarize(contents)

            if cache[1]:
                self.db.delete_entry(repo, self.db.summary_cache)

            self.db.insert_data(self.db.summary_cache, {
                'repo_name': repo,
                'response': summary,
                'updated_at': updated_at
            })

        if self.user_manager.is_logged_in():
            self.user_manager.add_to_search_history('Summary', repo)

        return summary
    
    def get_file_tree(self, repo, path=""):
        return self.gh.get_directory(repo, path)

    def scan_file(self, repo, file_path):
        updated_at = self.gh.get_update_date(repo)

        if type(updated_at) is int:
            return updated_at
        
        cache = self.db.get_recent_cache(repo, self.db.vulnerability_cache, updated_at, file_path)
        report = cache[0]
        if cache[2] is False:

            contents = self.gh.get_file_contents(repo, file_path)

            if type(contents) is int:
                return contents

            report = self.ai.scan_file(file_path, contents)

            if cache[1]:
                self.db.delete_entry(repo, self.db.vulnerability_cache, file_path)

            self.db.insert_data(self.db.vulnerability_cache, {
                'repo_name': repo,
                'file_name': file_path,
                'response': report,
                'updated_at': updated_at
            })

        if self.user_manager.is_logged_in():
            self.user_manager.add_to_search_history('Scan', repo, file_path)

        return report

    def login(self, username, password):
        if self.user_manager.authenticate_user(username, password):
            return True
        else:
            return False

    def create_account(self, username, email, password):
        if self.user_manager.create_user(username, email, password):
            self.user_manager.authenticate_user(username, password)
            return True
        else:
            return False

    def logout(self):
        self.user_manager.logout()

    def show_search_history(self):
        return self.user_manager.get_search_history()

    def view_bookmarks(self):
        bookmarks = self.user_manager.get_bookmarks()
        
        return bookmarks

    def delete_bookmark(self, bookmark_id):
        if self.user_manager.remove_bookmark(bookmark_id):
            return True
        else:
            return False

    def add_repo_bookmark(self, repo):
        if self.user_manager.add_bookmark(repo):
            return True
        else:
            return False

client = RepoIntelClient(os.environ.get('GENAI_KEY'))