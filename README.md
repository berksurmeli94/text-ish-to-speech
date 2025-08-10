# 🎧 Text-ish to Speech

Convert `.epub` books into educational audiobooks — offline and fully automated with chapter intros, silence spacing, and `.m4b` export.

> ⭐ **Useful?** Give it a star to support the project!  
> 💬 **Have ideas or found a bug?** Open an [issue](https://github.com/berksurmeli94/text-ish-to-speech/issues)

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
```

---

## 🤝 Contributing

If you want to contribute to a project and make it better, your help is very welcome.

### How to contribute

- Create a personal fork of the project on Github.
- Clone the fork on your local machine. Your remote repo on Github is called `origin`.
- Add the original repository as a remote called `upstream`.
- If you created your fork a while ago be sure to pull upstream changes into your local repository.
- Create a new branch to work on! Branch from `develop` if it exists, else from `master`.
- Implement/fix your feature, comment your code.
- Follow the code style of the project, including indentation.
- If the project has tests run them!
- Write or adapt tests as needed.
- Add or change the documentation as needed.
- Squash your commits into a single commit with git's [interactive rebase](https://help.github.com/articles/interactive-rebase). Create a new branch if necessary.
- Push your branch to your fork on Github, the remote `origin`.
- From your fork open a pull request in the correct branch. Target the project's `develop` branch if there is one, else go for `master`!
- If the maintainer requests further changes just push them to your branch. The PR will be updated automatically.
- Once the pull request is approved and merged you can pull the changes from `upstream` to your local repo and delete
  your extra branch(es).

And last but not least: Always write your commit messages in the present tense. Your commit message should describe what the commit, when applied, does to the code – not what you did to the code.
