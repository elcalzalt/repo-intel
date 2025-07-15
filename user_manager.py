import sqlalchemy as db
import hashlib
import secrets
from datetime import datetime
from typing import Optional, List, Tuple

class UserManager:
    def __init__(self, db_path='sqlite:///users.db'):
        self.engine = db.create_engine(db_path)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.define_tables()
        self.metadata.create_all(self.engine)
        self.current_user_id = None
        self.current_username = None

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
            db.Column("bookmark_type", db.String(20), nullable=False),
            db.Column("repo_name", db.String(100), nullable=False),
            db.Column("file_path", db.String(200)),
            db.Column("title", db.String(200)),
            db.Column("notes", db.String(1000)),
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
            existing_user = self.connection.execute(
                db.select(self.users).where(
                    (self.users.c.username == username) | (self.users.c.email == email)
                )
            ).fetchone()
            
            if existing_user:
                return False
            
            salt = self._generate_salt()
            password_hash = self._hash_password(password, salt)
            
            self.connection.execute(self.users.insert(), {
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'salt': salt
            })
            
            return True
        except Exception:
            return False

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user and set current session"""
        try:
            user = self.connection.execute(
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
                
                self.connection.execute(
                    self.users.update().where(self.users.c.id == self.current_user_id).values(
                        last_login=datetime.utcnow()
                    )
                )
                return True
            
            return False
        except Exception:
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

    def add_to_search_history(self, search_type: str, repo_name: str, file_path: str = None):
        """Add a search to user's history"""
        if not self.is_logged_in():
            return False
        
        try:
            self.connection.execute(self.search_history.insert(), {
                'user_id': self.current_user_id,
                'search_type': search_type,
                'repo_name': repo_name,
                'file_path': file_path
            })
            return True
        except Exception:
            return False

    def get_search_history(self, limit: int = 20) -> List[Tuple]:
        """Get user's search history"""
        if not self.is_logged_in():
            return []
        
        try:
            query = db.select(self.search_history).where(
                self.search_history.c.user_id == self.current_user_id
            ).order_by(self.search_history.c.searched_at.desc()).limit(limit)
            
            results = self.connection.execute(query).fetchall()
            return results
        except Exception:
            return []

    def add_bookmark(self, bookmark_type: str, repo_name: str, file_path: str = None, 
                    title: str = None, notes: str = None) -> bool:
        """Add a bookmark for the user"""
        if not self.is_logged_in():
            return False
        
        try:
            query = db.select(self.bookmarks).where(
                (self.bookmarks.c.user_id == self.current_user_id) &
                (self.bookmarks.c.repo_name == repo_name) &
                (self.bookmarks.c.file_path == file_path)
            )
            existing = self.connection.execute(query).fetchone()
            
            if existing:
                return False
            
            self.connection.execute(self.bookmarks.insert(), {
                'user_id': self.current_user_id,
                'bookmark_type': bookmark_type,
                'repo_name': repo_name,
                'file_path': file_path,
                'title': title or (f"{repo_name}/{file_path}" if file_path else repo_name),
                'notes': notes
            })
            return True
        except Exception:
            return False

    def remove_bookmark(self, bookmark_id: int) -> bool:
        """Remove a bookmark"""
        if not self.is_logged_in():
            return False
        
        try:
            query = db.select(self.bookmarks).where(
                (self.bookmarks.c.user_id == self.current_user_id) &
                (self.bookmarks.c.id == bookmark_id)
            )
            existing = self.connection.execute(query).fetchone()
            
            if existing:
                stmt = db.delete(self.bookmarks).where(
                    (self.bookmarks.c.id == bookmark_id) &
                    (self.bookmarks.c.user_id == self.current_user_id)
                )
                self.connection.execute(stmt)
                return True
            return False
        except Exception:
            return False

    def get_bookmarks(self) -> List[Tuple]:
        """Get user's bookmarks"""
        if not self.is_logged_in():
            return []
        
        try:
            query = db.select(self.bookmarks).where(
                self.bookmarks.c.user_id == self.current_user_id
            ).order_by(self.bookmarks.c.created_at.desc())
            
            results = self.connection.execute(query).fetchall()
            return results
        except Exception:
            return []

    def update_bookmark(self, bookmark_id: int, title: str = None, notes: str = None) -> bool:
        """Update bookmark title and/or notes"""
        if not self.is_logged_in():
            return False
        
        try:
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
            
            self.connection.execute(stmt)
            return True
        except Exception:
            return False
