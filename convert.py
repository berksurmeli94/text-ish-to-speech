# convert_epub_to_audio.py

import sys
import os
import zipfile
import asyncio
from bs4 import BeautifulSoup
from edge_tts import Communicate

VOICE = "en-US-JennyNeural"
CHUNK_SIZE = 5000
OUTPUT_DIR = "audiobook"

def extract_text_from_epub(epub_path):
    texts = []
    with zipfile.ZipFile(epub_path, 'r') as z:
        for filename in z.namelist():
            if filename.endswith(('.xhtml', '.html')) and "chapter" in filename.lower():
                with z.open(filename) as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    text = soup.get_text(separator=' ', strip=True)
                    if len(text) > 500:
                        texts.append(text)
    return " ".join(texts)

def chunk_text(text, max_length):
    for i in range(0, len(text), max_length):
        yield text[i:i+max_length]

async def speak(text, filename):
    communicate = Communicate(text, VOICE)
    await communicate.save(filename)

async def main(epub_file):
    if not os.path.exists(epub_file):
        print(f"❌ EPUB file not found: {epub_file}")
        return

    print(f"📖 Extracting from: {epub_file}")
    full_text = extract_text_from_epub(epub_file)
    chunks = list(chunk_text(full_text, CHUNK_SIZE))
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, chunk in enumerate(chunks, start=1):
        filename = os.path.join(OUTPUT_DIR, f"part_{i}.mp3")
        print(f"🎧 Generating part {i}")
        await speak(chunk, filename)
        print(f"✅ Saved: {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <book.epub>")
        sys.exit(1)
    asyncio.run(main(sys.argv[1]))
