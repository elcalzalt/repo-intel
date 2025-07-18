import sqlalchemy as db
import hashlib
import secrets
from datetime import datetime
from typing import Optional, List, Tuple, Any
from github_client import GitHubClient
from ai_analyzer import AIAnalyzer
import os

class UserManager:
    def __init__(self, cache, db_path='sqlite:///users.db'):
        self.engine = db.create_engine(db_path)
        self.metadata = db.MetaData()
        self.define_tables()
        self.metadata.create_all(self.engine)
        self.current_user_id = None
        self.current_username = None
        self.gh = GitHubClient()
        genai_key = os.environ.get('GENAI_KEY', '')
        self.ai = AIAnalyzer(genai_key)
        self.db = cache

    def define_tables(self):
        self.users = db.Table(
            "users", self.metadata,
            db.Column("id", db.Integer, primary_key=True, autoincrement=True),
            db.Column("username", db.String(50), unique=True, nullable=False),
            db.Column("email", db.String(100), unique=True, nullable=False),
            db.Column("password_hash", db.String(128), nullable=False),
            db.Column("salt", db.String(32), nullable=False),
            db.Column("created_at", db.DateTime, default=db.func.now()),
            db.Column("last_login", db.DateTime)
        )

        self.search_history = db.Table(
            "search_history", self.metadata,
            db.Column("id", db.Integer, primary_key=True, autoincrement=True),
            db.Column("user_id", db.Integer, db.ForeignKey("users.id"), nullable=False),
            db.Column("search_type", db.String(20), nullable=False),
            db.Column("repo_name", db.String(100), nullable=False),
            db.Column("file_path", db.String(200)),
            db.Column("searched_at", db.DateTime, default=db.func.now())
        )

        self.bookmarks = db.Table(
            "bookmarks", self.metadata,
            db.Column("id", db.Integer, primary_key=True, autoincrement=True),
            db.Column("user_id", db.Integer, db.ForeignKey("users.id"), nullable=False),
            db.Column("repo_name", db.String(100), nullable=False),
            db.Column("created_at", db.DateTime, default=db.func.now())
        )

    def _hash_password(self, password: str, salt: str) -> str:
        """Hash a password with salt using SHA-256"""
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def _generate_salt(self) -> str:
        """Generate a random salt"""
        return secrets.token_hex(16)

    def create_user(self, username: str, email: str, password: str) -> bool:
        """Create a new user account"""
        try:
            with self.engine.begin() as conn:
                existing_user = conn.execute(
                    db.select(self.users).where(
                        (self.users.c.username == username) | (self.users.c.email == email)
                    )
                ).fetchone()
                
                if existing_user:
                    return False
                
                salt = self._generate_salt()
                password_hash = self._hash_password(password, salt)
                
                conn.execute(self.users.insert(), {
                    'username': username,
                    'email': email,
                    'password_hash': password_hash,
                    'salt': salt
                })
                
                return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user and set current session"""
        try:
            with self.engine.begin() as conn:
                user = conn.execute(
                    db.select(self.users).where(self.users.c.username == username)
                ).fetchone()
                
                if not user:
                    return False
                
                stored_hash = user[3]
                salt = user[4]
                provided_hash = self._hash_password(password, salt)
                
                if stored_hash == provided_hash:
                    self.current_user_id = user[0]
                    self.current_username = user[1]
                    
                    conn.execute(
                        self.users.update().where(self.users.c.id == self.current_user_id).values(
                            last_login=datetime.utcnow()
                        )
                    )
                    return True
                
                return False
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return False

    def logout(self):
        """Clear current user session"""
        self.current_user_id = None
        self.current_username = None

    def is_logged_in(self) -> bool:
        """Check if a user is currently logged in"""
        return self.current_user_id is not None

    def get_current_user(self) -> Optional[Tuple[int, str]]:
        """Get current user info (id, username)"""
        if self.is_logged_in():
            return (self.current_user_id, self.current_username)
        return None

    def add_to_search_history(self, search_type: str, repo_name: str, file_path: Optional[str] = None):
        """Add a search to user's history"""
        if not self.is_logged_in():
            return False
        
        try:
            with self.engine.begin() as conn:
                conn.execute(self.search_history.insert(), {
                    'user_id': self.current_user_id,
                    'search_type': search_type,
                    'repo_name': repo_name,
                    'file_path': file_path
                })
                return True
        except Exception as e:
            print(f"Error adding to search history: {e}")
            return False

    def get_search_history(self, limit: int = 20) -> List[Any]:
        """Get user's search history"""
        if not self.is_logged_in():
            return []
        
        try:
            with self.engine.begin() as conn:
                query = db.select(self.search_history).where(
                    self.search_history.c.user_id == self.current_user_id
                ).order_by(self.search_history.c.searched_at.desc()).limit(limit)
                
                results = conn.execute(query).fetchall()
                return list(results)
        except Exception as e:
            print(f"Error getting search history: {e}")
            return []

    def add_bookmark(self, repo_name: str) -> bool:
        """Add a bookmark for the user"""
        if not self.is_logged_in():
            return False
        
        try:
            with self.engine.begin() as conn:
                query = db.select(self.bookmarks).where(
                    (self.bookmarks.c.user_id == self.current_user_id) &
                    (self.bookmarks.c.repo_name == repo_name)
                )
                existing = conn.execute(query).fetchone()
                
                if existing:
                    return False
                
                conn.execute(self.bookmarks.insert(), {
                    'user_id': self.current_user_id,
                    'repo_name': repo_name
                })
                return True
        except Exception as e:
            print(f"Error adding bookmark: {e}")
            return False

    def remove_bookmark(self, bookmark_id: int) -> bool:
        """Remove a bookmark"""
        if not self.is_logged_in():
            return False
        
        try:
            with self.engine.begin() as conn:
                query = db.select(self.bookmarks).where(
                    (self.bookmarks.c.user_id == self.current_user_id) &
                    (self.bookmarks.c.id == bookmark_id)
                )
                existing = conn.execute(query).fetchone()
                
                if existing:
                    stmt = db.delete(self.bookmarks).where(
                        (self.bookmarks.c.id == bookmark_id) &
                        (self.bookmarks.c.user_id == self.current_user_id)
                    )
                    conn.execute(stmt)
                    return True
                return False
        except Exception as e:
            print(f"Error removing bookmark: {e}")
            return False

    def get_bookmarks(self) -> List[Any]:
        """Get user's bookmarks"""
        if not self.is_logged_in():
            return []
        
        try:
            with self.engine.begin() as conn:
                query = db.select(self.bookmarks).where(
                    self.bookmarks.c.user_id == self.current_user_id
                ).order_by(self.bookmarks.c.created_at.desc())
                
                results = conn.execute(query).fetchall()
                return list(results)
        except Exception as e:
            print(f"Error getting bookmarks: {e}")
            return []

    def update_bookmark(self, bookmark_id: int, title: Optional[str] = None, notes: Optional[str] = None) -> bool:
        """Update bookmark title and/or notes"""
        if not self.is_logged_in():
            return False
        
        try:
            with self.engine.begin() as conn:
                update_data = {}
                if title is not None:
                    update_data['title'] = title
                if notes is not None:
                    update_data['notes'] = notes
                
                if not update_data:
                    return False
                
                stmt = self.bookmarks.update().where(
                    (self.bookmarks.c.id == bookmark_id) &
                    (self.bookmarks.c.user_id == self.current_user_id)
                ).values(**update_data)
                
                conn.execute(stmt)
                return True
        except Exception as e:
            print(f"Error updating bookmark: {e}")
            return False

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

        if self.is_logged_in():
            self.add_to_search_history('Summary', repo)

        return summary
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

        if self.is_logged_in():
            self.add_to_search_history('Scan', repo, file_path)

        return report
    
    def get_file_tree(self, repo, path=""):
        return self.gh.get_directory(repo, path)
    
    def get_user_info(self) -> Optional[dict]:
        if not self.is_logged_in():
            return None
        try:
            with self.engine.begin() as conn:
                query = db.select(self.users).where(self.users.c.id == self.current_user_id)
                user = conn.execute(query).fetchone()
                if user:
                    return {
                        'id': user[0],
                        'username': user[1],
                        'email': user[2],
                        'created_at': user[5],
                        'last_login': user[6]
                    }
        except Exception as e:
            print(f"Error fetching user info: {e}")
        
        return None