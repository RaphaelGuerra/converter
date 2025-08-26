# 🚀 M4A to MP3 Converter v3.0 - Quick Start

## 🎯 Choose Your Version

### ⭐ Python Edition (Recommended)
**Best for**: Audio processing, beautiful CLI, advanced features
- 🎨 **Stunning CLI** with Rich library
- 🔊 **Mature audio processing** with Pydub/Librosa
- 📊 **Advanced progress bars** with time estimates
- 🖥️ **Cross-platform excellence**

### Node.js Edition
**Best for**: Quick setup, familiar JavaScript ecosystem
- ⚡ **Fast npm installation**
- 🎮 **Full interactive CLI**
- 📦 **Self-contained package**
- 🔧 **Established ecosystem**

## 🎨 What You'll Get (Both Versions)

- **Interactive file selection** with visual menus
- **Real-time progress bars** during conversion
- **Smart compression** under 16MB automatically
- **Colored CLI output** for easy reading
- **Detailed statistics** and summaries
- **Batch processing** capabilities

## ⚡ 3-Step Setup

### Step 1: Install FFmpeg
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows: Download from https://ffmpeg.org/download.html
```

### Step 2: Setup Project

#### Python Edition (Recommended)
```bash
# Install Python dependencies and setup
python setup.py
```

#### Node.js Edition
```bash
# Install Node.js dependencies and setup
npm run setup
```

### Step 3: Add Your Files & Convert
```bash
# Copy your M4A files
cp ~/Downloads/*.m4a ./input/

# Start interactive conversion
python convert.py convert    # Python version
# OR
npm run convert             # Node.js version
```

## 🎮 Interactive Menu Guide

### 1. File Selection
```
📋 Available M4A Files:

┌─────┬────────────────┬─────────┬────────────┬──────────────┐
│Index│Filename        │Size     │Duration    │Estimated MP3 │
├─────┼────────────────┼─────────┼────────────┼──────────────┤
│1    │my-40mb-file.m4a│40.2MB   │240s        │~12.8MB       │
└─────┴────────────────┴─────────┴────────────┴──────────────┘

? What would you like to do? (Use arrow keys)
❯ ✅ Convert ALL files
  📂 Select specific files
  ❌ Cancel
```

### 2. Progress Monitoring
```
🎵 Converting: my-40mb-file.m4a
✅ Duration: 240s
🎯 Target bitrate: 85kbps

██████████████████████████████░░░░░ 87% | ETA: 5s | 87/100
```

### 3. Results Summary
```
════════════════════════════════════════════════════════════
🎉 CONVERSION SUMMARY
════════════════════════════════════════════════════════════

📊 Total Files: 1
📏 Original Size: 40.2MB
📏 Converted Size: 12.8MB
🗜️  Total Compression: 68.2%

✅ File is under 16MB limit!
```

## 🎨 Visual Features

### ✅ What You'll See
- **📋 File tables** with size information
- **📊 Progress bars** with ETA
- **🎨 Colored output** (green=success, red=errors, blue=info)
- **📈 Statistics** after conversion
- **⚠️  Warnings** if files are over 16MB

### 🎯 Smart Compression
- **40MB file** → **~13MB MP3** (68% compression)
- **Automatic bitrate** calculation
- **Quality optimization** for size limits
- **Stereo audio** preservation

## 🛠️ Command Reference

### Python Edition
| Command | Description |
|---------|-------------|
| `python convert.py convert` | **Interactive menu** (recommended) |
| `python convert.py batch` | Convert all files in input/ |
| `python convert.py single file.m4a` | Single file conversion |
| `python setup.py` | Setup and installation |

### Node.js Edition
| Command | Description |
|---------|-------------|
| `npm run convert` | **Interactive menu** (recommended) |
| `npm run convert-cli` | Command line version |
| `npm run convert-single file.m4a` | Single file conversion |
| `npm run setup` | Setup and installation |

## 💡 Pro Tips

1. **Large files**: The converter automatically optimizes for 16MB
2. **Batch processing**: Select multiple files in the interactive menu
3. **Progress tracking**: Watch real-time progress bars
4. **Error handling**: Clear error messages if something goes wrong
5. **File organization**: Keep sources in `input/`, results in `output/`

## 🔍 Example: Your 40MB File

```
Input: my-podcast.m4a (40MB)
Process: Analyzes duration → Calculates optimal bitrate → Converts
Output: my-podcast.mp3 (12.8MB) ✅
```

The interactive system will guide you through every step with visual feedback!

---

**Ready to convert? Choose your version and follow the menus! 🎵**

```bash
# Python edition (recommended)
python convert.py convert

# Node.js edition
npm run convert
```
