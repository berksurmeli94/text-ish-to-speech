# 🎧 Text-ish to Speech

Convert any `.epub` book into a fully narrated audiobook — complete with chapter announcements, educational tone, and clean `.m4b` export. All locally, no AI API keys needed.

---

## 📚 Features

- ✅ Converts `.epub` files to MP3 chunks using `pyttsx3` (offline text-to-speech)
- ✅ Generates chapter intros using natural-sounding `edge-tts` voices
- ✅ Merges everything into a single audiobook with silence buffers
- ✅ Exports in `.m4b` format (iTunes & audiobook player friendly)
- ✅ One-command automation via Makefile

---

## 🚀 Setup

> Recommended Python: **3.10.13**

1. Clone the repo:
   ```bash
   git clone https://github.com/berksurmeli94/text-ish-to-speech.git
   cd text-ish-to-speech

2. setup
brew install ffmpeg   # on macOS
# or
sudo apt install ffmpeg  # on Ubuntu/Debian

3. create and activate virtualenv
python3.10 -m venv .venv
source .venv/bin/activate

4. installing depedencies
pip install -r requirements.txt

5. run
make setup
make
make clean

