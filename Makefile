BOOK ?= $(shell read -p "📘 Enter book file (e.g., book.epub): " book; echo $$book)

PYTHON = .venv/bin/python
PIP = .venv/bin/pip

.PHONY: all setup convert generate merge export clean

all: convert generate merge export

setup:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

convert:
	$(PYTHON) convert.py "$(BOOK)"

generate:
	$(PYTHON) generate_chapter_announcements.py

merge:
	$(PYTHON) merge.py

export:
	ffmpeg -i audiobook_full_with_intros.mp3 -vn -c:a aac -b:a 64k audiobook.m4b
	@echo "✅ Exported: audiobook.m4b"

clean:
	@echo "🧹 Cleaning up..."
	@rm -rf .venv __pycache__ \
		audiobook \
		chapter_announcements \
		audiobook_full.mp3 \
		audiobook_full_with_intros.mp3 \
		*.part.mp3 \
		*.chapter.mp3 \
		*.DS_Store || true
	@echo "✅ Clean complete."
