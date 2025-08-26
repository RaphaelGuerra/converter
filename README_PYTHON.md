# 🎵 M4A to MP3 Converter v3.0 - Python Edition

Convert M4A video files to compressed MP3 audio files under 16MB with a beautiful interactive CLI powered by Python and Rich.

## ✨ Why Python?

- **🎨 Beautiful CLI**: Rich library provides stunning terminal interfaces
- **🔊 Audio Processing**: Pydub and Librosa offer mature audio processing
- **📊 Rich Progress**: Advanced progress bars with time estimates
- **🎯 Smart Compression**: Intelligent bitrate calculation
- **🖥️  Cross-Platform**: Consistent experience across all platforms

## 🚀 Quick Start

### 1. Prerequisites
```bash
# FFmpeg (required for audio processing)
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows: Download from https://ffmpeg.org/download.html
```

### 2. Setup
```bash
# Clone or download the project
cd /path/to/decoder

# Run Python setup
python setup.py
```

### 3. Convert Your Files
```bash
# Interactive mode (recommended)
python convert.py convert

# Batch convert all files
python convert.py batch

# Convert single file
python convert.py single your-file.m4a
```

## 🎨 Interactive Features

### Rich File Selection Table
```
┌─────┬────────────────┬─────────┬────────────┬──────────────┐
│Index│Filename        │Size     │Duration    │Estimated MP3 │
├─────┼────────────────┼─────────┼────────────┼──────────────┤
│1    │my-40mb-file.m4a│40.2MB   │5:30        │~12.8MB       │
│2    │podcast.m4a     │35.8MB   │4:45        │~11.4MB       │
└─────┴────────────────┴─────────┴────────────┴──────────────┘
```

### Advanced Progress Bars
```
🎵 Converting: my-40mb-file.m4a
✅ Duration: 5:30
🎯 Target bitrate: 85kbps
📏 Target size: Under 16MB

Converting my-40mb-file.m4a ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 87% 0:00:02
Overall Progress               ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/2 0:00:05
```

### Interactive Selection
```bash
? What would you like to do? (Use arrow keys)
❯ ✅ Convert ALL files
  📂 Select specific files
  ❌ Cancel
```

## 📖 Command Reference

| Command | Description |
|---------|-------------|
| `python convert.py convert` | **Interactive file selection** |
| `python convert.py batch` | Convert all files in input/ |
| `python convert.py single file.m4a [output.mp3]` | Convert single file |
| `python convert.py --help` | Show help and options |

## 🏗️ Technical Architecture

### Libraries Used
- **Rich**: Beautiful terminal interfaces and progress bars
- **Pydub**: Audio file processing and conversion
- **Librosa**: Advanced audio analysis
- **Questionary**: Interactive prompts and selections
- **FFmpeg-Python**: Direct FFmpeg integration
- **TQDM**: Progress bar utilities

### Smart Compression Algorithm
```python
def calculate_optimal_bitrate(duration_seconds):
    target_bytes = 16 * 1024 * 1024  # 16MB
    bitrate_bps = (target_bytes * 8) / duration_seconds
    bitrate_kbps = bitrate_bps / 1000
    return max(64, min(320, bitrate_kbps))  # Constrain 64-320kbps
```

## 🎯 Perfect for Your Use Case

### 40MB M4A File Example
```
Input: podcast.m4a (40.2MB, 5:30 duration)
Process: Analyzes → Calculates 85kbps bitrate → Converts
Output: podcast.mp3 (12.8MB) ✅ UNDER 16MB LIMIT
```

### Key Benefits
- **Automatic Optimization**: No manual bitrate calculation needed
- **Quality Preservation**: Maintains audio quality while meeting size limits
- **Batch Processing**: Handle multiple files efficiently
- **Visual Feedback**: See progress and results in real-time

## 📊 Conversion Results

### Sample Output
```
════════════════════════════════════════════════════════════
🎉 CONVERSION SUMMARY
════════════════════════════════════════════════════════════

┌────────────────┬──────────────┬──────────────┬────────────┬────────┐
│File            │Original Size │Converted Size│Compression │Status  │
├────────────────┼──────────────┼──────────────┼────────────┼────────┤
│podcast.mp3     │40.2MB        │12.8MB        │68.2%       │✅ OK    │
│interview.mp3   │35.8MB        │11.4MB        │68.2%       │✅ OK    │
└────────────────┴──────────────┼──────────────┼────────────┼────────┘

📈 OVERALL STATISTICS:
📊 Total Files: 2
📏 Original Size: 76.0MB
📏 Converted Size: 24.2MB
🗜️  Total Compression: 68.2%
```

## 🛠️ Advanced Usage

### Custom Directories
```bash
# Specify custom input/output directories
python convert.py convert --input-dir /path/to/m4a/files --output-dir /path/to/output

# Batch convert from specific directory
python convert.py batch --input-dir my-recordings
```

### Integration with Scripts
```python
from convert import AudioConverter

converter = AudioConverter(input_dir="input", output_dir="output")
files = converter.find_m4a_files()
results = converter.convert_files(files)
converter.show_summary(results)
```

## 🔧 Troubleshooting

### Common Issues

**FFmpeg not found**
```bash
# Check installation
ffmpeg -version

# Install (macOS)
brew install ffmpeg

# Install (Ubuntu)
sudo apt install ffmpeg
```

**Python dependencies missing**
```bash
# Reinstall requirements
pip install -r requirements.txt
```

**Audio file errors**
```bash
# Check file format
file your-file.m4a

# Convert problem files individually
python convert.py single problem-file.m4a
```

### Performance Tips

- **Large files**: Consider splitting long recordings before conversion
- **Batch processing**: Process files in smaller batches for better monitoring
- **Disk space**: Ensure sufficient space in output directory

## 📈 Performance Comparison

| Feature | Node.js Version | Python Version |
|---------|----------------|----------------|
| **CLI Beauty** | Good (chalk) | **Excellent** (Rich) |
| **Audio Processing** | Good | **Excellent** (Librosa) |
| **Progress Bars** | Good | **Excellent** (Rich) |
| **File Selection** | Good | **Excellent** (Questionary) |
| **Cross-platform** | Good | **Excellent** |
| **Dependencies** | More complex | **Simpler** |

## 🎨 Rich CLI Examples

### Welcome Screen
```
┌─────────────────────────────────────────────────────────────┐
│                 🎵 M4A to MP3 Converter v3.0                │
│                   Python Interactive CLI                    │
└─────────────────────────────────────────────────────────────┘
```

### Progress with Multiple Bars
```
Converting podcast.m4a         ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 87% 0:00:02
Overall Progress               ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/2 0:00:05
```

### Statistics Panel
```
📈 OVERALL STATISTICS:
📊 Total Files: 5
📏 Original Size: 180.5MB
📏 Converted Size: 57.3MB
🗜️  Total Compression: 68.3%
```

## 🤝 Contributing

### Adding New Features
1. **Audio formats**: Extend support for more input formats
2. **Compression algorithms**: Implement different compression strategies
3. **UI themes**: Add different Rich themes and styles
4. **Batch operations**: Add parallel processing capabilities

### Code Structure
```
convert.py       # Main CLI application
├── AudioConverter class
├── File selection methods
├── Conversion logic
└── Progress monitoring

setup.py         # Installation and setup
requirements.txt # Python dependencies
```

## 📝 Version History

### v3.0 - Python Edition
- ✨ Complete rewrite in Python
- 🎨 Rich CLI with beautiful interfaces
- 🔊 Advanced audio processing with Pydub/Librosa
- 📊 Enhanced progress monitoring
- 🎯 Smart compression algorithms
- 🖥️  Cross-platform compatibility

### v2.0 - Node.js Interactive
- 🎮 Interactive file selection
- 📊 Visual progress bars
- ⚡ Smart compression

---

**🎵 Powered by Python's excellent audio ecosystem**
