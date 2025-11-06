# Quick Dev Setup - Fast Testing Mode ⚡

## TL;DR
Skip slow Docling conversion during development by using cached PDF and markdown.

---

## Setup (2 minutes)

### 1. First Upload (One-time)
```bash
# Start backend
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload --port 8000

# Start frontend (new terminal)
cd frontend
npm start
```

Upload your test PDF through the UI → Cache created automatically!

### 2. Done! 🎉
All subsequent uploads use cache instantly.

---

## How to Use

### During Development
```python
# backend/dev_cache.py
DEV_MODE = True  # ✅ Already enabled
```

**Result:** Upload any PDF → Instant loading ⚡

### Before Deployment
```python
# backend/dev_cache.py
DEV_MODE = False  # ❌ Disable for production
```

**Result:** Real Docling conversion for each PDF

---

## Visual Guide

### First Upload (Creates Cache)
```
Upload PDF → ⏳ Converting (5-30s) → 💾 Saved to cache
```

### Subsequent Uploads (Uses Cache)
```
Upload PDF → 🚀 DEV MODE → ⚡ Instant!
```

---

## Console Messages

**Dev Mode Active:**
```
🚀 DEV MODE: Using cached PDF and markdown
📦 Loaded from cache: sample.pdf
```

**Cache Created:**
```
💾 Saving to cache for future dev use...
✓ Cached PDF: backend/dev_cache_data/sample.pdf
```

---

## Files Created

```
backend/dev_cache_data/
├── sample.pdf           # Your test PDF
├── sample.md            # Pre-converted markdown
└── page_mapping.json    # Page mapping
```

---

## Benefits

- ⚡ **Instant loading** (no 30s wait)
- 🔄 **Test quickly** (rapid iteration)
- 🎯 **Focus on logic** (not waiting)
- 💰 **Save time** (hours → minutes)

---

## Troubleshooting

**Still slow?**
- Check: `backend/dev_cache.py` → `DEV_MODE = True`
- Restart backend server

**Want fresh cache?**
```bash
rm -rf backend/dev_cache_data/
# Upload PDF again
```

---

**See `DEV_MODE_GUIDE.md` for detailed documentation.**
