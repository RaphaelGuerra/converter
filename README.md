# 🎵 M4A to MP3 Converter v3.0

Convert M4A audio files to compressed MP3 files under 16MB with an interactive CLI featuring visual progress monitoring and smart compression algorithms.

## ✨ Key Features

- **🎨 Beautiful CLI**: Rich library provides stunning terminal interfaces with tables and progress bars
- **🔊 Superior Audio Processing**: Pydub and Librosa for mature audio processing
- **📊 Real-time Progress**: Advanced progress bars with time estimates
- **🎯 Smart Compression**: Intelligent bitrate calculation for optimal file sizes
- **📋 Interactive Selection**: Choose specific files or convert all files
- **📈 Detailed Statistics**: Comprehensive conversion summaries

## 🚀 Quick Start

```bash
# 1. Install FFmpeg (required)
brew install ffmpeg  # macOS
# OR
sudo apt install ffmpeg  # Ubuntu/Debian

# 2. Setup Python environment
python setup.py

# 3. Convert your files
python convert.py convert

# 4. Follow the interactive menus!
```

## ✨ New Features in v2.0

- 🎯 **Interactive File Selection** - Choose which files to convert
- 📊 **Visual Progress Bars** - Real-time conversion progress
- 📋 **File Information Table** - View file sizes and estimates
- 🎨 **Colored CLI Output** - Enhanced visual feedback
- ⚡ **Smart Compression** - Automatic bitrate calculation
- 📈 **Conversion Statistics** - Detailed summary reports

## 📖 Usage Guide

### Directory Structure

```
converter/
├── input/          # 📥 Place your .m4a files here
├── output/         # 📤 Converted .mp3 files appear here
├── convert.py      # ⚙️  Main converter application
├── setup.py        # 🛠️  Setup and installation
├── test_python.py  # 🧪 Test script
└── requirements.txt # 📦 Python dependencies
```

### Available Commands

| Command | Description |
|---------|-------------|
| `python setup.py` | Initial setup and dependency installation |
| `python convert.py convert` | **Interactive menu with visual progress** ⭐ |
| `python convert.py batch` | Convert all files in input directory |
| `python convert.py single file.m4a` | Convert single file |
| `python test_python.py` | Test installation and dependencies |

### Command Line Examples

```bash
# Interactive menu (recommended)
python convert.py convert

# Convert all files in input directory
python convert.py batch

# Convert single file
python convert.py single my-file.m4a

# Show help
python convert.py --help
```

## 🎯 Interactive Mode Features

### Visual File Selection
- **File Browser**: View all available M4A files in a table
- **Smart Selection**: Choose all files or pick specific ones
- **Size Estimates**: See original and estimated output sizes
- **Batch Processing**: Convert multiple files with progress tracking

### Real-time Monitoring
- **Progress Bars**: Visual progress for each conversion
- **ETA Display**: Estimated time remaining
- **File Statistics**: Size, bitrate, compression ratio
- **Status Indicators**: Success/failure status for each file

### Enhanced Feedback
- **Colored Output**: Easy-to-read status messages
- **Detailed Summary**: Comprehensive conversion statistics
- **Error Handling**: Clear error messages and recovery suggestions

## 🎨 Interactive Menu Walkthrough

### 1. Welcome Screen
```
╔══════════════════════════════════════════════════════════════╗
║                 🎵 M4A to MP3 Converter v3.0                ║
║                   Python Interactive CLI                     ║
╚══════════════════════════════════════════════════════════════╝
```

### 2. File Selection Table
```
📋 Available M4A Files:

┌─────┬────────────────┬─────────┬────────────┬──────────────┐
│Index│Filename        │Size     │Duration    │Estimated MP3 │
├─────┼────────────────┼─────────┼────────────┼──────────────┤
│1    │sample1.m4a     │40.2MB   │5:30        │~12.8MB       │
│2    │sample2.m4a     │35.8MB   │4:15        │~11.4MB       │
└─────┴────────────────┴─────────┴────────────┴──────────────┘
```

### 3. Selection Options
- ✅ **Convert ALL files** - Process everything
- 📂 **Select specific files** - Choose individual files
- ❌ **Cancel** - Exit the program

### 4. Conversion Progress
```
🎵 Converting: sample1.m4a
✅ Duration: 5:30
🎯 Target bitrate: 85kbps
📏 Target size: Under 16MB

Converting sample1.m4a ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 87% 0:00:02
Overall Progress       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/2 0:00:05
```

### 5. Conversion Summary

## 🔧 Technical Details

### Smart Compression Algorithm

The converter automatically calculates the optimal bitrate using:

```
bitrate = (target_bytes × 8) ÷ (duration_seconds × 1000)
target_bytes = 12.8MB (conservative estimate accounting for MP3 overhead)
```

This ensures files stay under 16MB while maintaining good quality.

### 2. File Selection Table
```
📋 Available M4A Files:

┌─────┬────────────────┬─────────┬────────────┬──────────────┐
│Index│Filename        │Size     │Duration    │Estimated MP3 │
├─────┼────────────────┼─────────┼────────────┼──────────────┤
│1    │sample1.m4a     │40.2MB   │Calculating │~12.8MB       │
│2    │sample2.m4a     │35.8MB   │Calculating │~11.4MB       │
└─────┴────────────────┴─────────┴────────────┴──────────────┘
```

### 3. Selection Options
- ✅ **Convert ALL files** - Process everything
- 📂 **Select specific files** - Choose individual files
- ❌ **Cancel** - Exit the program

### 4. Conversion Progress
```
🎵 Converting: sample1.m4a
✅ Duration: 240s
🎯 Target bitrate: 85kbps
📏 Target size: Under 16MB

██████████████████████████████░░░░░ 87% | ETA: 5s | 87/100
```

### 5. Conversion Summary
```
════════════════════════════════════════════════════════════
🎉 CONVERSION SUMMARY
════════════════════════════════════════════════════════════

┌────────────────┬──────────────┬──────────────┬────────────┬────────┐
│File            │Original Size │Converted Size│Compression │Status  │
├────────────────┼──────────────┼──────────────┼────────────┬────────┤
│sample1.mp3     │40.2MB        │12.8MB        │68.2%       │✅ OK    │
│sample2.mp3     │35.8MB        │11.4MB        │68.2%       │✅ OK    │
└────────────────┴──────────────┼──────────────┼────────────┼────────┘

📈 OVERALL STATISTICS:
📊 Total Files: 2
📏 Original Size: 76.0MB
📏 Converted Size: 24.2MB
🗜️  Total Compression: 68.2%
```

## 🔧 Technical Details

### Smart Compression Algorithm

The converter automatically calculates the optimal bitrate using:

```
bitrate = (16MB × 8) ÷ (duration_seconds × 1000)
```

This ensures files stay under 16MB while maintaining good quality.

### Supported Formats

- **Input**: M4A (AAC), MP4 (with audio), most audio formats
- **Output**: MP3 (stereo, 44.1kHz sample rate)
- **Bitrate Range**: 64-320 kbps (automatically optimized)

### File Size Handling

- **Small files** (< 16MB): Converted at higher quality
- **Large files** (> 16MB): Compressed to meet size limit
- **Very large files**: May need manual bitrate adjustment

## 🛠️ Troubleshooting

### FFmpeg Issues
```bash
# Check FFmpeg installation
ffmpeg -version

# Install FFmpeg
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Ubuntu
```

### Large Output Files
If files exceed 16MB:
1. Use shorter audio clips
2. Run setup again to update dependencies
3. Check the conversion summary for details

### Permission Errors
```bash
# Ensure write permissions
chmod 755 ./output/
```

### Interactive Menu Not Working
```bash
# Force reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

## 📊 Example Workflow

```bash
# 1. Setup
npm run setup

# 2. Add files
cp ~/Downloads/*.m4a ./input/

# 3. Convert interactively
npm run convert
# → Select files from menu
# → Watch progress bars
# → View summary

# 4. Check results
ls -la ./output/
```

## 🎯 Perfect for

- **Podcasters**: Convert long interviews under size limits
- **Content Creators**: Optimize audio for web/mobile
- **Archivists**: Batch convert large audio collections
- **Developers**: Automated audio processing workflows

## 📝 Version History

### v2.0 - Interactive CLI
- ✨ Interactive file selection menu
- 📊 Visual progress bars and statistics
- 🎨 Enhanced colored output
- 📋 File information tables
- ⚡ Smart compression algorithms

### v1.0 - Basic CLI
- Basic command-line conversion
- Simple progress feedback
- Automatic compression

---

**Made with ❤️ for audio conversion workflows**
