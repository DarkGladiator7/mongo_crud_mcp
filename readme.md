# MCP MongoDB Multi-DB CRUD Project

This is a simple project demonstrating:
- Connecting to multiple MongoDB databases via MCP
- Performing CRUD operations (`Create`, `Read`, `Update`, `Delete`)
- Exposing APIs with FastAPI
- Interacting via a Streamlit dashboard

---

## 🛠 Tools & Libraries Used
- Python 3.10+
- MongoDB (database)
- FastAPI (REST API backend)
- Streamlit (frontend UI)
- Motor (async MongoDB driver)
- Pydantic (data validation)
- Uvicorn (server)

---

## ⚡ Setup

1. Install dependencies:
pip install -r requirements.txt

2. Start MongoDB.

3. Run FastAPI:
uvicorn app.main:app --reload

4. Run Streamlit:
streamlit run streamlit_app/dashboard.py
