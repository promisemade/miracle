"""Re-extract PDFs that failed due to encoding issues."""
import PyPDF2
import os

base = r"c:\Users\lroos\Desktop\Projet mIRAcle\Ressources"
failed_pdfs = [
    os.path.join(base, "France 2025  actualités et données clés (La Documentation française) (z-library.sk, 1lib.sk, z-lib.sk).pdf"),
    os.path.join(base, "Guide des politiques territoriales de A à Z Communes, intercommunalités, départements, régions, État  qui fait quoi  ( etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"),
    os.path.join(base, "Droit administratif", "Contentieux Administratif 7e édition Dalloz Lefevbre.pdf"),
    os.path.join(base, "Ressources humaines", "Fonction publique Mode d'emploi.pdf"),
]

output_file = os.path.join(r"c:\Users\lroos\Desktop\Projet mIRAcle", "extracted_failed_pdfs.txt")

with open(output_file, "w", encoding="utf-8", errors="replace") as out:
    for pdf_path in failed_pdfs:
        basename = os.path.basename(pdf_path)
        if not os.path.exists(pdf_path):
            out.write(f"\n{'='*80}\nFILE NOT FOUND: {basename}\n{'='*80}\n")
            continue
        
        out.write(f"\n{'='*80}\nFILE: {basename}\n{'='*80}\n")
        
        try:
            reader = PyPDF2.PdfReader(pdf_path)
            total_pages = len(reader.pages)
            out.write(f"Pages: {total_pages}\n\n")
            
            pages_to_extract = list(range(min(total_pages, 60)))
            if total_pages > 60:
                pages_to_extract += list(range(60, min(total_pages, 200), 3))
            if total_pages > 200:
                pages_to_extract += list(range(max(200, total_pages - 10), total_pages))
            
            for i in pages_to_extract:
                try:
                    text = reader.pages[i].extract_text()
                    if text and text.strip():
                        out.write(f"--- Page {i+1} ---\n")
                        out.write(text.strip() + "\n\n")
                except Exception as e:
                    out.write(f"--- Page {i+1} ---\nERROR: {e}\n\n")
                        
        except Exception as e:
            out.write(f"FATAL ERROR: {e}\n")

print(f"Done! Output: {output_file}")
print(f"Size: {os.path.getsize(output_file)} bytes")
