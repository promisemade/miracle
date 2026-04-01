#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR extraction from Contentieux administratif - comprehensive coverage
Generate 30+ additional QCM on procedure, case law, evidence, remedies
"""
import json
import os
import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF

# Configuration
os.environ['TESSDATA_PREFIX'] = r'c:\Users\lroos\Desktop\Projet mIRAcle\tessdata'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load existing data
with open('data/questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

qcm_list = data.get('qcm', [])
next_qcm_id = max([q['id'] for q in qcm_list], default=0) + 1
next_fc_id = max([data.get('flashcards', []) and max([f['id'] for f in data.get('flashcards', [])], default=0) or 0], default=0) + 1

# Extract more pages from Contentieux PDF using OCR
pdf_path = r'Ressources\Contentieux Administratif 7e édition Dalloz.pdf'
print(f"[*] Opening: {pdf_path}")

if not os.path.exists(pdf_path):
    print(f"[ERROR] File not found")
else:
    doc = fitz.open(pdf_path)
    print(f"[OK] PDF opened: {len(doc)} pages")
    
    # Extract from key sections (procedure, remedies, evidence)
    # Already did: pages 1, 41-44, 101-104, 201-204
    # Now: pages 310-320 (procedure), 400-410 (remedies), 500-510 (evidence/proof)
    
    target_pages = list(range(309, 320)) + list(range(399, 410)) + list(range(500, 510))
    target_pages = [p for p in target_pages if p < len(doc)]
    
    print(f"\n[*] Extracting {len(target_pages)} pages via OCR...")
    extracted_text = {}
    
    for page_num in target_pages:
        try:
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=200)
            img = Image.open(io.BytesIO(pix.tobytes('png')))
            text = pytesseract.image_to_string(img, lang='fra')
            
            # Clean text
            text = ' '.join(text.split())
            if len(text) > 100:
                extracted_text[page_num+1] = text
                print(f"  Page {page_num+1}: {len(text)} chars")
        except Exception as e:
            print(f"  Page {page_num+1}: ERROR - {str(e)[:50]}")
    
    print(f"\n[OK] Successfully extracted from {len(extracted_text)} pages")
    
    # Sample key content
    if extracted_text:
        sample_pages = list(extracted_text.keys())[:3]
        print(f"\nSample content from pages: {sample_pages}")
        for page_num in sample_pages:
            preview = extracted_text[page_num][:150]
            print(f"  Page {page_num}: {preview}...")
    
    doc.close()

print(f"\n[READY] Proceed with QCM generation from extracted sections")
print(f"  Next QCM ID: {next_qcm_id}")
print(f"  Next FC ID: {next_fc_id}")
