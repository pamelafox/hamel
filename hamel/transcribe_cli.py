"""Download YouTube video transcripts and output to stdout."""

from typing import Annotated
import typer
from hamel.yt import transcribe as hamel_transcribe

app = typer.Typer()

@app.command()
def transcribe(
    url: Annotated[str, typer.Argument(help="YouTube video URL or video ID")],
    seconds_only: Annotated[bool, typer.Option("--seconds", "-s", help="Show timestamps in seconds instead of HH:MM:SS")] = False,
):
    """Download YouTube transcript and output to stdout."""
    try:
        transcript_text = hamel_transcribe(url, seconds_only=seconds_only)
        print(transcript_text)
    except Exception as e: raise typer.Exit(f"Error: {str(e)}")

def main():
    app()
