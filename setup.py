#!/usr/bin/env python3
"""
🎵 M4A to MP3 Converter - Python Setup Script
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm
except ImportError:
    print("❌ Rich library not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], check=True)
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm

console = Console()

class SetupManager:
    """Manages the setup process for the M4A to MP3 converter"""

    def __init__(self):
        self.project_root = Path(__file__).parent

    def show_welcome(self):
        """Show welcome message"""
        welcome = Panel.fit(
            "[bold blue]🎵 M4A to MP3 Converter[/bold blue]\n"
            "[dim]Python version with Interactive CLI[/dim]\n"
            "[green]Smart compression under 16MB[/green]",
            title="🚀 Python Setup v3.0",
            border_style="blue"
        )
        console.print(welcome)
        console.print()

    def check_python_version(self):
        """Check if Python version is compatible"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            console.print("[red]❌ Python 3.7+ is required[/red]")
            console.print(f"[yellow]Current version: {version.major}.{version.minor}[/yellow]")
            return False

        console.print(f"[green]✅ Python {version.major}.{version.minor}.{version.micro} detected[/green]")
        return True

    def check_ffmpeg(self):
        """Check if FFmpeg is installed"""
        try:
            result = subprocess.run(['ffmpeg', '-version'],
                                  capture_output=True, text=True, check=True)
            # Extract version from first line
            first_line = result.stdout.split('\n')[0]
            console.print(f"[green]✅ FFmpeg installed:[/green] {first_line}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            console.print("[red]❌ FFmpeg not found[/red]")
            return False

    def show_ffmpeg_installation_guide(self):
        """Show platform-specific FFmpeg installation instructions"""
        system = platform.system().lower()

        console.print("\n[bold yellow]📦 FFmpeg Installation Guide:[/bold yellow]")

        if system == "darwin":  # macOS
            console.print("[cyan]macOS:[/cyan]")
            console.print("  brew install ffmpeg")
        elif system == "linux":
            console.print("[cyan]Ubuntu/Debian:[/cyan]")
            console.print("  sudo apt update && sudo apt install ffmpeg")
            console.print("[cyan]CentOS/RHEL:[/cyan]")
            console.print("  sudo yum install ffmpeg")
        elif system == "windows":
            console.print("[cyan]Windows:[/cyan]")
            console.print("  Download from: https://ffmpeg.org/download.html")
            console.print("  Add to PATH: C:\\ffmpeg\\bin")
        else:
            console.print(f"[cyan]{system}:[/cyan]")
            console.print("  Visit: https://ffmpeg.org/download.html")

        console.print("\n[yellow]After installing FFmpeg, run this setup script again.[/yellow]")

    def install_python_dependencies(self):
        """Install Python dependencies"""
        requirements_file = self.project_root / "requirements.txt"

        if not requirements_file.exists():
            console.print("[red]❌ requirements.txt not found![/red]")
            return False

        console.print("[bold blue]📦 Installing Python dependencies...[/bold blue]")

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold green]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Installing packages...", total=None)

            try:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
                ], capture_output=True, text=True, check=True)

                progress.update(task, completed=True)
                console.print("[green]✅ All dependencies installed successfully![/green]")
                return True

            except subprocess.CalledProcessError as e:
                progress.update(task, completed=True)
                console.print("[red]❌ Failed to install dependencies[/red]")
                console.print(f"[red]Error: {e.stderr}[/red]")
                return False

    def create_directories(self):
        """Create necessary directories"""
        directories = [
            self.project_root / "input",
            self.project_root / "output",
            self.project_root / "test-files"
        ]

        console.print("[bold blue]📁 Creating directories...[/bold blue]")

        created_count = 0
        for directory in directories:
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
                console.print(f"  [green]📁 Created:[/green] {directory.name}/")
                created_count += 1
            else:
                console.print(f"  [blue]📁 Exists:[/blue] {directory.name}/")

        if created_count > 0:
            console.print(f"[green]✅ Created {created_count} directories[/green]")
        else:
            console.print("[blue]📁 All directories already exist[/blue]")

        # Show directory structure
        console.print("\n[bold cyan]📂 Project Structure:[/bold cyan]")
        console.print("  [cyan]input/[/cyan]     → Place your .m4a files here")
        console.print("  [cyan]output/[/cyan]    → Converted .mp3 files appear here")
        console.print("  [cyan]test-files/[/cyan] → Test files directory")

    def show_next_steps(self):
        """Show next steps after successful setup"""
        console.print("\n[bold green]🎯 Next Steps:[/bold green]")
        console.print("  1. [yellow]Place your .m4a files in the input/ directory[/yellow]")
        console.print("  2. [yellow]Run: python convert.py convert[/yellow]")
        console.print("  3. [yellow]Or run: python convert.py --help[/yellow]")
        console.print("  4. [yellow]Find your MP3s in the output/ directory[/yellow]")

        console.print("\n[bold cyan]📚 Available Commands:[/bold cyan]")
        console.print("  [cyan]python convert.py convert[/cyan]       → Interactive menu")
        console.print("  [cyan]python convert.py batch[/cyan]         → Convert all files")
        console.print("  [cyan]python convert.py single file.m4a[/cyan] → Convert one file")
        console.print("  [cyan]python convert.py --help[/cyan]        → Show help")

    def create_sample_file(self):
        """Create a sample instruction file"""
        sample_file = self.project_root / "input" / "README_PLACE_FILES_HERE.txt"

        if not sample_file.exists():
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
            console.print("[blue]📝 Created instruction file in input/ directory[/blue]")

    def run_setup(self):
        """Run the complete setup process"""
        self.show_welcome()

        console.print("[bold]🚀 Setting up M4A to MP3 Converter (Python)...\n[/bold]")

        # Check Python version
        if not self.check_python_version():
            return False

        # Check FFmpeg
        ffmpeg_ok = self.check_ffmpeg()
        if not ffmpeg_ok:
            self.show_ffmpeg_installation_guide()
            console.print("\n[red]❌ Setup incomplete - FFmpeg required[/red]")
            return False

        # Install Python dependencies
        if not self.install_python_dependencies():
            return False

        # Create directories
        self.create_directories()

        # Create sample instruction
        self.create_sample_file()

        # Final success message
        console.print("\n[bold green]🎉 Python Setup Complete![/bold green]")
        self.show_next_steps()

        console.print(f"\n[bold blue]{'='*60}[/bold blue]")
        console.print("[bold]Ready to convert your M4A files![/bold]")
        console.print("[dim]Just run: python convert.py convert[/dim]")

        return True


def main():
    """Main setup function"""
    try:
        setup = SetupManager()
        success = setup.run_setup()

        if success:
            console.print("\n[green]🎵 Happy converting![/green]")
        else:
            console.print("\n[red]❌ Setup failed. Please resolve the issues above.[/red]")
            sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Setup cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]💥 Setup error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
