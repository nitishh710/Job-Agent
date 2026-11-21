import sqlite3
from src.database import DB_PATH, vector_collection

def filter_jobs_by_sql(min_salary: int = 0, location: str = None, is_remote: bool = None) -> str:
    """
    Use this tool when the user asks for hard constraints like salary minimums, specific locations, or remote work.
    """
    print(f"\n[AGENT EXECUTING SQL] salary >= {min_salary}, loc={location}, remote={is_remote}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT title, salary, location, is_remote FROM jobs WHERE salary >= ?"
    params = [min_salary]
    
    if location:
        query += " AND location = ?"
        params.append(location)
    if is_remote is not None:
        query += " AND is_remote = ?"
        params.append(is_remote)
        
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return "No jobs found matching those exact criteria."
    
    return "\n".join([f"- {r[0]} ({r[2]}), Salary: {r[1]}, Remote: {r[3]}" for r in results])

def semantic_search_jobs(search_query: str) -> str:
    """
    Use this tool when the user asks for soft concepts, company culture, specific technologies, or job descriptions.
    """
    print(f"\n[AGENT EXECUTING VECTOR SEARCH] query='{search_query}'")
    
    results = vector_collection.query(
        query_texts=[search_query],
        n_results=2
    )
    
    if not results['documents'][0]:
        return "No semantic matches found."
        
    formatted = []
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        formatted.append(f"- {meta['title']} ({meta['location']}): {doc}")
        
    return "\n".join(formatted)

agent_tools = [filter_jobs_by_sql, semantic_search_jobs]