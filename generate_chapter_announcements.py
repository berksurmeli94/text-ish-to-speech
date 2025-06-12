import os
import asyncio
from edge_tts import Communicate

VOICE = "en-US-JennyNeural"
AUDIOBOOK_DIR = "audiobook"
OUTPUT_DIR = "chapter_announcements"

async def speak(text, filename):
    try:
        communicate = Communicate(text, VOICE)
        await communicate.save(filename)
    except Exception as e:
        raise RuntimeError(f"Failed to generate audio for '{text}' → {e}")

def get_part_files(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"❌ Missing audio directory: {directory}")

    files = [
        f for f in os.listdir(directory)
        if f.startswith("part_") and f.endswith(".mp3")
    ]
    if not files:
        raise FileNotFoundError("❌ No audio parts found. Run `make convert` first.")

    files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
    return files

async def main():
    try:
        part_files = get_part_files(AUDIOBOOK_DIR)
        num_parts = len(part_files)

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        for i in range(1, num_parts + 1):
            text = f"Chapter {i}"
            output_path = os.path.join(OUTPUT_DIR, f"chapter_{i}.mp3")
            print(f"🎙️ Generating: {text}")
            await speak(text, output_path)
            print(f"✅ Saved: {output_path}")

    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())
