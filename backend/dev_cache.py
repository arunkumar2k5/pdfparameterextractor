"""
Development cache for pre-converted PDF and markdown.
This allows faster testing by skipping the slow Docling conversion.
"""

import os
from pathlib import Path

# Development mode flag - Set to True to use cached data
DEV_MODE = True

# Paths for cached files
CACHE_DIR = Path(__file__).parent / "dev_cache_data"
CACHE_DIR.mkdir(exist_ok=True)

CACHED_PDF_PATH = CACHE_DIR / "sample.pdf"
CACHED_MARKDOWN_PATH = CACHE_DIR / "sample.md"
CACHED_PAGE_MAPPING_PATH = CACHE_DIR / "page_mapping.json"


def save_to_cache(pdf_path: str, markdown: str, page_mapping: dict):
    """
    Save PDF, markdown, and page mapping to cache for development.
    Call this once with a real PDF to create the cache.
    """
    import json
    import shutil
    
    # Copy PDF to cache
    if os.path.exists(pdf_path):
        shutil.copy(pdf_path, CACHED_PDF_PATH)
        print(f"✓ Cached PDF: {CACHED_PDF_PATH}")
    
    # Save markdown
    with open(CACHED_MARKDOWN_PATH, 'w', encoding='utf-8') as f:
        f.write(markdown)
    print(f"✓ Cached Markdown: {CACHED_MARKDOWN_PATH}")
    
    # Save page mapping
    with open(CACHED_PAGE_MAPPING_PATH, 'w', encoding='utf-8') as f:
        json.dump(page_mapping, f, indent=2)
    print(f"✓ Cached Page Mapping: {CACHED_PAGE_MAPPING_PATH}")
    
    print("\n✅ Cache created! Set DEV_MODE = True to use cached data.")


def load_from_cache():
    """
    Load cached PDF, markdown, and page mapping.
    Returns: (pdf_path, markdown, page_mapping, total_pages)
    """
    import json
    
    if not CACHED_PDF_PATH.exists():
        raise FileNotFoundError(
            f"Cache not found. Please run with a real PDF first to create cache.\n"
            f"Expected: {CACHED_PDF_PATH}"
        )
    
    # Load markdown
    with open(CACHED_MARKDOWN_PATH, 'r', encoding='utf-8') as f:
        markdown = f.read()
    
    # Load page mapping
    with open(CACHED_PAGE_MAPPING_PATH, 'r', encoding='utf-8') as f:
        page_mapping = json.load(f)
    
    total_pages = len(set(page_mapping.values())) if page_mapping else 1
    
    print(f"📦 Loaded from cache: {CACHED_PDF_PATH.name}")
    print(f"   Markdown: {len(markdown)} chars")
    print(f"   Pages: {total_pages}")
    
    return str(CACHED_PDF_PATH), markdown, page_mapping, total_pages


def is_cache_available():
    """Check if cache files exist"""
    return (
        CACHED_PDF_PATH.exists() and 
        CACHED_MARKDOWN_PATH.exists() and 
        CACHED_PAGE_MAPPING_PATH.exists()
    )


# For quick testing
if __name__ == "__main__":
    if is_cache_available():
        print("✓ Cache is available!")
        pdf_path, markdown, page_mapping, total_pages = load_from_cache()
        print(f"\nPDF: {pdf_path}")
        print(f"Markdown preview: {markdown[:200]}...")
        print(f"Total pages: {total_pages}")
    else:
        print("✗ Cache not available. Upload a PDF first to create cache.")
