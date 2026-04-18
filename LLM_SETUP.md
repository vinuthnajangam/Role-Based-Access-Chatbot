# 🚀 LLM Configuration Guide

## Recommended: OpenRouter (Fast & Affordable)

### Step 1: Get OpenRouter API Key (Free Credits!)
1. Go to: https://openrouter.ai/
2. Sign up (free)
3. Go to Keys: https://openrouter.ai/keys
4. Click "Create Key"
5. Copy your API key (starts with `sk-or-v1-...`)

### Step 2: Choose a Model
**Recommended for production:**
- `mistralai/mistral-7b-instruct` - Fast, cheap ($0.0006/1M tokens) ⭐ **BEST**
- `meta-llama/llama-3.2-3b-instruct` - Very fast, very cheap
- `openai/gpt-3.5-turbo` - Better quality, more expensive

**For high quality (more $):**
- `anthropic/claude-3-haiku` - Best balance
- `openai/gpt-4o-mini` - Good quality

### Step 3: Configure Environment Variables

**For Local Development:**
Create a `.env` file in the root directory:
```env
LLM_API_KEY=your-openrouter-api-key-here
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=mistralai/mistral-7b-instruct
```

**For Render Deployment:**
Add these environment variables in Render dashboard:
1. Go to your service → Environment
2. Add:
   - `LLM_API_KEY` = `your-openrouter-api-key`
   - `LLM_BASE_URL` = `https://openrouter.ai/api/v1`
   - `LLM_MODEL` = `mistralai/mistral-7b-instruct`

---

## Alternative: HuggingFace (Free but Slower)

### Step 1: Get HuggingFace Token
1. Go to: https://huggingface.co/
2. Sign up (free)
3. Go to Settings → Access Tokens
4. Create a token with "Read" permissions
5. Copy your token (starts with `hf_...`)

### Step 2: Configure for HuggingFace

**Environment Variables:**
```env
LLM_API_KEY=your-huggingface-token-here
LLM_BASE_URL=https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2/v1
LLM_MODEL=mistralai/Mistral-7B-Instruct-v0.2
```

**Note:** HuggingFace free tier has:
- ⚠️ Rate limits (few requests per minute)
- ⚠️ Cold starts (30-60s first request)
- ⚠️ Slower responses

---

## Pricing Comparison

### OpenRouter (Mistral 7B)
- **Cost:** ~$0.0006 per 1M tokens
- **Example:** 1000 queries/month = ~$0.60
- **Latency:** 1-3 seconds
- **Free credits:** Yes ($0.005 to start)

### HuggingFace Inference API
- **Cost:** FREE (rate limited)
- **Latency:** 10-60 seconds (with cold starts)
- **Reliability:** Lower on free tier

---

## 💡 My Recommendation

**For your deployment:**
1. ✅ Use **OpenRouter with Mistral 7B**
2. ✅ It's fast, cheap, and reliable
3. ✅ Free credits to test
4. ✅ No rate limits or cold starts
5. ✅ Better user experience

**Cost estimate:**
- ~$0.60/month for 1000 queries
- ~$2/month for 5000 queries
- Much cheaper than running your own GPU server!

---

## Quick Setup (OpenRouter)

```bash
# 1. Copy .env.example to .env
cp .env.example .env

# 2. Edit .env and add your OpenRouter key
LLM_API_KEY=sk-or-v1-your-key-here
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=mistralai/mistral-7b-instruct

# 3. Restart backend
python "week 5/src/main.py"
```

---

## Testing Your Setup

```bash
# Test locally
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('API Key:', os.getenv('LLM_API_KEY')[:20] + '...')"

# Test the RAG pipeline
python "week 6/src/rag_pipeline.py"
```

---

## Troubleshooting

**Issue: "No API Key found"**
- Check `.env` file exists in root directory
- Verify `LLM_API_KEY` is set correctly
- Restart the backend server

**Issue: "Rate limit exceeded" (HuggingFace)**
- Switch to OpenRouter (no rate limits on paid tier)
- Or wait a few minutes for HuggingFace cooldown

**Issue: "Model not found"**
- Check model name is correct
- For OpenRouter: https://openrouter.ai/models
- For HuggingFace: https://huggingface.co/models

---

## What Your Code Already Supports ✅

Your `rag_pipeline.py` already supports:
- ✅ OpenRouter
- ✅ OpenAI
- ✅ HuggingFace
- ✅ Any OpenAI-compatible API

Just change the environment variables! 🎉
