# Quick Start - AI Extraction

## 3-Step Setup

### 1️⃣ Install Dependencies
```bash
cd backend
install-ai-dependencies.bat
```

### 2️⃣ Add Your API Key
1. Open `backend\.env`
2. Replace `your_openai_api_key_here` with your actual key
3. Get key from: https://platform.openai.com/api-keys

### 3️⃣ Start the App
```bash
# Terminal 1 - Backend
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm start
```

## Usage

1. **Upload** parameter list and PDF
2. **Select** "AI-Powered (OpenAI)" radio button
3. **Click** "Extract Parameters"
4. **Wait** 2-5 seconds for AI analysis
5. **Review** results!

*Note: API key is read automatically from `backend/.env` file*

## Cost
- ~$0.01-0.02 per extraction (GPT-3.5)
- Much cheaper than manual work!

## Comparison

| Mode | Speed | Accuracy | Cost |
|------|-------|----------|------|
| Simple | Instant | ~85% | Free |
| AI | 2-5s | ~95%+ | ~$0.01 |

---

**See `AI_EXTRACTION_SETUP.md` for detailed documentation.**
