#!/usr/bin/env python3
"""
🎵 M4A to MP3 Converter with Interactive CLI
Python version with visual monitoring and smart compression
"""

import os
import sys
from pathlib import Path
from typing import List, Dict

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, DownloadColumn
from rich.prompt import Confirm
from rich.panel import Panel

import ffmpeg
import questionary
from pydub import AudioSegment

# Initialize Rich console
console = Console()

class AudioConverter:
    """Main audio converter class with visual feedback"""

    def __init__(self, input_dir: str = "input", output_dir: str = "output"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.max_size_mb = 16
        self.max_size_bytes = self.max_size_mb * 1024 * 1024

        # Ensure directories exist
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)

    def show_welcome(self):
        """Display simple welcome banner"""
        console.print("[bold blue]🎵 M4A to MP3 Converter[/bold blue] [dim]v3.0[/dim]")
        console.print("[green]Smart compression under 16MB[/green]")
        console.print()

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
        """Calculate optimal bitrate for ~12.8MB target (conservative compression)"""
        # Reduce target by ~20% to account for MP3 encoding overhead
        target_bytes = int(self.max_size_bytes * 0.8)  # 12.8MB instead of 16MB
        bitrate_bps = (target_bytes * 8) / duration_seconds
        bitrate_kbps = int(bitrate_bps / 1000)

        # Constrain to reasonable range (lower minimum for better compression)
        return max(48, min(256, bitrate_kbps))

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

            # Estimate MP3 size
            if info['duration'] > 0:
                estimated_mp3_mb = min(size_mb * 0.3, 12.8)
                estimated_str = f"~{estimated_mp3_mb:.1f}MB"
            else:
                estimated_str = "Unknown"

            console.print(f"  {i}. [cyan]{file_path.name}[/cyan]")
            console.print(f"     [red]{size_mb:.1f}MB[/red] → [green]{estimated_str}[/green] | Duration: [blue]{duration_str}[/blue]")
            console.print()

    def select_files(self, files: List[Path]) -> List[Path]:
        """Simple file selection - convert all by default"""
        if len(files) == 0:
            return []

        if len(files) == 1:
            console.print("[green]→ Converting the file automatically[/green]")
            return files

        # For multiple files, ask if user wants to select specific ones
        console.print(f"\n[dim]💡 Tip: Press Enter to convert all {len(files)} files, or 's' to select specific files[/dim]")
        try:
            choice = input("Convert [A]ll files or [S]elect specific? [A/s]: ").strip().lower()
        except KeyboardInterrupt:
            console.print("\n[yellow]→ Cancelled by user[/yellow]")
            return []

        if choice in ['s', 'select']:
            # Simple numbered selection
            console.print("\n[dim]Enter file numbers separated by commas (e.g., 1,3,5):[/dim]")
            try:
                selection = input("Files to convert: ").strip()
                if not selection:
                    return files

                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                selected_files = []
                for idx in indices:
                    if 0 <= idx < len(files):
                        selected_files.append(files[idx])

                if selected_files:
                    console.print(f"[green]→ Selected {len(selected_files)} file(s)[/green]")
                    return selected_files
                else:
                    console.print("[yellow]→ No valid files selected, converting all[/yellow]")
                    return files
            except (ValueError, KeyboardInterrupt):
                console.print("[yellow]→ Invalid selection, converting all files[/yellow]")
                return files
        else:
            console.print("[green]→ Converting all files[/green]")
            return files

    def show_conversion_settings(self, files: List[Path]) -> None:
        """Show conversion settings (no confirmation needed)"""
        if len(files) == 0:
            return

        total_size = sum(self.get_audio_info(f)['size'] for f in files)
        total_size_mb = total_size / (1024 * 1024)

        estimated_total = sum(min(self.get_audio_info(f)['size'] * 0.3, 12.8 * 1024 * 1024) for f in files)
        estimated_total_mb = estimated_total / (1024 * 1024)

        console.print(f"\n[bold]🚀 Starting conversion of {len(files)} file(s):[/bold]")
        console.print(f"📏 Total input: [red]{total_size_mb:.1f}MB[/red]")
        console.print(f"🎯 Estimated output: [green]{estimated_total_mb:.1f}MB[/green]")
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

            # Export with compression (optimized for size)
            audio.export(
                str(output_path),
                format="mp3",
                bitrate=f"{bitrate}k",
                parameters=["-q:a", "4"]  # Good quality VBR with better compression
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
                    status = "OK" if result['output_size'] <= int(self.max_size_bytes * 0.8) else "OVER_LIMIT"

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
        """Simple, straightforward conversion process"""
        self.show_welcome()

        # Ask user what they want to do
        console.print()
        console.print("[bold]What would you like to do?[/bold]")
        console.print("  1. [cyan]📁 Convert files from input/ directory[/cyan] (recommended)")
        console.print("  2. [cyan]📄 Convert a single specific file[/cyan]")
        console.print()

        try:
            choice = input("Enter your choice [1/2]: ").strip()
        except KeyboardInterrupt:
            console.print("\n[yellow]👋 Goodbye![/yellow]")
            return

        if choice == "2":
            # Single file conversion
            self.convert_single_file()
        else:
            # Directory conversion (default)
            self.convert_from_directory()

    def convert_single_file(self):
        """Convert a single specific file"""
        console.print("\n[bold]📄 Single File Conversion[/bold]")
        console.print("[dim]Enter the path to your M4A file:[/dim]")

        try:
            file_path = input("File path: ").strip()
        except KeyboardInterrupt:
            console.print("\n[yellow]→ Cancelled[/yellow]")
            return

        if not file_path:
            console.print("[yellow]No file specified.[/yellow]")
            return

        input_path = Path(file_path)
        if not input_path.exists():
            console.print(f"[red]❌ File not found: {file_path}[/red]")
            return

        if input_path.suffix.lower() != '.m4a':
            console.print(f"[red]❌ Not an M4A file: {input_path.suffix}[/red]")
            return

        # Ask for output location
        console.print("[dim]Enter output file path (or press Enter for default):[/dim]")
        try:
            output_path_input = input("Output path: ").strip()
        except KeyboardInterrupt:
            console.print("\n[yellow]→ Cancelled[/yellow]")
            return

        if output_path_input:
            output_path = Path(output_path_input)
        else:
            output_path = Path('output') / f"{input_path.stem}.mp3"

        # Create output directory if needed
        Path('output').mkdir(exist_ok=True)

        console.print(f"\n[bold cyan]🎵 Converting:[/bold cyan] {input_path.name}")

        result = self.convert_file(input_path, output_path)

        if result['success']:
            output_size_mb = result['output_size'] / (1024 * 1024)
            status = "✅ OK" if result['output_size'] <= int(self.max_size_bytes * 0.8) else "⚠️  OVER LIMIT"

            console.print(f"[green]✓[/green] Complete: [blue]{output_size_mb:.1f}MB[/blue] [{status}]")
            console.print(f"📁 Saved to: [cyan]{output_path}[/cyan]")
        else:
            console.print(f"[red]❌ Failed: {result['error']}[/red]")

    def convert_from_directory(self):
        """Convert files from input directory"""
        # Find M4A files
        files = self.find_m4a_files()

        if len(files) == 0:
            console.print(f"[yellow]📁 No M4A files found in {self.input_dir}[/yellow]")
            console.print("[dim]Place your .m4a files in the input/ directory and try again.[/dim]")
            console.print("[dim]Or choose option 2 to convert a specific file.[/dim]")
            return

        # Show files
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
