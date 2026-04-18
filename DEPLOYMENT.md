# 🚀 Deployment Guide

## 1. Backend Deployment (Render)
*Deploy this first to get your API URL.*

### Step 1: Deploy to Render
1. Go to [Render](https://render.com) and click **"New"** → **"Web Service"**.
2. Connect your GitHub repository: `pashaarshad/RBAC_GP3`.
3. Configure the service:
   - **Name:** `rbac-backend`
   - **Start Command:** `python "week 5/src/main.py"`
   - **Build Command:** `pip install -r requirements.txt`
4. **Environment Variables (CRITICAL):**
   - Click "Advanced" → "Add Environment Variable":
     - `LLM_API_KEY`: (Your OpenRouter Key)
     - `LLM_BASE_URL`: `https://openrouter.ai/api/v1`
     - `LLM_MODEL`: `mistralai/mistral-7b-instruct`
5. Click **"Create Web Service"**.
6. **Wait for deployment** and copy your URL (e.g., `https://rbac-gp3.onrender.com`).

---

## 2. Frontend Deployment (Vercel)
*This matches your current screen.*

### Step 1: Fix Vercel Settings
Vercel might auto-detect "FastAPI" because of Python files in the root. **You must change this to Next.js manually.**

1. On the screen you are currently viewing:
2. **Root Directory:** Click "Edit" and change `./` to **`rbac-frontend`**.
3. **Framework Preset:** Ensure it is set to **Next.js**.
4. **Environment Variables:**
   - Expand the section and add:
     - **Key:** `NEXT_PUBLIC_API_URL`
     - **Value:** (The Render URL you copied earlier, e.g., `https://rbac-gp3.onrender.com`)
5. Click **"Deploy"**.

---

## 3. Post-Deployment (CORS)
Once Vercel gives you a URL (e.g., `https://rbac-frontend.vercel.app`), update the backend.

1. Open `week 5/src/main.py`.
2. Update `allow_origins`:
   ```python
   allow_origins=[
       "https://your-vercel-url.vercel.app",
       "http://localhost:3000"
   ]
   ```
3. Push the change to GitHub. Render will auto-redeploy.

---

## 🔑 Login Credentials
Use these updated emails for login:
- **Admin:** `arshad@rbac.com` / `admin123`
- **Finance:** `priyanshu@rbac.com` / `pass123`
- **HR:** `kanak@rbac.com` / `pass123`
- **Marketing:** `shirisha@rbac.com` / `pass123`

