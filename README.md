# Enterprise RBAC Chatbot

A secure internal chatbot system with Role-Based Access Control (RBAC) and Retrieval-Augmented Generation (RAG).

---

## 🌐 Live Demo & Delivery Instructions

### Important Links (Add these to GitHub "About" section)
- **Frontend (UI):** [https://rbac-infosys-internship.vercel.app/login](https://rbac-infosys-internship.vercel.app/login)
- **Backend (API):** [https://rbac-gp3.onrender.com/](https://rbac-gp3.onrender.com/)

### How to Access the Live App Effectively:
> **⚠️ Render Free Tier Notice:** The backend API is hosted on Render's free tier, which goes to sleep after 15 minutes of inactivity. **It may take 1-2 minutes to wake up** on the first request.

1. **Wake up the Backend:** First, click the [Backend Link](https://rbac-gp3.onrender.com/) and wait until you see `{"status": "ok", "message": "RBAC Secured API is running smoothly!"}` on the screen.
2. **Open the Frontend:** Once the backend is awake, open the [Frontend Link](https://rbac-infosys-internship.vercel.app/login).
3. **Log In:** Use the Quick Demo Access buttons or type in the credentials listed below to test different roles. The presentation can be accessed via the "Detailed Info" button on the login page!

---

## 👥 The RBAC Group 3 Team
**Led by Arshad Pasha | 8 Active Members**

| Role | Name | Contact | Status |
| :--- | :--- | :--- | :--- |
| 👑 **Team Leader** | **Arshad Pasha** | [arshadpashaintern@gmail.com](mailto:arshadpashaintern@gmail.com) | ✅ Active |
| 👨‍💻 Member | **Depuru Joshika Reddy** | [joshikareddy07@gmail.com](mailto:joshikareddy07@gmail.com) | ✅ Active |
| 👨‍💻 Member | **Guru Karthik Reddy Marthala** | [marthalagurukarthikreddy11@gmail.com](mailto:marthalagurukarthikreddy11@gmail.com) | ✅ Active |
| 👩‍💻 Member | **Kavya Ghantasala** | [vtu24677@veltech.edu.in](mailto:vtu24677@veltech.edu.in) | ✅ Active |
| 👨‍💻 Member | **Kushagra Bhargava** | [kushagra.23bai10987@vitbhopal.ac.in](mailto:kushagra.23bai10987@vitbhopal.ac.in) | ✅ Active |
| 👩‍💻 Member | **Mandha Shirisha** | [mandhashirisha90@gmail.com](mailto:mandhashirisha90@gmail.com) | ✅ Active |
| 👩‍💻 Member | **Sri Saranya Chandrapati** | [srnya0986@gmail.com](mailto:srnya0986@gmail.com) | ✅ Active |
| 👩‍💻 Member | **Vinuthna Jangam** | [vinuthnaaj@gmail.com](mailto:vinuthnaaj@gmail.com) | ✅ Active |

---

## 🚀 Setup & Installation

1.  **Clone / Folder Setup**:
    Ensure you are in the root directory `rbac-system`.

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Data Processing (Week 1 & 2)**:
    Parse documents and assign metadata roles.
    ```bash
    python "week 2/src/chunking.py"
    python "week 2/src/parse_markdown.py"
    python "week 2/src/parse_csv.py"
    python "week 2/src/text_cleaning.py"
    python "week 2/src/metadata_tagging.py"
    ```

4.  **Vector DB (Week 3)**:
    Generate embeddings and index them.
    ```bash
    python "week 3/src/embeddings.py"
    python "week 3/src/index_embeddings.py"
    ```

5.  **Run Backend (Week 5)**:
    Start the FastAPI server.
    ```bash
    python "week 5/src/main.py"
    ```
    API will run at `http://127.0.0.1:8000`.
    Docs at `http://127.0.0.1:8000/docs`.

## 🤖 Local LLM Setup (Ollama)

This project uses **Ollama** to run a local LLM for AI-powered responses. No API key needed!

### Step 1: Install Ollama

**Windows:**
1. Download from: https://ollama.com/download
2. Run the installer (`OllamaSetup.exe`)
3. Restart your terminal after installation

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 2: Download the Model

Open a terminal and run:
```bash
ollama pull llama3.2:3b
```

This downloads the **Llama 3.2 3B** model (~2GB). Other recommended models:
- `llama3.2:1b` - Smaller, faster (~1.3GB)
- `phi3:mini` - Microsoft's efficient model (~2.3GB)
- `mistral:7b` - More powerful but larger (~4GB)

### Step 3: Start Ollama Server

Ollama usually runs automatically as a service. To verify:
```bash
ollama list
```

### Step 4: Configure the Application

Create/update `.env` file in the project root:
```env
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=llama3.2:3b
```

### Step 5: Start the Application

```bash
# Terminal 1: Backend
python "week 5/src/main.py"

# Terminal 2: Frontend
cd rbac-frontend
npm run dev
```

### Troubleshooting

- **Ollama not found**: Restart your terminal or add Ollama to PATH
- **Model not loading**: Run `ollama serve` manually
- **Slow responses**: Try a smaller model like `llama3.2:1b`

## 🧪 Testing

- **RBAC Tests**: `python "week 4/tests/rbac_tests.py"`
- **Search Benchmark**: `python "week 4/tests/benchmark.py"`

## 👤 Default Users (Seeded)

| Username | Password | Role | Access |
|---|---|---|---|
| `arshad@rbac.com` | `admin123` | `c-level` | All Departments |
| `priyanshu@rbac.com` | `pass123` | `finance` | Finance + General |
| `kanak@rbac.com` | `pass123` | `hr` | HR + General |
| `shirisha@rbac.com` | `pass123` | `marketing` | Marketing + General |
| `eng_user@rbac.com` | `pass123` | `engineering` | Engineering + General |
| `employee@rbac.com` | `pass123` | `employees` | General Only |

## 🏗 Architecture
- **Preprocessing**: LangChain + TikToken
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Vector DB**: ChromaDB
- **Backend**: FastAPI + SQLite + JWT
- **RBAC**: Custom Middleware + Metadata Filtering
