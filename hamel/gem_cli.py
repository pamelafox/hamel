"""CLI for Google Gemini API interactions via hamel.gem."""

import sys
import os
from typing import Annotated, Optional, List
from pathlib import Path
import typer
from hamel.gem import gem as hamel_gem

app = typer.Typer()

@app.command()
def gem(
    prompt: Annotated[Optional[str], typer.Argument(help="Text prompt (reads from stdin if not provided)")] = None,
    attachments: Annotated[Optional[List[str]], typer.Argument(help="File paths or URLs to analyze")] = None,
    model: Annotated[str, typer.Option("--model", "-m", help="Gemini model to use")] = "gemini-2.5-pro",
    thinking: Annotated[int, typer.Option("--thinking", "-t", help="Thinking budget (-1 for default)")] = -1,
    search: Annotated[bool, typer.Option("--search", "-s", help="Enable grounded Google search")] = False,
):
    """Generate content with Google Gemini API.
    
    Examples:
        ai-gem "Write a haiku"
        ai-gem "Summarize this" document.pdf
        ai-gem "Compare these" file1.pdf file2.png
        echo "Some text" | ai-gem "Analyze this"
    """
    
    if not os.environ.get("GEMINI_API_KEY"):
        raise typer.Exit("Error: GEMINI_API_KEY environment variable not set")
    
    # Get prompt from stdin if not provided as argument
    if prompt is None:
        if sys.stdin.isatty():
            raise typer.Exit("Error: No prompt provided. Use as argument or pipe input via stdin")
        prompt = sys.stdin.read().strip()
        if not prompt:
            raise typer.Exit("Error: Empty input from stdin")
    
    try:
        # Validate file attachments exist
        if attachments:
            for attachment in attachments:
                p = Path(attachment)
                if not p.exists() and not attachment.startswith(('http://', 'https://', 'www.')) and 'youtube.com' not in attachment and 'youtu.be' not in attachment:
                    raise typer.Exit(f"Error: File not found: {attachment}")
        
        # Call hamel.gem with appropriate parameters
        result = hamel_gem(
            prompt=prompt,
            o=attachments if attachments else None,
            model=model,
            thinking=thinking,
            search=search
        )
        
        print(result)
        
    except Exception as e:
        raise typer.Exit(f"Error: {str(e)}")

def main():
    app()
