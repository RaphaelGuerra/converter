# 🎵 M4A to MP3 Converter v3.0

Convert M4A video files to compressed MP3 audio files under 16MB with **two powerful implementations** featuring interactive CLIs with visual progress monitoring and smart file selection.

## 🚀 Choose Your Version

### Python Edition (Recommended) ⭐
- **🎨 Beautiful CLI**: Rich library provides stunning terminal interfaces
- **🔊 Audio Processing**: Pydub and Librosa offer mature audio processing
- **📊 Rich Progress**: Advanced progress bars with time estimates
- **🎯 Smart Compression**: Intelligent bitrate calculation

### Node.js Edition
- **⚡ Fast Setup**: Quick installation with npm
- **🎮 Interactive**: Full CLI with file selection and progress bars
- **📦 Self-contained**: All dependencies bundled
- **🔧 Mature**: Well-established ecosystem

## 🎯 Quick Start - Python Edition

```bash
# 1. Install FFmpeg
brew install ffmpeg  # macOS
# OR
sudo apt install ffmpeg  # Ubuntu

# 2. Setup Python environment
python setup.py

# 3. Convert your files
python convert.py convert

# 4. Follow the interactive menus!
```

## 🎯 Quick Start - Node.js Edition

```bash
# 1. Install FFmpeg
brew install ffmpeg  # macOS

# 2. Setup Node.js environment
npm run setup

# 3. Convert your files
npm run convert

# 4. Follow the interactive menus!
```

## ✨ New Features in v2.0

- 🎯 **Interactive File Selection** - Choose which files to convert
- 📊 **Visual Progress Bars** - Real-time conversion progress
- 📋 **File Information Table** - View file sizes and estimates
- 🎨 **Colored CLI Output** - Enhanced visual feedback
- ⚡ **Smart Compression** - Automatic bitrate calculation
- 📈 **Conversion Statistics** - Detailed summary reports

## 🚀 Quick Start

### 1. Setup (One-time)

```bash
# Install FFmpeg (required)
brew install ffmpeg  # macOS
# OR
sudo apt install ffmpeg  # Ubuntu/Debian

# Run setup
npm run setup
```

### 2. Add Your M4A Files

```bash
# Copy your .m4a files to the input directory
cp /path/to/your/files/*.m4a ./input/
```

### 3. Convert!

```bash
# Interactive menu (recommended)
npm run convert

# OR command line
npm run convert-cli
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

## 📖 Usage Guide

### Directory Structure

```
decoder/
├── input/          # 📥 Place your .m4a files here
├── output/         # 📤 Converted .mp3 files appear here
├── menu.js         # 🎯 Interactive menu system
├── convert.js      # ⚙️  Command-line converter
└── setup.js        # 🛠️  Setup and installation
```

### Available Commands

| Command | Description |
|---------|-------------|
| `npm run setup` | Initial setup and dependency installation |
| `npm run convert` | **Interactive menu with visual progress** |
| `npm run convert-cli` | Command line interface |
| `npm run convert-current` | Convert files from current directory |
| `npm run convert-single your-file.m4a` | Convert single file |

### Command Line Options

```bash
# Interactive menu (recommended)
npm run convert

# Convert specific directories
node menu.js

# Command line mode
npm run convert-cli input-dir output-dir

# Single file conversion
npm run convert-single input.m4a output.mp3

# Help
node convert.js --help
```

## 🎨 Interactive Menu Walkthrough

### 1. Welcome Screen
```
╔══════════════════════════════════════════════════════════════╗
║                 🎵 M4A to MP3 Converter v2.0                 ║
║                   with Interactive CLI                       ║
╚══════════════════════════════════════════════════════════════╝
```

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
