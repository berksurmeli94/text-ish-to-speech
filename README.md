# 🎧 Text-ish to Speech

Convert `.epub` books into educational audiobooks — offline and fully automated with chapter intros, silence spacing, and `.m4b` export.

---

## 📚 Features

- 🎙️ Converts `.epub` to MP3 chunks using `pyttsx3` (offline)
- 📢 Generates natural-sounding chapter intros with `edge-tts`
- 🧩 Merges parts with silence and intros
- 📦 Exports a clean `.m4b` file
- 🛠️ Fully automated with a `Makefile`

---

## 🚀 Setup & Run

### 1. Clone the repo, install system dependencies, and set up the environment:

```bash
git clone https://github.com/berksurmeli94/text-ish-to-speech.git
cd text-ish-to-speech

# Install system dependencies
brew install ffmpeg        # macOS
# or
sudo apt install ffmpeg    # Ubuntu/Debian

# Create and activate a virtual environment
python3.10 -m venv .venv
source .venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Run
make setup
make
make clean
