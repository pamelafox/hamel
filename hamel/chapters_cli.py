"""Generate chapter summaries with timestamps for YouTube videos using Google's Gemini API."""

import os
import typer
from typing import Annotated
from rich.console import Console
from hamel.yt import yt_chapters

app = typer.Typer()
console = Console()

@app.command()
def chapters(
    url: Annotated[str, typer.Argument(help="YouTube video URL")],
):
    """Generate chapter summaries for a YouTube video."""
    if not os.environ.get("GEMINI_API_KEY"): raise typer.Exit("Error: GEMINI_API_KEY environment variable is not set.")
    
    with console.status("[bold blue]Analyzing video...[/bold blue]", spinner="dots"):
        try:
            result = yt_chapters(url)
            if result: print(result)
        except Exception as e: raise typer.Exit(f"Error: {str(e)}")

def main():
    app()
