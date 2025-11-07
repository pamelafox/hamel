"""CLI for Zoom transcript downloads."""

from pathlib import Path
from dotenv import load_dotenv
from fastcore.parallel import parallel
import httpx
import typer
from hamel.zoom import get_zoom_token, list_recordings, download_transcript, make_filename

load_dotenv()

app = typer.Typer()

@app.command()
def zoom(
    meeting_id: str = typer.Argument(None, help="Meeting ID to download"),
    search: str = typer.Option(None, "--search", "-s", help="Filter by text in topic"),
    days: int = typer.Option(45, "--days", "-d", help="Number of days to look back"),
    output: Path = typer.Option(None, "--output", "-o", help="Output file or directory"),
):
    """Download Zoom meeting transcripts.
    
    Examples:
      zoom 123456789              # Print to stdout (pipe to other tools)
      zoom 123456789 -o file.vtt  # Download to file
      zoom -s "Jason"              # Search, select one or 'a' for all
      zoom -s ""                   # List all meetings
    """
    try:
        token = get_zoom_token()
        
        # Direct meeting ID download
        if meeting_id:
            transcript = download_transcript(meeting_id, token)
            if not transcript:
                print("No transcript available.")
                raise typer.Exit(1)
            
            if output:
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(transcript, encoding="utf-8")
                print(f"Saved to {output}")
            else:
                print(transcript)
            return
        
        # Search and download
        meetings = list_recordings(days)
        
        # Filter by topic
        if search is not None:
            query = search.lower()
            meetings = [m for m in meetings if query in m.get('topic', '').lower()]
        
        if not meetings:
            print("No meetings found.")
            return
        
        # Show list
        print(f"\nFound {len(meetings)} meeting(s):\n")
        for idx, meeting in enumerate(meetings, 1):
            date = meeting['start_time'].split('T')[0]
            print(f"{idx:2}. {date} | {meeting['id']} | {meeting.get('topic', '')}")
        
        # Prompt for selection
        choice = typer.prompt("\nEnter number (or 'a' for all)")
        
        # Prompt for output directory
        outdir = Path(typer.prompt("Save to directory", default="."))
        if outdir != Path("."):
            outdir.mkdir(parents=True, exist_ok=True)
        
        # Download all
        if choice.lower() == "a":
            print(f"\nDownloading {len(meetings)} transcript(s)...")
            
            def download_one(meeting):
                transcript = download_transcript(str(meeting['id']), token)
                if transcript:
                    filepath = outdir / make_filename(meeting)
                    filepath.write_text(transcript, encoding="utf-8")
                    print(f"✓ {filepath.name}")
                else:
                    print(f"✗ No transcript: {meeting.get('topic', '')[:50]}")
            
            parallel(download_one, meetings, threadpool=True, n_workers=8)
            return
        
        # Download one
        try:
            idx = int(choice)
        except ValueError:
            print("Invalid input.")
            raise typer.Exit(1)
        
        if idx < 1 or idx > len(meetings):
            print("Invalid selection.")
            raise typer.Exit(1)
        
        meeting = meetings[idx - 1]
        transcript = download_transcript(str(meeting['id']), token)
        if not transcript:
            print("No transcript available.")
            raise typer.Exit(1)
        
        filepath = outdir / make_filename(meeting)
        filepath.write_text(transcript, encoding="utf-8")
        print(f"Saved to {filepath}")
        
    except (httpx.HTTPError, httpx.RequestError, KeyError) as e:
        print(f"Error: {e}")
        raise typer.Exit(1)

def main():
    app()
