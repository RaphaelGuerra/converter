# Audio Converter (M4A → MP3)

Last updated: 2025-11-28

## Table of Contents

<!-- TOC start -->
- [What It Does](#what-it-does)
- [How It Works](#how-it-works)
- [Run Locally](#run-locally)
- [Tech Stack](#tech-stack)
- [Status & Learnings](#status-learnings)
- [License](#license)
<!-- TOC end -->

Simple, interactive CLI to convert M4A audio files into MP3 with three quality presets.

This is a small portfolio side project for learning — CLI UX, bitrate targeting with FFmpeg, batch selection, and progress feedback. It is not a production tool.

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

## Tech Stack
- Python + FFmpeg
- Minimal dependencies

## Status & Learnings
- Functional prototype to practice CLI ergonomics and quality/size trade‑offs
- Next ideas: waveform preview, per‑file overrides, and presets export/import

## License
All rights reserved. Personal portfolio project — not for production use.
