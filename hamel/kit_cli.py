"""CLI tool to fetch Kit broadcasts."""

import json
import os
import sys
from typing import Optional

import httpx
import typer
from rich.console import Console
from typing_extensions import Annotated

KIT_API_KEY = os.getenv('KIT_API_KEY')
BASE_URL = "https://api.kit.com/v4"

console = Console(stderr=True)


def fetch_broadcasts(api_key: str, per_page: int = 500) -> list[dict]:
    """Fetch all broadcasts from Kit API with pagination."""
    broadcasts = []
    after_cursor = None
    
    with httpx.Client(timeout=30.0) as client:
        while True:
            params = {"per_page": per_page}
            if after_cursor:
                params["after"] = after_cursor
            
            response = client.get(
                f"{BASE_URL}/broadcasts",
                headers={"X-Kit-Api-Key": api_key},
                params=params
            )
            
            if response.status_code != 200:
                console.print(f"[red]Error: {response.status_code} - {response.text}[/red]")
                sys.exit(1)
            
            data = response.json()
            broadcasts.extend(data["broadcasts"])
            
            pagination = data.get("pagination", {})
            if not pagination.get("has_next_page"):
                break
            after_cursor = pagination.get("end_cursor")
    
    return broadcasts


def fetch_broadcast_stats(api_key: str, per_page: int = 500) -> dict:
    """Fetch stats for all broadcasts."""
    stats = {}
    after_cursor = None
    
    with httpx.Client(timeout=30.0) as client:
        while True:
            params = {"per_page": per_page}
            if after_cursor:
                params["after"] = after_cursor
            
            response = client.get(
                f"{BASE_URL}/broadcasts/stats",
                headers={"X-Kit-Api-Key": api_key},
                params=params
            )
            
            if response.status_code == 403:
                return {}
            
            if response.status_code != 200:
                console.print(f"[red]Error fetching stats: {response.status_code} - {response.text}[/red]")
                return {}
            
            data = response.json()
            for b in data.get("broadcasts", []):
                stats[b["id"]] = b["stats"]
            
            pagination = data.get("pagination", {})
            if not pagination.get("has_next_page"):
                break
            after_cursor = pagination.get("end_cursor")
    
    return stats


def format_broadcast(broadcast: dict, stats: dict = None) -> dict:
    """Extract relevant fields from a broadcast."""
    data = {
        "id": broadcast["id"],
        "subject": broadcast["subject"],
        "preview_text": broadcast.get("preview_text"),
        "content": broadcast.get("content"),
        "created_at": broadcast["created_at"],
        "send_at": broadcast.get("send_at"),
        "published_at": broadcast.get("published_at"),
        "public": broadcast.get("public", False),
        "public_url": broadcast.get("public_url"),
    }
    if stats:
        data["stats"] = stats
    return data


app = typer.Typer()


@app.command()
def kit_broadcasts(
    api_key: Annotated[Optional[str], typer.Option("--api-key", "-k", help="Kit API key (or set KIT_API_KEY env var)")] = None,
    output: Annotated[Optional[str], typer.Option("--output", "-o", help="Output file path (default: stdout)")] = None,
    full: Annotated[bool, typer.Option("--full", help="Include all fields, not just subject/preview/content")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Show progress info")] = False,
):
    """Fetch all Kit broadcasts and output as JSON.
    
    By default outputs simplified broadcast data (subject, preview_text, content) to stdout.
    Use --full to include all fields. Use --output to save to a file.
    """
    key = api_key or KIT_API_KEY
    if not key:
        console.print("[red]Error: No API key provided. Use --api-key or set KIT_API_KEY env var.[/red]")
        raise typer.Exit(1)
    
    if verbose:
        console.print("[cyan]Fetching broadcasts from Kit...[/cyan]")
    
    broadcasts = fetch_broadcasts(key)
    
    if verbose:
        console.print("[cyan]Fetching broadcast stats...[/cyan]")
    
    stats = fetch_broadcast_stats(key)
    
    if verbose:
        console.print(f"[green]Fetched {len(broadcasts)} broadcasts[/green]")
    
    if not full:
        broadcasts = [format_broadcast(b, stats.get(b["id"])) for b in broadcasts]
    elif stats:
        for b in broadcasts:
            if b["id"] in stats:
                b["stats"] = stats[b["id"]]
    
    output_json = json.dumps(broadcasts, indent=2, ensure_ascii=False)
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(output_json)
        if verbose:
            console.print(f"[green]Saved to {output}[/green]")
    else:
        print(output_json)


def main():
    app()
