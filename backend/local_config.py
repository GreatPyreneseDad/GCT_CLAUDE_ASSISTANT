"""
Local Development Configuration
Optimized for Apple Silicon M4 Max performance
"""
import os
from pathlib import Path

class LocalConfig:
    # Base directory
    BASE_DIR = Path(__file__).parent
    
    # Database optimization for Apple Silicon
    DATABASE_URL = os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR}/gct_data.db')
    
    # SQLite optimizations for M4 Max
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'max_overflow': 40,
        'pool_pre_ping': True,
        'connect_args': {
            'check_same_thread': False,
            'timeout': 30,
            # Enable Write-Ahead Logging for better concurrency
            'isolation_level': None,
        }
    }
    
    # Flask configuration
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # CORS configuration for local development
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
    
    # Performance settings
    SEND_FILE_MAX_AGE_DEFAULT = 0  # Disable caching in development
    
    # Threading and process configuration
    THREADED = True
    PROCESSES = 1  # Use threading instead of processes for development
    
    @staticmethod
    def init_app(app):
        """Initialize app with local development settings"""
        # Enable SQLite optimizations
        if app.config['DATABASE_URL'].startswith('sqlite'):
            from sqlalchemy import event
            from sqlalchemy.engine import Engine
            
            @event.listens_for(Engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                # Enable Write-Ahead Logging
                cursor.execute("PRAGMA journal_mode=WAL")
                # Increase cache size (in KB, -64000 = 64MB)
                cursor.execute("PRAGMA cache_size=-64000")
                # Store temp tables in memory
                cursor.execute("PRAGMA temp_store=MEMORY")
                # Synchronous mode for better performance
                cursor.execute("PRAGMA synchronous=NORMAL")
                # Enable memory-mapped I/O (up to 256MB)
                cursor.execute("PRAGMA mmap_size=268435456")
                cursor.close()