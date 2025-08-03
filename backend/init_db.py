#!/usr/bin/env python3
"""
Initialize and optimize SQLite database for local development
Includes Apple Silicon optimizations
"""

import sqlite3
import os
from datetime import datetime

def init_database():
    """Initialize database with optimized settings"""
    db_path = 'gct_data.db'
    
    # Remove old database if exists
    if os.path.exists(db_path):
        print(f"Backing up existing database to {db_path}.backup")
        os.rename(db_path, f"{db_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    # Create new database with optimizations
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable optimizations
    optimizations = [
        "PRAGMA journal_mode=WAL;",  # Write-Ahead Logging
        "PRAGMA synchronous=NORMAL;",  # Faster writes
        "PRAGMA cache_size=-64000;",  # 64MB cache
        "PRAGMA temp_store=MEMORY;",  # Use memory for temp tables
        "PRAGMA mmap_size=268435456;",  # 256MB memory-mapped I/O
        "PRAGMA page_size=4096;",  # Optimal page size for SSDs
        "PRAGMA auto_vacuum=INCREMENTAL;",  # Prevent DB bloat
    ]
    
    for opt in optimizations:
        cursor.execute(opt)
        print(f"Applied: {opt}")
    
    # Create tables (from GCTDatabase class schema)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            assessment_type TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            data TEXT NOT NULL,
            coherence_profile TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS communications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            text TEXT NOT NULL,
            analysis TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_a_id TEXT NOT NULL,
            user_b_id TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            compatibility_data TEXT NOT NULL
        )
    ''')
    
    # Create indexes for better query performance
    cursor.execute('CREATE INDEX idx_assessments_user_id ON assessments(user_id);')
    cursor.execute('CREATE INDEX idx_assessments_timestamp ON assessments(timestamp);')
    cursor.execute('CREATE INDEX idx_communications_user_id ON communications(user_id);')
    cursor.execute('CREATE INDEX idx_relationships_users ON relationships(user_a_id, user_b_id);')
    
    conn.commit()
    
    # Analyze tables for query optimizer
    cursor.execute('ANALYZE;')
    
    conn.close()
    
    print("\n✅ Database initialized successfully!")
    print(f"Location: {os.path.abspath(db_path)}")
    print("\nOptimizations applied:")
    print("- Write-Ahead Logging (WAL) for better concurrency")
    print("- 64MB cache for faster queries")
    print("- Memory-mapped I/O for M4 Max SSD performance")
    print("- Optimized indexes on frequently queried columns")

if __name__ == "__main__":
    init_database()