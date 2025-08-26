# 🚀 Python M4A to MP3 Converter - Quick Start

## 🎯 Why Python?

- **🎨 Beautiful CLI** with Rich library
- **🔊 Superior Audio Processing** with Pydub and Librosa
- **📊 Advanced Progress Bars** with time estimates
- **🖥️ Cross-Platform Excellence**
- **🎯 Mature Ecosystem** for audio conversion

## ⚡ 3-Step Setup

### Step 1: Install FFmpeg
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows: Download from https://ffmpeg.org/download.html
```

### Step 2: Setup Python Environment
```bash
# Run the automated setup
python setup.py

# This will:
# ✅ Check Python version (3.7+)
# ✅ Verify FFmpeg installation
# 📦 Install Python dependencies
# 📁 Create input/, output/, test-files/ directories
```

### Step 3: Convert Your Files
```bash
# Interactive mode (recommended)
python convert.py convert

# Batch convert all files
python convert.py batch

# Convert single file
python convert.py single your-file.m4a
```

## 🎨 What Makes Python Version Special

### Rich Interactive Interface
```
┌─────────────────────────────────────────────────────────────┐
│                 🎵 M4A to MP3 Converter v3.0                │
│                   Python Interactive CLI                    │
└─────────────────────────────────────────────────────────────┘
```

### Beautiful File Table
```
┌─────┬────────────────┬─────────┬────────────┬──────────────┐
│Index│Filename        │Size     │Duration    │Estimated MP3 │
├─────┼────────────────┼─────────┼────────────┼──────────────┤
│1    │my-40mb-file.m4a│40.2MB   │5:30        │~12.8MB       │
│2    │podcast.m4a     │35.8MB   │4:45        │~11.4MB       │
└─────┴────────────────┴─────────┴────────────┴──────────────┘
```

### Advanced Progress Monitoring
```
Converting my-40mb-file.m4a ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 87% 0:00:02
Overall Progress               ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/2 0:00:05
```

## 🎯 Perfect for Your 40MB File

```
Input: podcast.m4a (40.2MB, 5:30 duration)
Process: Analyzes → Calculates 85kbps bitrate → Converts with Rich progress
Output: podcast.mp3 (12.8MB) ✅ UNDER 16MB LIMIT
```

### Key Advantages
- **🔊 Pydub Audio Processing**: Superior audio manipulation
- **📊 Rich Progress Bars**: Beautiful, informative progress display
- **🎯 Smart Compression**: Advanced bitrate optimization
- **🖥️ Platform Independent**: Consistent experience everywhere

## 🛠️ Python Commands

| Command | Description |
|---------|-------------|
| `python convert.py convert` | **Interactive menu** (recommended) |
| `python convert.py batch` | Convert all files in input/ |
| `python convert.py single file.m4a` | Convert single file |
| `python setup.py` | Setup and installation |

## 📊 Conversion Results

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

## 💡 Pro Tips

1. **Large files**: Python handles large audio files exceptionally well
2. **Batch processing**: Rich progress bars show overall and per-file progress
3. **Quality control**: Pydub provides superior audio quality analysis
4. **Cross-platform**: Consistent experience on macOS, Linux, and Windows

## 🎨 Rich CLI Features

- **🎨 Stunning Interface**: Beautiful tables, panels, and progress bars
- **📊 Real-time Statistics**: Live compression ratios and file sizes
- **🎯 Smart Selection**: Interactive file selection with Questionary
- **📈 Detailed Reports**: Comprehensive conversion summaries

## 🔧 Advanced Usage

### Custom Directories
```bash
python convert.py convert --input-dir /path/to/m4a/files --output-dir /path/to/output
```

### Integration
```python
from convert import AudioConverter

converter = AudioConverter()
files = converter.find_m4a_files()
results = converter.convert_files(files)
```

---

**🎵 Experience the beauty of Python's audio processing ecosystem!**
