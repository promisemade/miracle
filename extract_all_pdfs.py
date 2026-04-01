"""Extract key content from all new PDFs for question generation."""
import os
import PyPDF2

RESSOURCES = r"c:\Users\lroos\Desktop\Projet mIRAcle\Ressources"

pdf_files = []
for root, dirs, files in os.walk(RESSOURCES):
    for f in files:
        if f.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(root, f))

print(f"Found {len(pdf_files)} PDF files\n")

for pdf_path in sorted(pdf_files):
    rel = os.path.relpath(pdf_path, RESSOURCES)
    print(f"\n{'='*80}")
    print(f"FILE: {rel}")
    print(f"{'='*80}")
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        total_pages = len(reader.pages)
        print(f"Pages: {total_pages}")
        
        # Extract first 15 pages and some middle pages for content overview
        pages_to_read = list(range(min(20, total_pages)))
        # Add some middle pages
        if total_pages > 40:
            mid = total_pages // 2
            pages_to_read += list(range(mid-3, mid+3))
        # Add some later pages  
        if total_pages > 60:
            pages_to_read += list(range(total_pages-5, total_pages))
            
        pages_to_read = sorted(set(p for p in pages_to_read if 0 <= p < total_pages))
        
        for i in pages_to_read:
            text = reader.pages[i].extract_text()
            if text and len(text.strip()) > 50:
                print(f"\n--- Page {i+1} ---")
                # Print first 2000 chars of each page
                print(text[:2000])
    except Exception as e:
        print(f"ERROR: {e}")
