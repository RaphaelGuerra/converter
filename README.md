# Audio Converter (M4A → MP3)

Last updated: 2026-01-06

## Table of Contents

<!-- TOC start -->
- [What It Does](#what-it-does)
- [How It Works](#how-it-works)
- [Run Locally](#run-locally)
- [Usage](#usage)
- [Tech Stack](#tech-stack)
- [Status & Learnings](#status--learnings)
- [License](#license)
<!-- TOC end -->

[![Lint](https://github.com/RaphaelGuerra/converter/actions/workflows/readme-lint.yml/badge.svg)](https://github.com/RaphaelGuerra/converter/actions/workflows/readme-lint.yml)
[![Security](https://github.com/RaphaelGuerra/converter/actions/workflows/security.yml/badge.svg)](https://github.com/RaphaelGuerra/converter/actions/workflows/security.yml)

Simple, interactive CLI to convert M4A audio files into MP3 with three quality
presets.

This is a small portfolio side project for learning — CLI UX, bitrate targeting
with FFmpeg, batch selection, and progress feedback. It is not a production
tool.

## What It Does

- Converts .m4a files to .mp3 using three presets (Small / Medium / Large)
- Targets practical file sizes while keeping reasonable quality
- Batch or selective conversion with simple range inputs
- Clear, guided prompts and progress output

## How It Works

- Wraps FFmpeg to transcode audio and estimate bitrates for the chosen preset
- Uses a simple folder workflow:
  - Place sources in `input/`
  - Converted files appear in `output/`
- Runs entirely offline on your machine

## Run Locally

Prerequisites: Python 3.10+ and FFmpeg

```bash
# Install FFmpeg (example)
# macOS
brew install ffmpeg
# Ubuntu/Debian
sudo apt install ffmpeg

# Setup Python env and run
python setup.py
python convert.py
```

## Usage

```bash
# Convert all .m4a files in input/ with Medium preset (default)
python convert.py

# Convert with Small preset for tighter size targets
python convert.py --quality small
```

## Tech Stack

- Python + FFmpeg
- Minimal dependencies

## Status & Learnings

- Functional prototype to practice CLI ergonomics and quality/size trade‑offs
- Next ideas: waveform preview, per‑file overrides, and presets export/import

## License

All rights reserved. Personal portfolio project — not for production use.
