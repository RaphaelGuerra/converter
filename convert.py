#!/usr/bin/env python3
"""
🎵 M4A to MP3 Converter with Interactive CLI
Python version with visual monitoring and smart compression
"""

import subprocess
from pathlib import Path
from typing import List, Dict

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

import ffmpeg
from pydub import AudioSegment

# Initialize Rich console
console = Console()

class AudioConverter:
    """Main audio converter class with visual feedback and quality options"""

    # Quality levels with compression factors
    QUALITY_LEVELS = {
        'small': {
            'name': 'Small File (High Compression)',
            'compression_factor': 0.7,  # 30% of original size target
            'description': 'Maximum compression, smaller file size',
            'use_case': 'Mobile, web, storage constrained',
            'quality': 'Good',
            'bitrate_range': '48-96 kbps'
        },
        'medium': {
            'name': 'Medium File (Balanced)',
            'compression_factor': 0.8,  # 20% of original size target
            'description': 'Balanced size and quality',
            'use_case': 'General use, podcasts, music',
            'quality': 'Very Good',
            'bitrate_range': '64-160 kbps'
        },
        'large': {
            'name': 'Large File (High Quality)',
            'compression_factor': 0.9,  # 10% of original size target
            'description': 'High quality, larger file size',
            'use_case': 'Archiving, high-fidelity audio',
            'quality': 'Excellent',
            'bitrate_range': '96-256 kbps'
        }
    }

    def __init__(self, input_dir: str = "input", output_dir: str = "output", quality: str = "medium"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.quality = quality
        self.max_size_mb = 16
        self.max_size_bytes = self.max_size_mb * 1024 * 1024
        self.compression_factor = self.QUALITY_LEVELS[quality]['compression_factor']

        # Ensure directories exist
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)

    def show_welcome(self):
        """Display simple welcome banner"""
        console.print("[bold blue]🎵 M4A to MP3 Converter[/bold blue] [dim]v3.0[/dim]")
        console.print("[green]Smart compression under 16MB[/green]")
        console.print()

    def check_ffmpeg(self) -> bool:
        """Verify ffmpeg is available before processing."""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            console.print("[red]❌ FFmpeg not found. Please install it first.[/red]")
            console.print("[dim]macOS: brew install ffmpeg[/dim]")
            console.print("[dim]Ubuntu/Debian: sudo apt install ffmpeg[/dim]")
            return False

    def find_m4a_files(self) -> List[Path]:
        """Find all M4A files in input directory"""
        return list(self.input_dir.glob("*.m4a"))

    def get_audio_info(self, file_path: Path) -> Dict:
        """Get audio file information using pydub"""
        try:
            audio = AudioSegment.from_file(str(file_path), format="m4a")
            duration_seconds = len(audio) / 1000
            file_size = file_path.stat().st_size

            return {
                'duration': duration_seconds,
                'size': file_size,
                'channels': audio.channels,
                'frame_rate': audio.frame_rate,
                'sample_width': audio.sample_width
            }
        except Exception as e:
            console.print(f"[red]Error reading {file_path.name}: {e}[/red]")
            return {
                'duration': 0,
                'size': file_path.stat().st_size,
                'channels': 2,
                'frame_rate': 44100,
                'sample_width': 2
            }

    def calculate_optimal_bitrate(self, duration_seconds: float) -> int:
        """Calculate optimal bitrate based on selected quality level"""
        # Apply compression factor to target size
        target_bytes = int(self.max_size_bytes * self.compression_factor)
        bitrate_bps = (target_bytes * 8) / duration_seconds
        bitrate_kbps = int(bitrate_bps / 1000)

        # Quality-specific bitrate ranges
        quality_ranges = {
            'small': (48, 96),
            'medium': (64, 160),
            'large': (96, 256)
        }

        min_bitrate, max_bitrate = quality_ranges[self.quality]
        return max(min_bitrate, min(max_bitrate, bitrate_kbps))

    def show_quality_info(self):
        """Display information about all quality levels"""
        console.print("\n[bold]🎵 Quality Levels & Compression Options:[/bold]")
        console.print()

        for key, level in self.QUALITY_LEVELS.items():
            current = " ← [green]CURRENT[/green]" if key == self.quality else ""
            console.print(f"[bold cyan]{key.upper()}: {level['name']}[/bold cyan]{current}")
            console.print(f"  [yellow]📏 Target Size:[/yellow] ~{int(self.max_size_mb * level['compression_factor'])}MB ({int((1-level['compression_factor'])*100)}% compression)")
            console.print(f"  [yellow]🎯 Quality:[/yellow] {level['quality']}")
            console.print(f"  [yellow]🎵 Bitrate:[/yellow] {level['bitrate_range']}")
            console.print(f"  [yellow]📱 Use Case:[/yellow] {level['use_case']}")
            console.print(f"  [yellow]📝 Note:[/yellow] {level['description']}")
            console.print()

    def select_quality(self) -> str:
        """Let user select compression quality level"""
        console.print("\n[bold]🎯 Select Compression Quality:[/bold]")
        console.print("  [S] Small File (High Compression) - ~11MB, Good quality")
        console.print("  [M] Medium File (Balanced) - ~13MB, Very Good quality")
        console.print("  [L] Large File (High Quality) - ~14MB, Excellent quality")
        console.print()

        try:
            choice = input("Choose quality [S/M/L] or press Enter for Medium: ").strip().lower()
        except KeyboardInterrupt:
            console.print("\n[yellow]→ Using Medium quality (default)[/yellow]")
            return "medium"

        if choice in ['s', 'small']:
            return "small"
        elif choice in ['l', 'large']:
            return "large"
        else:
            return "medium"  # Default

    def update_quality(self, quality: str):
        """Update converter quality settings"""
        if quality in self.QUALITY_LEVELS:
            self.quality = quality
            self.compression_factor = self.QUALITY_LEVELS[quality]['compression_factor']
            console.print(f"[green]→ Quality set to: {self.QUALITY_LEVELS[quality]['name']}[/green]")
        else:
            console.print("[red]❌ Invalid quality level[/red]")

    def show_files(self, files: List[Path]) -> None:
        """Show files in a clean, simple list"""
        console.print(f"[bold]📁 Found {len(files)} M4A file(s):[/bold]")
        console.print()

        for i, file_path in enumerate(files, 1):
            info = self.get_audio_info(file_path)
            size_mb = info['size'] / (1024 * 1024)

            # Format duration
            if info['duration'] > 0:
                minutes = int(info['duration'] // 60)
                seconds = int(info['duration'] % 60)
                duration_str = f"{minutes}:{seconds:02d}"
            else:
                duration_str = "Unknown"

            # Estimate MP3 size based on selected quality
            if info['duration'] > 0:
                bitrate = self.calculate_optimal_bitrate(info['duration'])
                estimated_seconds = info['duration']
                estimated_bytes = (bitrate * 1000 * estimated_seconds) / 8
                estimated_mp3_mb = estimated_bytes / (1024 * 1024)
                estimated_str = f"~{estimated_mp3_mb:.1f}MB"
            else:
                estimated_str = "Unknown"

            console.print(f"  {i}. [cyan]{file_path.name}[/cyan]")
            console.print(f"     [red]{size_mb:.1f}MB[/red] → [green]{estimated_str}[/green] | Duration: [blue]{duration_str}[/blue]")
            console.print()

    def select_files(self, files: List[Path]) -> List[Path]:
        """Enhanced file selection with clear options"""
        if len(files) == 0:
            return []

        if len(files) == 1:
            console.print("[green]→ Converting the file automatically[/green]")
            return files

        # Show selection options clearly
        console.print(f"\n[bold]🎯 File Selection Options:[/bold]")
        console.print("  [A] Convert ALL files")
        console.print("  [S] Select specific files")
        console.print()

        try:
            choice = input("Choose [A]ll or [S]elect? [A/s]: ").strip().lower()
        except KeyboardInterrupt:
            console.print("\n[yellow]→ Cancelled by user[/yellow]")
            return []

        if choice in ['s', 'select']:
            return self.select_specific_files(files)
        else:
            console.print(f"[green]→ Converting all {len(files)} files[/green]")
            return files

    def select_specific_files(self, files: List[Path]) -> List[Path]:
        """Allow user to select specific files by number"""
        console.print(f"\n[bold]📋 Select files to convert:[/bold]")
        console.print("[dim]Enter numbers separated by commas (e.g., 1,2,4 or 1-3,5)[/dim]")
        console.print("[dim]Or press Enter to convert all files[/dim]")
        console.print()

        try:
            selection = input("Files to convert: ").strip()

            # If no selection, convert all
            if not selection:
                console.print("[yellow]→ No selection made, converting all files[/yellow]")
                return files

            # Parse selection (support both comma-separated and ranges)
            selected_files = []
            parts = selection.split(',')

            for part in parts:
                part = part.strip()
                if '-' in part:
                    # Handle ranges like "1-3"
                    try:
                        start, end = map(int, part.split('-'))
                        for idx in range(start-1, end):  # Convert to 0-based indexing
                            if 0 <= idx < len(files):
                                selected_files.append(files[idx])
                    except ValueError:
                        continue
                else:
                    # Handle individual numbers
                    try:
                        idx = int(part) - 1  # Convert to 0-based indexing
                        if 0 <= idx < len(files):
                            selected_files.append(files[idx])
                    except ValueError:
                        continue

            # Remove duplicates while preserving order
            selected_files = list(dict.fromkeys(selected_files))

            if selected_files:
                console.print(f"[green]→ Selected {len(selected_files)} file(s) for conversion[/green]")
                # Show selected files
                for i, file in enumerate(selected_files, 1):
                    console.print(f"  {i}. [cyan]{file.name}[/cyan]")
                return selected_files
            else:
                console.print("[yellow]→ No valid files selected, converting all files[/yellow]")
                return files

        except KeyboardInterrupt:
            console.print("\n[yellow]→ Selection cancelled, converting all files[/yellow]")
            return files

    def show_conversion_settings(self, files: List[Path]) -> None:
        """Show conversion settings (no confirmation needed)"""
        if len(files) == 0:
            return

        total_size = sum(self.get_audio_info(f)['size'] for f in files)
        total_size_mb = total_size / (1024 * 1024)

        # Calculate estimated output based on selected quality
        estimated_total = 0
        for f in files:
            info = self.get_audio_info(f)
            if info['duration'] > 0:
                bitrate = self.calculate_optimal_bitrate(info['duration'])
                estimated_bytes = (bitrate * 1000 * info['duration']) / 8
                estimated_total += estimated_bytes

        estimated_total_mb = estimated_total / (1024 * 1024)

        console.print(f"\n[bold]🚀 Starting conversion of {len(files)} file(s):[/bold]")
        console.print(f"📏 Total input: [red]{total_size_mb:.1f}MB[/red]")
        console.print(f"🎯 Estimated output: [green]{estimated_total_mb:.1f}MB[/green]")
        console.print(f"🎵 Quality Level: [cyan]{self.QUALITY_LEVELS[self.quality]['name']}[/cyan]")
        console.print(f"📁 Output directory: [cyan]{self.output_dir}[/cyan]")
        console.print()

    def convert_file(self, input_path: Path, output_path: Path, progress_callback=None) -> Dict:
        """Convert single file with progress tracking"""
        try:
            # Get audio info
            info = self.get_audio_info(input_path)

            if info['duration'] == 0:
                console.print(f"[red]❌ Cannot determine duration for {input_path.name}[/red]")
                return {'success': False, 'error': 'Unknown duration'}

            # Calculate optimal bitrate
            bitrate = self.calculate_optimal_bitrate(info['duration'])

            # Load audio
            audio = AudioSegment.from_file(str(input_path), format="m4a")

            # Export with compression based on quality level
            vbr_quality = {
                'small': "6",   # Lower quality, higher compression
                'medium': "4",  # Good balance
                'large': "2"    # Higher quality, less compression
            }

            audio.export(
                str(output_path),
                format="mp3",
                bitrate=f"{bitrate}k",
                parameters=["-q:a", vbr_quality[self.quality]]
            )

            # Check output size
            output_size = output_path.stat().st_size
            output_size_mb = output_size / (1024 * 1024)

            return {
                'success': True,
                'input_size': info['size'],
                'output_size': output_size,
                'duration': info['duration'],
                'bitrate': bitrate,
                'compression_ratio': (1 - output_size / info['size']) * 100
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def convert_files(self, files: List[Path]) -> List[Dict]:
        """Convert all selected files with clean progress monitoring"""
        results = []

        # Show simple progress bar for overall conversion
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(complete_style="green", finished_style="green"),
            TextColumn("[bold yellow]{task.completed}/{task.total} files"),
            TimeRemainingColumn(),
            console=console,
            refresh_per_second=4
        ) as progress:

            overall_task = progress.add_task("Converting files", total=len(files))

            for file_path in files:
                filename = file_path.name
                output_path = self.output_dir / f"{file_path.stem}.mp3"

                # Update progress description with current file
                progress.update(overall_task, description=f"Converting: {filename}")

                # Convert file (without verbose output)
                result = self.convert_file(file_path, output_path)

                if result['success']:
                    output_size_mb = result['output_size'] / (1024 * 1024)
                    status = "OK" if result['output_size'] <= int(self.max_size_bytes * self.compression_factor) else "OVER_LIMIT"

                    results.append({
                        'filename': filename,
                        'input_size': result['input_size'],
                        'output_size': result['output_size'],
                        'duration': result['duration'],
                        'bitrate': result['bitrate'],
                        'compression_ratio': result['compression_ratio'],
                        'status': status
                    })
                else:
                    results.append({
                        'filename': filename,
                        'error': result['error'],
                        'status': 'FAILED'
                    })

                # Update progress
                progress.update(overall_task, advance=1)

        return results

    def show_summary(self, results: List[Dict]):
        """Show clean conversion summary"""
        successful = [r for r in results if 'error' not in r]
        failed = [r for r in results if 'error' in r]

        console.print(f"\n[bold green]🎉 Conversion Complete![/bold green]")

        if successful:
            total_original = sum(r['input_size'] for r in successful)
            total_converted = sum(r['output_size'] for r in successful)
            total_original_mb = total_original / (1024 * 1024)
            total_converted_mb = total_converted / (1024 * 1024)
            total_compression = (1 - total_converted / total_original) * 100 if total_original > 0 else 0

            console.print(f"[green]✅ Successfully converted: {len(successful)} file(s)[/green]")
            console.print(f"📊 Total saved: [green]{total_compression:.1f}%[/green] ([red]{total_original_mb:.1f}MB[/red] → [blue]{total_converted_mb:.1f}MB[/blue])")

            # Show individual results for failed files only
            if len(successful) <= 5:
                for result in successful:
                    converted_mb = result['output_size'] / (1024 * 1024)
                    status = "✅" if result['status'] == 'OK' else "⚠️"
                    console.print(f"  {status} {result['filename']}: [blue]{converted_mb:.1f}MB[/blue]")

        if failed:
            console.print(f"\n[red]❌ Failed conversions: {len(failed)} file(s)[/red]")
            for result in failed:
                console.print(f"  [red]✗ {result['filename']}: {result['error']}[/red]")

    def run(self):
        """Complete conversion process with quality selection"""
        self.show_welcome()

        if not self.check_ffmpeg():
            return

        # Step 1: Quality Selection
        console.print("\n[dim]First, let's choose your compression quality:[/dim]")
        selected_quality = self.select_quality()
        self.update_quality(selected_quality)

        # Optional: Show detailed quality info
        show_info = input("Show detailed quality information? [y/N]: ").strip().lower()
        if show_info == 'y':
            self.show_quality_info()

        # Find M4A files in input directory
        files = self.find_m4a_files()

        if len(files) == 0:
            console.print(f"[yellow]📁 No M4A files found in {self.input_dir}[/yellow]")
            console.print("[dim]Place your .m4a files in the input/ directory and try again.[/dim]")
            return

        # Show files with updated size estimates
        self.show_files(files)

        # Select files (simple process)
        selected_files = self.select_files(files)

        if len(selected_files) == 0:
            console.print("[yellow]No files to convert.[/yellow]")
            return

        # Show settings and convert
        self.show_conversion_settings(selected_files)
        results = self.convert_files(selected_files)
        self.show_summary(results)

        console.print("\n[bold green]🎵 Conversion finished![/bold green]")


def main():
    """Run the interactive M4A to MP3 converter"""
    converter = AudioConverter('input', 'output')
    converter.run()


if __name__ == "__main__":
    main()
