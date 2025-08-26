#!/usr/bin/env python3
"""
🎵 M4A to MP3 Converter with Interactive CLI
Python version with visual monitoring and smart compression
"""

import os
import sys
import time
import math
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, DownloadColumn
from rich.prompt import Confirm, Prompt
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.layout import Layout
from rich.columns import Columns
from rich.align import Align

import ffmpeg
import questionary
from pydub import AudioSegment
from tqdm import tqdm

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
        """Display welcome banner"""
        welcome = Panel.fit(
            "[bold blue]🎵 M4A to MP3 Converter[/bold blue]\n"
            "[dim]Python version with Interactive CLI[/dim]\n"
            "[green]Smart compression under 16MB[/green]",
            title="🎯 Audio Converter v3.0",
            border_style="blue"
        )
        console.print(welcome)
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
        """Calculate optimal bitrate for 16MB target"""
        target_bytes = self.max_size_bytes
        bitrate_bps = (target_bytes * 8) / duration_seconds
        bitrate_kbps = int(bitrate_bps / 1000)

        # Constrain to reasonable range
        return max(64, min(320, bitrate_kbps))

    def create_file_table(self, files: List[Path]) -> Table:
        """Create a beautiful table of available files"""
        table = Table(title="📋 Available M4A Files", show_header=True, header_style="bold cyan")
        table.add_column("Index", style="yellow", justify="right")
        table.add_column("Filename", style="white", no_wrap=True)
        table.add_column("Size", style="red", justify="right")
        table.add_column("Duration", style="blue", justify="right")
        table.add_column("Est. MP3", style="green", justify="right")

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
                bitrate = self.calculate_optimal_bitrate(info['duration'])
                estimated_mp3_mb = min(size_mb * 0.3, 15.0)
                estimated_str = f"~{estimated_mp3_mb:.1f}MB"
            else:
                estimated_str = "Unknown"

            table.add_row(
                str(i),
                file_path.name,
                f"{size_mb:.1f}MB",
                duration_str,
                estimated_str
            )

        return table

    def select_files(self, files: List[Path]) -> List[Path]:
        """Interactive file selection"""
        if len(files) == 0:
            return []

        console.print("\n[bold]File Selection Options:[/bold]")

        choices = [
            {"name": "✅ Convert ALL files", "value": "all"},
            {"name": "📂 Select specific files", "value": "select"},
            {"name": "❌ Cancel", "value": "cancel"}
        ]

        choice = questionary.select(
            "What would you like to do?",
            choices=[c["name"] for c in choices],
            default="✅ Convert ALL files"
        ).ask()

        if choice == "❌ Cancel" or choice is None:
            return []

        if choice == "✅ Convert ALL files":
            return files

        # Multi-select specific files
        file_choices = []
        for i, file_path in enumerate(files, 1):
            info = self.get_audio_info(file_path)
            size_mb = info['size'] / (1024 * 1024)
            file_choices.append({
                "name": f"{i}. {file_path.name} ({size_mb:.1f}MB → ~{min(size_mb * 0.3, 15.0):.1f}MB)",
                "value": file_path
            })

        selected = questionary.checkbox(
            "Select files to convert:",
            choices=[c["name"] for c in file_choices]
        ).ask()

        if not selected:
            return []

        # Map back to file paths
        selected_files = []
        for choice_name in selected:
            for choice in file_choices:
                if choice["name"] == choice_name:
                    selected_files.append(choice["value"])
                    break

        return selected_files

    def show_conversion_settings(self, files: List[Path]) -> bool:
        """Show conversion settings and confirm"""
        if len(files) == 0:
            return False

        total_size = sum(self.get_audio_info(f)['size'] for f in files)
        total_size_mb = total_size / (1024 * 1024)

        estimated_total = sum(min(self.get_audio_info(f)['size'] * 0.3, 15 * 1024 * 1024) for f in files)
        estimated_total_mb = estimated_total / (1024 * 1024)

        console.print("\n[bold]⚙️  Conversion Settings:[/bold]")
        console.print(f"📁 Output Directory: [cyan]{self.output_dir}[/cyan]")
        console.print(f"📊 Files Selected: [yellow]{len(files)}[/yellow]")
        console.print(f"📏 Total Input Size: [red]{total_size_mb:.1f}MB[/red]")
        console.print(f"🎯 Estimated Output: [green]{estimated_total_mb:.1f}MB[/green]")
        console.print(f"🗜️  Target Size Limit: [blue]{self.max_size_mb}MB per file[/blue]")

        return Confirm.ask("\n[bold]Start conversion?[/bold]", default=True)

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

            # Export with compression
            audio.export(
                str(output_path),
                format="mp3",
                bitrate=f"{bitrate}k",
                parameters=["-q:a", "2"]  # High quality VBR
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
        """Convert all selected files with visual progress"""
        results = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TimeRemainingColumn(),
            TextColumn("[bold green]{task.fields[filename] if 'filename' in task.fields else ''}"),
            console=console,
            refresh_per_second=10
        ) as progress:

            overall_task = progress.add_task("Overall Progress", total=len(files))

            for file_path in files:
                filename = file_path.name
                output_path = self.output_dir / f"{file_path.stem}.mp3"

                # File-specific progress
                file_task = progress.add_task(
                    f"Converting {filename}",
                    total=100,
                    filename=filename
                )

                console.print(f"\n[bold cyan]🎵 Converting:[/bold cyan] {filename}")

                # Show file info
                info = self.get_audio_info(file_path)
                duration_str = f"{int(info['duration'] // 60)}:{int(info['duration'] % 60):02d}" if info['duration'] > 0 else "Unknown"
                bitrate = self.calculate_optimal_bitrate(info['duration']) if info['duration'] > 0 else 128

                console.print(f"✅ Duration: [blue]{duration_str}[/blue]")
                console.print(f"🎯 Target bitrate: [green]{bitrate}kbps[/green]")
                console.print(f"📏 Target size: [blue]Under {self.max_size_mb}MB[/blue]")

                # Convert file
                result = self.convert_file(file_path, output_path)

                if result['success']:
                    output_size_mb = result['output_size'] / (1024 * 1024)
                    status = "✅ OK" if result['output_size'] <= self.max_size_bytes else "⚠️  OVER LIMIT"
                    status_color = "green" if result['output_size'] <= self.max_size_bytes else "red"

                    console.print(f"[green]✓[/green] {filename}: [blue]{output_size_mb:.1f}MB[/blue] [{status_color}]{status}[/{status_color}]")

                    results.append({
                        'filename': filename,
                        'input_size': result['input_size'],
                        'output_size': result['output_size'],
                        'duration': result['duration'],
                        'bitrate': result['bitrate'],
                        'compression_ratio': result['compression_ratio'],
                        'status': 'OK' if result['output_size'] <= self.max_size_bytes else 'OVER_LIMIT'
                    })
                else:
                    console.print(f"[red]✗[/red] {filename}: [red]{result['error']}[/red]")
                    results.append({
                        'filename': filename,
                        'error': result['error'],
                        'status': 'FAILED'
                    })

                # Update progress
                progress.update(file_task, completed=100)
                progress.update(overall_task, advance=1)
                progress.remove_task(file_task)

        return results

    def show_summary(self, results: List[Dict]):
        """Show comprehensive conversion summary"""
        successful = [r for r in results if 'error' not in r]
        failed = [r for r in results if 'error' in r]

        console.print(f"\n[bold blue]{'='*60}[/bold blue]")
        console.print("[bold green]🎉 CONVERSION SUMMARY[/bold green]")
        console.print(f"[bold blue]{'='*60}[/bold blue]")

        if successful:
            console.print(f"[green]✅ Successfully converted: {len(successful)} file(s)[/green]")

            # Create results table
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("File", style="white", no_wrap=True)
            table.add_column("Original", style="red", justify="right")
            table.add_column("Converted", style="blue", justify="right")
            table.add_column("Compression", style="yellow", justify="right")
            table.add_column("Status", style="green", justify="center")

            total_original = 0
            total_converted = 0

            for result in successful:
                original_mb = result['input_size'] / (1024 * 1024)
                converted_mb = result['output_size'] / (1024 * 1024)
                compression = result['compression_ratio']
                status = "✅ OK" if result['status'] == 'OK' else "⚠️  OVER"

                table.add_row(
                    result['filename'],
                    f"{original_mb:.1f}MB",
                    f"{converted_mb:.1f}MB",
                    f"{compression:.1f}%",
                    status
                )

                total_original += result['input_size']
                total_converted += result['output_size']

            console.print(table)

            # Overall statistics
            total_original_mb = total_original / (1024 * 1024)
            total_converted_mb = total_converted / (1024 * 1024)
            total_compression = (1 - total_converted / total_original) * 100 if total_original > 0 else 0

            console.print(f"\n[bold]📈 OVERALL STATISTICS:[/bold]")
            console.print(f"📊 Total Files: [yellow]{len(successful)}[/yellow]")
            console.print(f"📏 Original Size: [red]{total_original_mb:.1f}MB[/red]")
            console.print(f"📏 Converted Size: [blue]{total_converted_mb:.1f}MB[/blue]")
            console.print(f"🗜️  Total Compression: [green]{total_compression:.1f}%[/green]")

        if failed:
            console.print(f"[red]❌ Failed conversions: {len(failed)} file(s)[/red]")
            for result in failed:
                console.print(f"  [red]• {result['filename']}: {result['error']}[/red]")

    def run(self):
        """Main interactive loop"""
        while True:
            self.show_welcome()

            # Find M4A files
            files = self.find_m4a_files()

            if len(files) == 0:
                console.print(f"[yellow]📁 No M4A files found in {self.input_dir}[/yellow]")
                console.print("[dim]Place your .m4a files in the input/ directory and run this command again.[/dim]")
                console.print("[dim]Press Ctrl+C to exit\n[/dim]")

                try:
                    if not Confirm.ask("[bold]🔄 Check again for files?[/bold]", default=True):
                        break
                    continue
                except KeyboardInterrupt:
                    break
            else:
                # Show file table
                table = self.create_file_table(files)
                console.print(table)

                # Select files
                selected_files = self.select_files(files)

                if len(selected_files) == 0:
                    console.print("[yellow]👋 No files selected. Goodbye![/yellow]")
                    break

                # Confirm settings
                if not self.show_conversion_settings(selected_files):
                    console.print("[yellow]👋 Conversion cancelled. Goodbye![/yellow]")
                    break

                # Convert files
                results = self.convert_files(selected_files)

                # Show summary
                self.show_summary(results)

                # Continue?
                try:
                    if not Confirm.ask("\n[bold]🔄 Convert more files?[/bold]", default=False):
                        break
                except KeyboardInterrupt:
                    break

        console.print("\n[bold green]🎵 Thank you for using M4A to MP3 Converter![/bold green]")


@click.group()
@click.version_option("3.0.0")
def cli():
    """🎵 M4A to MP3 Converter with Interactive CLI"""
    pass


@cli.command()
@click.option('--input-dir', '-i', default='input', help='Input directory containing M4A files')
@click.option('--output-dir', '-o', default='output', help='Output directory for MP3 files')
def convert(input_dir, output_dir):
    """Interactive file selection and conversion"""
    converter = AudioConverter(input_dir, output_dir)
    converter.run()


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', required=False)
@click.option('--input-dir', '-i', default='input', help='Input directory')
@click.option('--output-dir', '-o', default='output', help='Output directory')
def single(input_file, output_file, input_dir, output_dir):
    """Convert a single M4A file"""
    converter = AudioConverter(input_dir, output_dir)

    input_path = Path(input_file)
    if not output_file:
        output_path = Path(output_dir) / f"{input_path.stem}.mp3"
    else:
        output_path = Path(output_file)

    Path(output_dir).mkdir(exist_ok=True)

    console.print(f"[bold cyan]🎵 Converting single file:[/bold cyan] {input_path.name}")

    result = converter.convert_file(input_path, output_path)

    if result['success']:
        output_size_mb = result['output_size'] / (1024 * 1024)
        status = "✅ OK" if result['output_size'] <= converter.max_size_bytes else "⚠️  OVER LIMIT"

        console.print(f"[green]✓[/green] Conversion complete!")
        console.print(f"📁 Output: [cyan]{output_path.name}[/cyan]")
        console.print(f"📏 Final size: [blue]{output_size_mb:.1f}MB[/blue] [{status}]")
    else:
        console.print(f"[red]❌ Conversion failed: {result['error']}[/red]")


@cli.command()
@click.option('--input-dir', '-i', default='input', help='Input directory')
@click.option('--output-dir', '-o', default='output', help='Output directory')
def batch(input_dir, output_dir):
    """Convert all M4A files in input directory"""
    converter = AudioConverter(input_dir, output_dir)

    files = converter.find_m4a_files()
    if len(files) == 0:
        console.print(f"[yellow]📁 No M4A files found in {input_dir}[/yellow]")
        return

    console.print(f"[bold cyan]🎵 Converting all files from {input_dir}[/bold cyan]")
    results = converter.convert_files(files)
    converter.show_summary(results)


if __name__ == "__main__":
    cli()
