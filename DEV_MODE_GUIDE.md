# Development Mode Guide

## Problem
Docling PDF → Markdown conversion is **slow** (5-30 seconds per PDF), making development and testing painful.

## Solution
**Development Mode** with cached PDF and markdown files for instant loading during testing.

---

## How It Works

### First Time (One-time setup)
1. Upload a real PDF through the UI
2. Backend converts it with Docling (slow, but only once)
3. Backend automatically saves to cache:
   - `backend/dev_cache_data/sample.pdf`
   - `backend/dev_cache_data/sample.md`
   - `backend/dev_cache_data/page_mapping.json`

### Every Time After
1. Upload any PDF through the UI
2. Backend detects `DEV_MODE = True`
3. **Instantly loads from cache** (no conversion!)
4. You can test immediately ⚡

---

## Setup Instructions

### Step 1: Enable Dev Mode (Already Done)
File: `backend/dev_cache.py`
```python
DEV_MODE = True  # ✅ Already set to True
```

### Step 2: Create Cache (First Time Only)

**Option A: Upload through UI (Recommended)**
1. Start backend: `cd backend && uvicorn main:app --reload --port 8000`
2. Start frontend: `cd frontend && npm start`
3. Upload your test PDF (e.g., `tps746-q1.pdf`)
4. Wait for conversion (this happens once)
5. Cache is automatically created! ✅

**Option B: Manual Cache Creation**
```python
# In backend directory
python
>>> from dev_cache import save_to_cache
>>> from markdown_converter import MarkdownConverter
>>> 
>>> # Convert your PDF
>>> converter = MarkdownConverter()
>>> result = converter.convert_pdf_to_markdown("path/to/your.pdf")
>>> 
>>> # Save to cache
>>> save_to_cache("path/to/your.pdf", result["markdown"], result["page_mapping"])
```

### Step 3: Test It!
1. Restart backend
2. Upload **any** PDF through UI
3. See console: `🚀 DEV MODE: Using cached PDF and markdown`
4. Instant loading! ⚡

---

## Usage

### During Development
```python
# backend/dev_cache.py
DEV_MODE = True  # ✅ Use cached data (fast)
```

- Upload any PDF → Uses cache
- Instant markdown loading
- Perfect for testing extraction logic
- No waiting for Docling

### Before Production/Deployment
```python
# backend/dev_cache.py
DEV_MODE = False  # ❌ Disable cache (use real conversion)
```

- Upload PDF → Real Docling conversion
- Fresh markdown for each PDF
- Production-ready behavior

---

## File Structure

```
backend/
├── dev_cache.py                    # Dev mode logic
├── dev_cache_data/                 # Cache directory (auto-created)
│   ├── sample.pdf                  # Cached PDF
│   ├── sample.md                   # Pre-converted markdown
│   └── page_mapping.json           # Page mapping data
├── main.py                         # Uses dev_cache when DEV_MODE=True
└── ...
```

---

## Console Output

### Dev Mode (Fast ⚡)
```
🚀 DEV MODE: Using cached PDF and markdown
📦 Loaded from cache: sample.pdf
   Markdown: 45231 chars
   Pages: 15
```

### Production Mode (Slow ⏳)
```
⏳ Converting PDF to markdown with Docling...
💾 Saving to cache for future dev use...
✓ Cached PDF: backend/dev_cache_data/sample.pdf
✓ Cached Markdown: backend/dev_cache_data/sample.md
✓ Cached Page Mapping: backend/dev_cache_data/page_mapping.json
```

---

## Benefits

| Aspect | Without Dev Mode | With Dev Mode |
|--------|------------------|---------------|
| **First Upload** | 5-30 seconds | 5-30 seconds (creates cache) |
| **Subsequent Uploads** | 5-30 seconds each | **Instant!** ⚡ |
| **Testing Speed** | Slow 😴 | Fast 🚀 |
| **Development Flow** | Painful | Smooth |

---

## Troubleshooting

### "Cache not found" error
- Upload a PDF through the UI first
- Or manually create cache (see Step 2, Option B)

### Still slow after enabling dev mode
- Check `backend/dev_cache.py`: `DEV_MODE = True`?
- Check if cache files exist: `backend/dev_cache_data/`
- Restart backend server

### Want to update cached PDF
1. Delete `backend/dev_cache_data/` folder
2. Upload new PDF through UI
3. New cache created automatically

### Disable dev mode
```python
# backend/dev_cache.py
DEV_MODE = False
```

---

## Testing Checklist

- [ ] `DEV_MODE = True` in `backend/dev_cache.py`
- [ ] Upload PDF once to create cache
- [ ] See "🚀 DEV MODE" message in console
- [ ] Subsequent uploads are instant
- [ ] Extraction works normally
- [ ] Before deployment: Set `DEV_MODE = False`

---

## Important Notes

1. **Cache is per-PDF:** If you need different PDFs, update the cache
2. **Git ignored:** `dev_cache_data/` is in `.gitignore` (won't be committed)
3. **Development only:** Always set `DEV_MODE = False` before production
4. **Automatic caching:** First upload in dev mode creates cache automatically

---

## Quick Commands

```bash
# Check if cache exists
cd backend
python dev_cache.py

# Clear cache (to start fresh)
rm -rf dev_cache_data/

# Test dev mode
python -c "import dev_cache; print('Dev mode:', dev_cache.DEV_MODE)"
```

---

**Status:** ✅ Ready to use!  
**Speed Improvement:** ~30 seconds → Instant ⚡  
**Perfect for:** Development, testing, debugging
