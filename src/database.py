import sqlite3
import json
import chromadb
from chromadb.utils import embedding_functions

DB_PATH = "jobs.db"
chroma_client = chromadb.PersistentClient(path="./chroma_db")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
vector_collection = chroma_client.get_or_create_collection(name="jobs", embedding_function=sentence_transformer_ef)

def init_db():
    # 1. Setup SQLite for Structured Data
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            title TEXT,
            salary INTEGER,
            location TEXT,
            is_remote BOOLEAN,
            description TEXT
        )
    ''')
    cursor.execute('DELETE FROM jobs') # Clear old data for PoC
    
    with open("data/jobs.json", "r") as f:
        jobs = json.load(f)
        
    for job in jobs:
        # Insert into SQLite
        cursor.execute('''
            INSERT INTO jobs (id, title, salary, location, is_remote, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (job['id'], job['title'], job['salary'], job['location'], job['is_remote'], job['description']))
        
        # 2. Insert into ChromaDB for Semantic Search
        vector_collection.add(
            documents=[job['description']],
            metadatas=[{"title": job['title'], "salary": job['salary'], "location": job['location']}],
            ids=[str(job['id'])]
        )
        
    conn.commit()
    conn.close()
    print("Database and Vector Store initialized.")

if __name__ == "__main__":
    init_db()