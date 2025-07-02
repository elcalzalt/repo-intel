import sqlalchemy as db
from datetime import datetime, timedelta

class CacheDatabase:
    def __init__(self, db_path='sqlite:///cache.db'):
        self.engine = db.create_engine(db_path)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.define_tables()
        self.metadata.create_all(self.engine)

    def define_tables(self):
        self.summary_cache = db.Table(
            "summary_cache", self.metadata,
            db.Column("repo_name", db.String(100), primary_key=True),
            db.Column("response", db.String(10000)),
            db.Column("created_at", db.DateTime, default=db.func.now())
        )
        self.vulnerability_cache = db.Table(
            "vulnerability_cache", self.metadata,
            db.Column("repo_name", db.String(100), primary_key=True),
            db.Column("response", db.String(10000)),
            db.Column("created_at", db.DateTime, default=db.func.now()),
            db.Column("file_name", db.String(100))
        )

    def insert_data(self, table, data):
        self.connection.execute(table.insert(), data)

    def delete_entry(self, repo_name, table, file_path=None):
        if file_path is not None:
            stmt = db.delete(table).where(
                (table.c.repo_name == repo_name) & (table.c.file_name == file_path)
            )
        else:
            stmt = db.delete(table).where(table.c.repo_name == repo_name)
        self.connection.execute(stmt)

    def get_recent_cache(self, repo_name, table, file_path=None, max_age_seconds=60):
        if file_path is not None:
            query = db.select(table).where(
                (table.c.repo_name == repo_name) & (table.c.file_name == file_path)
            )
        else:
            query = db.select(table).where(table.c.repo_name == repo_name)
        result = self.connection.execute(query).fetchone()
        if result is None:
            return None, False, False
        response, created_at = result[1], result[2]
        now = datetime.utcnow()
        if (now - created_at).total_seconds() < max_age_seconds:
            return response, True, True
        else:
            return response, True, False