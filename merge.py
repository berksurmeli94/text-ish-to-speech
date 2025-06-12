from pydub import AudioSegment
import os
import re

AUDIO_DIR = "audiobook"
INTRO_DIR = "chapter_announcements"
OUTPUT_FILE = "audiobook_full_with_intros.mp3"
SILENCE_DURATION_MS = 1000

def sorted_parts(directory, prefix):
    files = [
        f for f in os.listdir(directory)
        if f.endswith('.mp3') and f.startswith(prefix)
    ]
    files.sort(key=lambda x: int(re.search(r'_(\d+)', x).group(1)))
    return [os.path.join(directory, f) for f in files]

chapter_files = sorted_parts(INTRO_DIR, "chapter")
part_files = sorted_parts(AUDIO_DIR, "part")

combined = AudioSegment.empty()
silence = AudioSegment.silent(duration=SILENCE_DURATION_MS)

for chapter, part in zip(chapter_files, part_files):
    print(f"🎧 Merging: {chapter} + {part}")
    intro = AudioSegment.from_mp3(chapter)
    content = AudioSegment.from_mp3(part)
    combined += intro + silence + content + silence

combined.export(OUTPUT_FILE, format="mp3")
print(f"✅ Final audiobook with intros saved as: {OUTPUT_FILE}")
