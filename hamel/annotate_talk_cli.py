"""Generate annotated blog posts from technical talks with slides and video."""

import os
from fastcore.utils import Path
from typing import Optional, Annotated
import typer
from rich.console import Console
from hamel.writing import generate_annotated_talk_post

app = typer.Typer()
console = Console()

@app.command()
def annotate_talk(
    youtube_url: Annotated[str, typer.Argument(help="YouTube video URL")],
    slide_pdf: Annotated[Path, typer.Argument(help="Path to PDF slides")],
    image_dir: Annotated[str, typer.Argument(help="Output directory for slide images")],
    transcript: Annotated[Optional[Path], typer.Option("--transcript", "-t", help="Path to transcript file (optional)")] = None,
    output: Annotated[Optional[Path], typer.Option("--output", "-o", help="Output file path (defaults to stdout)")] = None,
    prompt_file: Annotated[Optional[Path], typer.Option("--prompt", "-p", help="Path to file with additional context/instructions")] = None,
):
    """Generate an annotated blog post from a technical talk with slides."""
    
    if not os.environ.get("GEMINI_API_KEY"): raise typer.Exit("Error: GEMINI_API_KEY environment variable is not set.")
    if not os.environ.get("JINA_READER_KEY"): raise typer.Exit("Error: JINA_READER_KEY environment variable is not set.")
    if not slide_pdf.exists(): raise typer.Exit(f"Error: Slide PDF not found: {slide_pdf}")
    if transcript and not transcript.exists(): raise typer.Exit(f"Error: Transcript file not found: {transcript}")
    if prompt_file and not prompt_file.exists(): raise typer.Exit(f"Error: Prompt file not found: {prompt_file}")
    
    Path(image_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        console.print(f"[bold green]Generating annotated post for:[/bold green] {youtube_url}")
        console.print(f"[bold]Slides:[/bold] {slide_pdf}")
        console.print(f"[bold]Images will be saved to:[/bold] {image_dir}/")
        
        user_prompt = Path(prompt_file).read_text() if prompt_file else None
        
        with console.status("[bold blue]Processing talk content...[/bold blue]", spinner="dots"):
            post_content = generate_annotated_talk_post(
                slide_path=str(slide_pdf),
                video_source=youtube_url,
                image_dir=image_dir,
                transcript_path=str(transcript) if transcript else None,
                user_prompt=user_prompt
            )
        
        if output:
            Path(output).write_text(post_content)
            console.print(f"\n[bold green]✓ Post saved to:[/bold green] {output}")
        else: print(post_content)
            
    except Exception as e: raise typer.Exit(f"Error: {str(e)}")

def main():
    app()
