"""
Database connection handlers for multiple database types
"""
from typing import Optional, Dict, Any, List
from sqlalchemy import create_engine, inspect, MetaData, Table, text
from sqlalchemy.engine import Engine
from pymongo import MongoClient
import aiosqlite
import json
from config import settings


class DatabaseConnection:
    """Base class for database connections"""
    
    def __init__(self):
        self.engine: Optional[Engine] = None
        self.client: Optional[Any] = None
        self.connection_string: Optional[str] = None
    
    def connect(self) -> bool:
        """Establish database connection"""
        raise NotImplementedError
    
    def disconnect(self):
        """Close database connection"""
        raise NotImplementedError
    
    def get_tables(self) -> List[str]:
        """Get list of table/collection names"""
        raise NotImplementedError
    
    def get_schema(self, table_name: str) -> Dict[str, Any]:
        """Get schema for a specific table/collection"""
        raise NotImplementedError


class MySQLConnection(DatabaseConnection):
    """MySQL database connection"""
    
    def connect(self) -> bool:
        try:
            self.connection_string = (
                f"mysql+pymysql://{settings.db_user}:{settings.db_password}"
                f"@{settings.db_host}:{settings.db_port or 3306}/{settings.db_name}"
            )
            self.engine = create_engine(self.connection_string, echo=False)
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"MySQL connection error: {e}")
            return False
    
    def disconnect(self):
        if self.engine:
            self.engine.dispose()
    
    def get_tables(self) -> List[str]:
        if not self.engine:
            return []
        inspector = inspect(self.engine)
        return inspector.get_table_names()
    
    def get_schema(self, table_name: str) -> Dict[str, Any]:
        if not self.engine:
            return {}
        inspector = inspect(self.engine)
        columns = inspector.get_columns(table_name)
        pk_constraint = inspector.get_pk_constraint(table_name)
        primary_keys = pk_constraint.get("constrained_columns", []) if pk_constraint else []
        foreign_keys = inspector.get_foreign_keys(table_name)
        
        schema = {
            "table_name": table_name,
            "columns": {},
            "primary_keys": primary_keys,
            "foreign_keys": [
                {
                    "constrained_columns": fk["constrained_columns"],
                    "referred_table": fk["referred_table"],
                    "referred_columns": fk["referred_columns"]
                }
                for fk in foreign_keys
            ]
        }
        
        for col in columns:
            schema["columns"][col["name"]] = {
                "type": str(col["type"]),
                "nullable": col["nullable"],
                "default": col.get("default"),
                "primary_key": col["name"] in primary_keys
            }
        
        return schema


class PostgreSQLConnection(DatabaseConnection):
    """PostgreSQL database connection"""
    
    def connect(self) -> bool:
        try:
            self.connection_string = (
                f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}"
                f"@{settings.db_host}:{settings.db_port or 5432}/{settings.db_name}"
            )
            self.engine = create_engine(self.connection_string, echo=False)
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"PostgreSQL connection error: {e}")
            return False
    
    def disconnect(self):
        if self.engine:
            self.engine.dispose()
    
    def get_tables(self) -> List[str]:
        if not self.engine:
            return []
        inspector = inspect(self.engine)
        return inspector.get_table_names()
    
    def get_schema(self, table_name: str) -> Dict[str, Any]:
        if not self.engine:
            return {}
        inspector = inspect(self.engine)
        columns = inspector.get_columns(table_name)
        pk_constraint = inspector.get_pk_constraint(table_name)
        primary_keys = pk_constraint.get("constrained_columns", []) if pk_constraint else []
        foreign_keys = inspector.get_foreign_keys(table_name)
        
        schema = {
            "table_name": table_name,
            "columns": {},
            "primary_keys": primary_keys,
            "foreign_keys": [
                {
                    "constrained_columns": fk["constrained_columns"],
                    "referred_table": fk["referred_table"],
                    "referred_columns": fk["referred_columns"]
                }
                for fk in foreign_keys
            ]
        }
        
        for col in columns:
            schema["columns"][col["name"]] = {
                "type": str(col["type"]),
                "nullable": col["nullable"],
                "default": col.get("default"),
                "primary_key": col["name"] in primary_keys
            }
        
        return schema


class SQLiteConnection(DatabaseConnection):
    """SQLite database connection"""
    
    def connect(self) -> bool:
        try:
            db_path = settings.sqlite_path or settings.db_name or "database.db"
            self.connection_string = f"sqlite:///{db_path}"
            self.engine = create_engine(self.connection_string, echo=False)
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"SQLite connection error: {e}")
            return False
    
    def disconnect(self):
        if self.engine:
            self.engine.dispose()
    
    def get_tables(self) -> List[str]:
        if not self.engine:
            return []
        inspector = inspect(self.engine)
        return inspector.get_table_names()
    
    def get_schema(self, table_name: str) -> Dict[str, Any]:
        if not self.engine:
            return {}
        inspector = inspect(self.engine)
        columns = inspector.get_columns(table_name)
        pk_constraint = inspector.get_pk_constraint(table_name)
        primary_keys = pk_constraint.get("constrained_columns", []) if pk_constraint else []
        foreign_keys = inspector.get_foreign_keys(table_name)
        
        schema = {
            "table_name": table_name,
            "columns": {},
            "primary_keys": primary_keys,
            "foreign_keys": [
                {
                    "constrained_columns": fk["constrained_columns"],
                    "referred_table": fk["referred_table"],
                    "referred_columns": fk["referred_columns"]
                }
                for fk in foreign_keys
            ]
        }
        
        for col in columns:
            schema["columns"][col["name"]] = {
                "type": str(col["type"]),
                "nullable": col["nullable"],
                "default": col.get("default"),
                "primary_key": col["name"] in primary_keys
            }
        
        return schema


class MongoDBConnection(DatabaseConnection):
    """MongoDB database connection"""
    
    def connect(self) -> bool:
        try:
            if settings.db_uri:
                self.connection_string = settings.db_uri
            else:
                # Handle authentication if provided
                if settings.db_user and settings.db_password:
                    self.connection_string = (
                        f"mongodb://{settings.db_user}:{settings.db_password}"
                        f"@{settings.db_host or 'localhost'}:{settings.db_port or 27017}/{settings.db_name}"
                    )
                else:
                    # No authentication
                    self.connection_string = (
                        f"mongodb://{settings.db_host or 'localhost'}:{settings.db_port or 27017}/{settings.db_name}"
                    )
            self.client = MongoClient(self.connection_string)
            # Test connection
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            return False
    
    def disconnect(self):
        if self.client:
            self.client.close()
    
    def get_tables(self) -> List[str]:
        if not self.client:
            return []
        db = self.client[settings.db_name]
        return db.list_collection_names()
    
    def get_schema(self, collection_name: str) -> Dict[str, Any]:
        """Infer schema from MongoDB collection sample documents"""
        if not self.client:
            return {}
        
        db = self.client[settings.db_name]
        collection = db[collection_name]
        
        # Sample documents to infer schema
        sample_docs = list(collection.find().limit(100))
        
        schema = {
            "collection_name": collection_name,
            "columns": {},
            "primary_keys": ["_id"],  # MongoDB always has _id
            "foreign_keys": []
        }
        
        # Infer schema from sample documents
        if sample_docs:
            for doc in sample_docs:
                for key, value in doc.items():
                    if key not in schema["columns"]:
                        schema["columns"][key] = {
                            "type": type(value).__name__,
                            "nullable": True,
                            "default": None,
                            "primary_key": key == "_id"
                        }
        
        return schema


def get_database_connection() -> Optional[DatabaseConnection]:
    """Factory function to get appropriate database connection"""
    db_type = settings.db_type or ""
    db_type = db_type.lower()
    
    if db_type == "mysql":
        return MySQLConnection()
    elif db_type == "postgresql" or db_type == "postgres":
        return PostgreSQLConnection()
    elif db_type == "sqlite":
        return SQLiteConnection()
    elif db_type == "mongodb" or db_type == "mongo":
        return MongoDBConnection()
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

