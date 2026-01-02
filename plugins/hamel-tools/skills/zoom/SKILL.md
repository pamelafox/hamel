---
name: zoom
description: Download Zoom meeting transcripts. Use when asked to get transcripts from Zoom recordings, download Zoom meeting notes, or fetch Zoom call transcripts.
---

# Zoom Transcript Downloader

Use the `zoom` CLI tool to download transcripts from Zoom meeting recordings.

## Important: Avoid Interactive Mode

The `-s` (search) flag triggers interactive prompts which don't work well in automated contexts. **Always use direct meeting ID download when possible.**

## Usage

### Direct Download (Preferred)

```bash
# Download transcript by meeting ID to stdout
zoom 123456789

# Save transcript to a specific file
zoom 123456789 -o transcript.vtt

# Save to a specific directory
zoom 123456789 -o meetings/call-transcript.vtt
```

### Finding Meeting IDs

If you need to find meeting IDs, run the search in a way that shows the list but exits:
```bash
# List recent meetings (will show IDs in output)
zoom -s "" 2>&1 | head -20
```

Then use the meeting ID directly with `zoom <meeting_id>`.

## Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `meeting_id` | | Meeting ID to download (positional, required for non-interactive use) |
| `--output` | `-o` | Output file path for the transcript |
| `--search` | `-s` | Search filter for topic (triggers interactive mode - avoid in automation) |
| `--days` | `-d` | Number of days to look back (default: 45) |

## Output

Returns VTT (WebVTT) transcript files containing timestamped speaker labels and text.

Example VTT format:
```
WEBVTT

00:00:05.000 --> 00:00:10.000
Speaker 1: Hello everyone, welcome to the meeting.

00:00:10.500 --> 00:00:15.000
Speaker 2: Thanks for joining today.
```

## Requirements

Environment variables for Server-to-Server OAuth:
- `ZOOM_CLIENT_ID`
- `ZOOM_CLIENT_SECRET`
- `ZOOM_ACCOUNT_ID`

The `hamel` package must be installed: `pip install hamel`

## Examples

**Download a specific meeting transcript:**
```bash
zoom 85678123456 -o meeting-notes.vtt
```

**Download and immediately read the content:**
```bash
zoom 85678123456 > transcript.vtt && cat transcript.vtt
```

**Process transcript with AI:**
```bash
zoom 85678123456 -o /tmp/meeting.vtt
ai-gem "Summarize this meeting transcript" /tmp/meeting.vtt
```
