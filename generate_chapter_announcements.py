import os
import asyncio
from edge_tts import Communicate

VOICE = "en-US-JennyNeural"
AUDIOBOOK_DIR = "audiobook"
OUTPUT_DIR = "chapter_announcements"

# Find number of audio parts
part_files = [
    f for f in os.listdir(AUDIOBOOK_DIR)
    if f.startswith("part_") and f.endswith(".mp3")
]
part_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
num_parts = len(part_files)

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def speak(text, filename):
    communicate = Communicate(text, VOICE)
    await communicate.save(filename)

async def main():
    for i in range(1, num_parts + 1):
        text = f"Chapter {i}"
        output_path = os.path.join(OUTPUT_DIR, f"chapter_{i}.mp3")
        print(f"🎙️ Generating: {text}")
        await speak(text, output_path)
        print(f"✅ Saved: {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
