import sqlite3
from datetime import datetime

class HistoryDatabase:
    def __init__(self, db_path='history.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()

    def connect(self):
        """Establish a connection to the SQLite database."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Create the history table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                method TEXT,
                url TEXT,
                headers TEXT,
                body TEXT,
                response_code INTEGER,
                response_body TEXT,
                timestamp DATETIME
            )
        ''')
        self.conn.commit()

    def add_entry(self, method, url, headers, body, response_code, response_body):
        """Add a new entry to the history table."""
        timestamp = datetime.now().isoformat()
        self.cursor.execute('''
            INSERT INTO history (method, url, headers, body, response_code, response_body, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (method, url, headers, body, response_code, response_body, timestamp))
        self.conn.commit()

    def get_all_entries(self):
        """Retrieve all entries from the history table."""
        self.cursor.execute('SELECT * FROM history ORDER BY timestamp DESC')
        return self.cursor.fetchall()

    def get_entry_by_id(self, entry_id):
        """Retrieve a specific entry by its ID."""
        self.cursor.execute('SELECT * FROM history WHERE id = ?', (entry_id,))
        return self.cursor.fetchone()

    def delete_entry(self, entry_id):
        """Delete a specific entry by its ID."""
        self.cursor.execute('DELETE FROM history WHERE id = ?', (entry_id,))
        self.conn.commit()

    def clear_history(self):
        """Clear all entries from the history table."""
        self.cursor.execute('DELETE FROM history')
        self.conn.commit()

    def search_history(self, keyword):
        """Search for entries containing the given keyword in URL or body."""
        self.cursor.execute('''
            SELECT * FROM history 
            WHERE url LIKE ? OR body LIKE ? OR response_body LIKE ?
            ORDER BY timestamp DESC
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Ensure the database connection is closed when the object is deleted."""
        self.close()

