#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract from Finances publiques 2016 GUALINO PDF and generate QCM
"""
import json
import os
from pypdf import PdfReader
import re

# Check if PDF exists
gualino_path = r'Ressources\Finances_publiques_2016_GUALINO.pdf'
if not os.path.exists(gualino_path):
    print(f"[ERROR] File not found: {gualino_path}")
    print("\nLooking for PDF files in Ressources/...")
    ressources_path = 'Ressources'
    pdfs = [f for f in os.listdir(ressources_path) if f.endswith('.pdf')]
    print(f"Found {len(pdfs)} PDF files:")
    for pdf in pdfs:
        print(f"  - {pdf}")
else:
    print(f"[OK] Found: {gualino_path}")
    
    # Try to extract text from first few pages
    try:
        reader = PdfReader(gualino_path)
        print(f"[OK] PDF loaded: {len(reader.pages)} pages")
        
        # Extract text from first 5 pages
        print("\n[*] Extracting first 5 pages...\n")
        for i in range(min(5, len(reader.pages))):
            page = reader.pages[i]
            text = page.extract_text()
            print(f"\n--- PAGE {i+1} ---")
            print(text[:400] if text else "[No text extracted]")
            
    except Exception as e:
        print(f"[ERROR] Failed to read PDF: {e}")
