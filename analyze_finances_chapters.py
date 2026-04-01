#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep extraction from Finances publiques EPUB - targeted content mining
"""
import json
import os
from ebooklib import epub
from bs4 import BeautifulSoup
import re

# ============ LOAD EXISTING DATA ============
with open('data/questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

qcm_list = data.get('qcm', [])
flashcard_list = data.get('flashcards', [])
next_qcm_id = max([q['id'] for q in qcm_list], default=0) + 1
next_fc_id = max([f['id'] for f in flashcard_list], default=0) + 1

# ============ EXTRACT FROM EPUB ============
epub_path = r'Ressources\Finances publiques(4.édit).Anne-Claire Dufour.epub'
print(f"[*] Extracting from: {epub_path}")

book = epub.read_epub(epub_path)
chapters = []

for item in book.get_items():
    if item.get_type() == 9:  # Text content
        try:
            content = item.get_content().decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')
            text = ' '.join(soup.stripped_strings)
            
            if len(text) > 300:  # Substantial content
                # Extract title if available
                title_tag = soup.find(['h1', 'h2', 'h3', 'title'])
                title = title_tag.get_text(strip=True) if title_tag else item.get_name()
                
                chapters.append({
                    'title': title,
                    'text': text,
                    'length': len(text)
                })
        except Exception as e:
            pass

print(f"\n[OK] Extracted {len(chapters)} chapters")
print(f"\nTop chapters by size:")
for i, ch in enumerate(sorted(chapters, key=lambda x: x['length'], reverse=True)[:10]):
    print(f"  {i+1}. {ch['title'][:60]:<60} {ch['length']:>6} chars")

# ============ FOCUS ON KEY TOPICS ============
# Search for chapters containing key financial concepts
key_topics = ['budget', 'lolf', 'pap', 'rap', 'dépense', 'recette', 'trésorerie', 
              'déficit', 'dette', 'fiscalité', 'impôt', 'subvention', 'droit', 'procédure']

print(f"\n[FIND] Chapters containing key financial topics:")
relevant_chapters = []
for ch in chapters:
    text_lower = ch['text'].lower()
    matches = [t for t in key_topics if t in text_lower]
    if matches:
        relevant_chapters.append((ch, matches))
        print(f"  - {ch['title'][:50]:<50} - {len(matches)} topics: {', '.join(set(matches))}")

print(f"\n[STATS] Total relevant chapters: {len(relevant_chapters)}")

# ============ EXTRACT DETAILED CONTENT FROM TOP CHAPTERS ============
print("\n\n=== DETAILED CONTENT EXTRACTION ===\n")

# Take top 15 relevant chapters by size
top_chapters = sorted(relevant_chapters, key=lambda x: x[0]['length'], reverse=True)[:15]

for idx, (chapter, topics) in enumerate(top_chapters, 1):
    text = chapter['text']
    title = chapter['title']
    
    # Extract sentences (rough sentence splitting)
    sentences = re.split(r'(?<=[.!?])\s+', text)[:50]  # First 50 sentences
    
    print(f"\n{idx}. {title}")
    print(f"   Topics: {', '.join(set(topics))}")
    print(f"   Sample content:")
    for sent in sentences[:3]:
        if sent.strip():
            print(f"   - {sent[:100]}...")

print("\n\n[SUCCESS] Ready for QCM generation from these chapters")
print(f"   Next QCM ID: {next_qcm_id}")
print(f"   Next Flashcard ID: {next_fc_id}")
