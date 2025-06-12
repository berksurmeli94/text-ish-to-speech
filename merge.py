from pydub import AudioSegment
import os
import re
import sys

AUDIO_DIR = "audiobook"
INTRO_DIR = "chapter_announcements"
OUTPUT_FILE = "audiobook_full_with_intros.mp3"
SILENCE_DURATION_MS = 1000

def sorted_parts(directory, prefix):
    try:
        files = [
            f for f in os.listdir(directory)
            if f.endswith('.mp3') and f.startswith(prefix)
        ]
        files.sort(key=lambda x: int(re.search(r'_(\d+)', x).group(1)))
        return [os.path.join(directory, f) for f in files]
    except Exception as e:
        print(f"❌ Error reading files in {directory}: {e}")
        sys.exit(2)

chapter_files = sorted_parts(INTRO_DIR, "chapter")
part_files = sorted_parts(AUDIO_DIR, "part")

if not chapter_files or not part_files:
    print("❌ Missing chapter or part files.")
    sys.exit(1)

combined = AudioSegment.empty()
silence = AudioSegment.silent(duration=SILENCE_DURATION_MS)

for chapter, part in zip(chapter_files, part_files):
    try:
        print(f"🎧 Merging: {chapter} + {part}")
        intro = AudioSegment.from_mp3(chapter)
        content = AudioSegment.from_mp3(part)
        combined += intro + silence + content + silence
    except Exception as e:
        print(f"❌ Failed to merge {chapter} and {part}: {e}")
        sys.exit(3)

try:
    combined.export(OUTPUT_FILE, format="mp3")
    print(f"✅ Final audiobook with intros saved as: {OUTPUT_FILE}")
except Exception as e:
    print(f"❌ Failed to export final audio: {e}")
    sys.exit(4)
