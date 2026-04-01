import json
from ebooklib import epub
from bs4 import BeautifulSoup
import re

# Load existing data
with open('data/questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

qcm_list = data.get('qcm', [])
flashcard_list = data.get('flashcards', [])

# Get next IDs
next_qcm_id = max([q['id'] for q in qcm_list], default=0) + 1
next_fc_id = max([f['id'] for f in flashcard_list], default=0) + 1

# Extract from Finances publiques EPUB
epub_path = r'Ressources\Finances publiques(4.édit).Anne-Claire Dufour.epub'
book = epub.read_epub(epub_path)

# Collect all chapters text
chapters_text = {}
for item in book.get_items():
    if item.get_type() == 9:  # EPUB type 9 = text content
        try:
            content = item.get_content().decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')
            text = ' '.join(soup.stripped_strings)
            if len(text) > 500:  # Only chapters with substantial content
                title = item.get_name()
                chapters_text[title] = text
        except:
            pass

# Print extracted content structure
print(f"Found {len(chapters_text)} chapters with substantial content")
for i, (title, text) in enumerate(list(chapters_text.items())[:15]):
    print(f"\n{i+1}. {title}: {len(text)} chars")
    print(f"   Preview: {text[:150]}...")
    if 'budget' in text.lower() or 'lolf' in text.lower() or 'pap' in text.lower():
        print("   ✓ Contains budget/LOLF/PAP content")
