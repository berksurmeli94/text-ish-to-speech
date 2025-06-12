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
    try:
        with zipfile.ZipFile(epub_path, 'r') as z:
            for filename in z.namelist():
                if filename.endswith(('.xhtml', '.html')) and "chapter" in filename.lower():
                    with z.open(filename) as f:
                        soup = BeautifulSoup(f.read(), 'html.parser')
                        text = soup.get_text(separator=' ', strip=True)
                        if len(text) > 500:
                            texts.append(text)
    except zipfile.BadZipFile:
        raise ValueError(f"❌ Not a valid EPUB file: {epub_path}")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to extract EPUB content: {e}")

    if not texts:
        raise ValueError("❌ No readable chapters found in EPUB.")
    
    return " ".join(texts)

def chunk_text(text, max_length):
    for i in range(0, len(text), max_length):
        yield text[i:i+max_length]

async def speak(text, filename):
    try:
        communicate = Communicate(text, VOICE)
        await communicate.save(filename)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to synthesize audio for chunk → {e}")

async def main(epub_file):
    try:
        if not os.path.exists(epub_file):
            raise FileNotFoundError(f"❌ EPUB file not found: {epub_file}")

        print(f"📖 Extracting from: {epub_file}")
        full_text = extract_text_from_epub(epub_file)

        chunks = list(chunk_text(full_text, CHUNK_SIZE))
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        for i, chunk in enumerate(chunks, start=1):
            filename = os.path.join(OUTPUT_DIR, f"part_{i}.mp3")
            print(f"🎧 Generating part {i}")
            await speak(chunk, filename)
            print(f"✅ Saved: {filename}")

    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <book.epub>")
        sys.exit(1)

    asyncio.run(main(sys.argv[1]))
