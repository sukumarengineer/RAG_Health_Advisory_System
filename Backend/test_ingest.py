# Backend/test_ingest.py — run this once, then delete it
from ingest import extract_text, chunk_text

text = extract_text("FactSheet_Dengue.pdf")
chunks = chunk_text(text)

print("Extracted", len(text), "characters")
print("Split into", len(chunks), "chunks")
print("1st chunk - Length: ",len(chunks[0]))

print("2nd chunk - Length: ",len(chunks[1]))

print("3rd chunk - Length: ",len(chunks[2]))

print("4th chunk - Length: ",len(chunks[3]))

print("5th chunk - Length: ",len(chunks[4]))

print("6th chunk - Length: ",len(chunks[5]))

print("7th chunk - Length: ",len(chunks[6]))