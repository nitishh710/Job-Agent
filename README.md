Conversational Job Agent:

![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi)
![Gemini API](https://img.shields.io/badge/Gemini_API-Function_Calling-orange?style=flat-square&logo=google)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Search-FF6F00?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)

An end-to-end LLM-powered agent designed to match users to jobs through natural language conversation. This Proof of Concept demonstrates **hybrid retrieval** by dynamically routing queries between exact-match SQL filtering and semantic vector search based on user intent.

## ✨ Core Features
* **LLM Tool Calling:** Utilizes the Gemini API with structured outputs to decide exactly when to query a database and which parameters to use.
* **Hybrid Retrieval System:** 
  * **SQL Database (`SQLite`):** Handles hard constraints (e.g., minimum salary, remote status, specific locations).
  * **Vector Database (`ChromaDB`):** Handles soft, unstructured concepts (e.g., "graph theory", "company culture", "large datasets") via semantic embeddings.
* **Automated Evaluations:** Includes a deterministic LLM evaluation pipeline to test routing accuracy and output quality.
* **Containerized:** Fully Dockerized for seamless cloud deployment.

---

## 🏗️ Repository Structure

```text
elip-job-agent/
├── data/
│   └── jobs.json           # Raw mock dataset for the PoC
├── src/
│   ├── __init__.py
│   ├── agent.py            # Gemini API integration and tool-calling logic
│   ├── database.py         # SQLite & ChromaDB initialization and population
│   ├── eval.py             # LLM evaluation test suite
│   ├── main.py             # FastAPI server configuration
│   └── tools.py            # Python functions exposed to the LLM (SQL & Vector)
├── .dockerignore
├── .gitignore
├── Dockerfile              # Production container build instructions
├── requirements.txt        
└── run.sh                  # Optional quick-start bash script
⚙️ Getting Started (Local Development)1. PrerequisitesEnsure you have Python 3.13+ installed. Set your Gemini API key as an environment variable:Bashexport GEMINI_API_KEY="your_api_key_here"
2. Install DependenciesBashpip install -r requirements.txt
3. Initialize DatabasesThis command reads data/jobs.json and generates the local jobs.db file and the chroma_db/ persistent vector directory.Bashpython3 -m src.database
4. Start the API ServerBashuvicorn src.main:app
The server will start on http://127.0.0.1:8000💬 API Usage & ExamplesSend POST requests to the /chat endpoint. The agent will automatically interpret the text, trigger the correct tool, and format a natural language response.Scenario A: Hard Constraints (Routes to SQL)Bashcurl -X POST "[http://127.0.0.1:8000/chat](http://127.0.0.1:8000/chat)" \
-H "Content-Type: application/json" \
-d '{"session_id": "user_1", "message": "Show me remote jobs paying over 70k"}'
Agent Action: Extracts min_salary=70000, is_remote=True $\rightarrow$ Executes filter_jobs_by_sql().Scenario B: Soft Constraints (Routes to Vector DB)Bashcurl -X POST "[http://127.0.0.1:8000/chat](http://127.0.0.1:8000/chat)" \
-H "Content-Type: application/json" \
-d '{"session_id": "user_1", "message": "Do you have any jobs involving graph theory?"}'
Agent Action: Recognizes unstructured requirement $\rightarrow$ Executes semantic_search_jobs("graph theory") using ChromaDB.🧪 LLM EvaluationsThis repository includes a deterministic evaluation script to assert that the LLM successfully maps specific prompts to the correct backend tool (SQL vs Vector) and retrieves the expected concepts.Bashpython3 -m src.eval
Output:PlaintextTest 1: Show me remote jobs paying over 70k (Target: SQL Filtering)
✅ PASS: Successfully retrieved Software Engineer Intern.

Test 2: Do you have any jobs involving graph theory? (Target: Semantic Search)
✅ PASS: Successfully retrieved Data Scientist.

Final Eval Score: 2/2
🐳 Docker DeploymentBuild and run the container locally to verify production readiness:Bashdocker build -t elip-job-agent .
docker run -p 8000:8000 -e GEMINI_API_KEY="your_api_key_here" elip-job-agent

Once you have replaced the contents of your `README.md` file, update your live GitHub repository by running these three commands in your terminal:

```bash
git add README.md
git commit -m "docs: upgrade README structure with badges and architecture"
git push -u origin main
