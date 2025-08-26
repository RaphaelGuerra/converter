#!/usr/bin/env python3
"""
🧪 Test script for Python M4A to MP3 Converter
Validates the installation and basic functionality
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required libraries can be imported"""
    print("🔍 Testing Python imports...")

    required_modules = [
        'rich',
        'pydub',
        'ffmpeg',
        'questionary',
        'tqdm',
        'librosa',
        'soundfile'
    ]

    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            missing.append(module)

    return len(missing) == 0, missing

def test_directories():
    """Test directory structure"""
    print("\n📁 Testing directory structure...")

    dirs = ['input', 'output', 'test-files']
    missing_dirs = []

    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/")
            missing_dirs.append(dir_name)

    return len(missing_dirs) == 0, missing_dirs

def test_ffmpeg():
    """Test FFmpeg availability"""
    print("\n🎵 Testing FFmpeg...")

    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'],
                              capture_output=True, text=True, check=True)
        version_line = result.stdout.split('\n')[0]
        print(f"  ✅ FFmpeg available: {version_line}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ❌ FFmpeg not found")
        return False

def test_converter_import():
    """Test if converter can be imported"""
    print("\n📦 Testing converter import...")

    try:
        from convert import AudioConverter
        print("  ✅ AudioConverter imported successfully")
        return True
    except ImportError as e:
        print(f"  ❌ Failed to import AudioConverter: {e}")
        return False

def create_sample_instruction():
    """Create sample instruction file"""
    sample_file = Path("input/README_PLACE_FILES_HERE.txt")
    if not sample_file.exists():
        sample_file.parent.mkdir(exist_ok=True)
        sample_file.write_text("""🎵 M4A to MP3 Converter - Input Directory

Place your .m4a files here to convert them to compressed MP3 files.

Example files:
- my-podcast.m4a
- interview.m4a
- music-recording.m4a

The converter will:
✅ Analyze each file's duration
🎯 Calculate optimal bitrate for <16MB output
🗜️  Convert to high-quality MP3
📊 Show progress and statistics

Run: python ../convert.py convert
""")
        print("📝 Created instruction file in input/ directory")

def main():
    """Run all tests"""
    print("🧪 Python M4A to MP3 Converter - Test Suite")
    print("=" * 50)

    all_passed = True

    # Test Python version
    print(f"🐍 Python version: {sys.version}")
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        return False

    # Test imports
    imports_ok, missing = test_imports()
    if not imports_ok:
        print(f"\n❌ Missing modules: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        all_passed = False

    # Test FFmpeg
    ffmpeg_ok = test_ffmpeg()
    if not ffmpeg_ok:
        all_passed = False

    # Test directories
    dirs_ok, missing_dirs = test_directories()
    if not dirs_ok:
        print(f"\n❌ Missing directories: {', '.join(missing_dirs)}")
        all_passed = False

    # Test converter import
    converter_ok = test_converter_import()
    if not converter_ok:
        all_passed = False

    # Create sample instruction
    create_sample_instruction()

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Ready to convert M4A files.")
        print("\nNext steps:")
        print("  1. Place your .m4a files in the input/ directory")
        print("  2. Run: python convert.py convert")
        print("  3. Follow the interactive menus!")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("Run: python setup.py")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
