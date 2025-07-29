import sqlalchemy as db
from datetime import datetime, timedelta

class CacheDatabase:
    def __init__(self, db_path='sqlite:///cache.db'):
        # Initialize the database engine at the given path
        # Establish a connection and prepare metadata registry
        # Define tables and create them if they do not exist
        self.engine = db.create_engine(db_path)
        self.metadata = db.MetaData()
        self.define_tables()
        self.metadata.create_all(self.engine)

    def define_tables(self):
        # Define the summary_cache table for storing repository summaries
        # Columns: repo_name (PK), response text, updated timestamp
        self.summary_cache = db.Table(
            "summary_cache", self.metadata,
            db.Column("repo_name", db.String(100), primary_key=True),
            db.Column("response", db.String(10000)),
            db.Column("updated_at", db.String(20))
        )
        # Define the vulnerability_cache table for storing file-level data
        # Columns: repo_name, response text, updated timestamp, file_name, full_path (PK)
        self.vulnerability_cache = db.Table(
            "vulnerability_cache", self.metadata,
            db.Column("repo_name", db.String(100)),
            db.Column("response", db.String(10000)),
            db.Column("updated_at", db.String(20)),
            db.Column("file_name", db.String(100)),
            db.Column("full_path", db.String(40), primary_key=True)
        )

    def insert_data(self, table, data):
        # Insert the provided data dictionary into the specified table
        try:
            with self.engine.begin() as conn:
                conn.execute(table.insert(), data)
                return True
        except Exception:
            return False

        self.connection.execute(table.insert(), data)

    def delete_entry(self, repo_name, table, file_path=None):
        if file_path is not None:
            stmt = db.delete(table).where(
                (table.c.repo_name == repo_name) & (table.c.file_name == file_path)
            )
        else:
            stmt = db.delete(table).where(table.c.repo_name == repo_name)
        # Execute the delete statement to remove matching cache entries
        try:
            with self.engine.begin() as conn:
                conn.execute(stmt)
                return True
        except Exception:
            return False

    def get_recent_cache(self, repo_name, table, updated_at, file_path=None):
        # Build a select query filtering by repo_name and optional file_path
        if file_path is not None:
            query = db.select(table).where(
                (table.c.repo_name == repo_name) & (table.c.file_name == file_path)
            )
        else:
            query = db.select(table).where(table.c.repo_name == repo_name)
        # Execute the query and fetch the first result (or None)
        try:
            with self.engine.begin() as conn:
                result = conn.execute(query).fetchone()
        except Exception:
            result = None
        # If no entry is found, return (None, found=False, fresh=False)
        if result is None:
            return None, False, False
        response, prev_updated_at = result[1], result[2]
        # Compare timestamps to determine if the cache is up-to-date
        if prev_updated_at == updated_at:
            # Entry matches requested timestamp: found and fresh
            return response, True, True
        else:
            # Entry exists but is stale compared to requested timestamp
            return response, True, False