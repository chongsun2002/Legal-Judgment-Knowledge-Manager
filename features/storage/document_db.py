import sqlite3
import os

class DocumentDatabase:
    _instance = None

    def __new__(cls, db_filename="document.db"):
        if cls._instance is None:
            cls._instance = super(DocumentDatabase, cls).__new__(cls)
            cls._instance._init(db_filename)
        return cls._instance

    def _init(self, db_filename):
        # Always store in a known folder relative to THIS FILE
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "..", "..", "data")
        os.makedirs(data_dir, exist_ok=True)

        self.db_path = os.path.join(data_dir, db_filename)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            case_name TEXT NOT NULL,
            year INTEGER,
            citation TEXT UNIQUE,
            parties TEXT,
            filename TEXT
        );
        """)
        self.conn.commit()

    def insert_document(self, id, case_name, year, citation, parties, filename):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO documents (id, case_name, year, citation, parties, filename)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (id, case_name, year, citation, parties, filename))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"Document already exists for citation: {citation}")

    def search_by_fields(self, filters: dict) -> list[dict]:
        cursor = self.conn.cursor()

        query = "SELECT * FROM documents"
        conditions = []
        params = []

        for field, value in filters.items():
            if field == "parties":
                if isinstance(value, list):
                    # Build OR conditions for each party
                    sub_conditions = []
                    for party in value:
                        sub_conditions.append("LOWER(parties) LIKE ?")
                        params.append(f"%{party.lower()}%")
                    conditions.append(f"({' OR '.join(sub_conditions)})")
                else:
                    conditions.append("LOWER(parties) LIKE ?")
                    params.append(f"%{value.lower()}%")
            else:
                conditions.append(f"{field} = ?")
                params.append(value)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_filenames_by_ids(self, ids: list[str]) -> list[str]:
        if not ids:
            return []

        cursor = self.conn.cursor()
        placeholders = ", ".join("?" for _ in ids)
        query = f"SELECT filename FROM documents WHERE id IN ({placeholders})"
        cursor.execute(query, ids)
        return [row["filename"] for row in cursor.fetchall()]

    def close(self):
        self.conn.close()