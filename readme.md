# 🚀 MCP Mongo Multi-DB CRUD + LLM Agent  

This project is a **MongoDB CRUD dashboard with multi-database support**, powered by **FastAPI**, **Streamlit**, and an **LLM Agent (Groq LLaMA)**.  

It allows you to:  
- Connect to **multiple MongoDB databases**  
- Perform **CRUD operations** on users  
- Create databases dynamically  
- Either use the **Streamlit UI** to enter and manage data manually  
- Or interact with the system using **natural language instructions**, automatically translated into CRUD actions by the LLM  

---

## ⚙️ Tools & Technologies  

- **FastAPI** – Backend API for CRUD operations  
- **Motor (Async MongoDB Driver)** – Non-blocking DB access  
- **MongoDB** – Database  
- **Streamlit** – Frontend Dashboard  
- **Requests** – API communication  
- **Groq LLaMA API** – Natural language to structured action translation  
- **Python-dotenv** – Environment variable management  

---

## 📂 Project Structure  

```
app/
 ├── crud.py          # CRUD operations
 ├── database.py      # MongoDB connection
 ├── models.py        # Pydantic models
 ├── routes.py        # FastAPI routes
 ├── main.py          # FastAPI entrypoint
 └── cli_agent.py     # CLI agent for natural language → CRUD

agent/
 └── llm_setup.py     # LLM API setup

streamlit_app/
 └── dashboard.py     # Streamlit UI
```

---

## 🚀 Run Instructions  

1. **Install requirements**  
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables** in `.env`  
   ```env
   MONGO_URL=mongodb://localhost:27017
   GROQ_API_KEY=your_groq_api_key
   ```

3. **Start FastAPI backend**  
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Run Streamlit dashboard**  
   ```bash
   streamlit run streamlit_app/dashboard.py
   ```

5. **Optional: Run CLI LLM Agent**  
   ```bash
   python app/cli_agent.py
   ```

---


