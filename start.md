# 🚀 Getting Started

To run the RBAC Chatbot system, you need to start both the backend and the frontend.

### 1. Start the Backend (FastAPI)
Open a terminal in the root directory and run:
```powershell
python "week 5/src/main.py"
```
The backend will be available at `http://127.0.0.1:8000`.

### 2. Start the Frontend (Next.js)
Open a **new** terminal, navigate to the frontend directory, and run:
```powershell
cd rbac-frontend
npm run dev
```
The application will be available at `http://localhost:3000`.

---

**Note:** Ensure your `.env` file is properly configured with your LLM provider (Hugging Face or local Ollama) before starting.
