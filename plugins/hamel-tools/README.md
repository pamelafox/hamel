# hamel-tools Plugin

CLI tools for processing YouTube videos, Zoom recordings, and newsletters.

## Installation

### Claude Code

```bash
# Add the marketplace
/plugin marketplace add hamelsmu/hamel

# Install the plugin
/plugin install hamel-tools@hamel
```

### Amp

```bash
amp skill add hamelsmu/hamel
```

Or use the command palette: `/skill-add hamelsmu/hamel`

## Prerequisites

Install the CLI tools:

```bash
pip install hamel
```

Required environment variables:

| Variable | Required for |
|----------|--------------|
| `GEMINI_API_KEY` | youtube-chapters, annotate-talk, gem |
| `KIT_API_KEY` | kit |
| `JINA_READER_KEY` | annotate-talk |
| `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET`, `ZOOM_ACCOUNT_ID` | zoom |

## Available Skills

| Skill | Description |
|-------|-------------|
| youtube-transcribe | Download YouTube video transcripts |
| youtube-chapters | Generate chapter summaries for YouTube videos |
| annotate-talk | Create annotated blog posts from technical talks |
| gem | Multimodal Gemini API for PDFs, images, videos |
| kit | Manage Kit/ConvertKit newsletter broadcasts |
| zoom | Process Zoom transcripts and office hours Q&A |

## Local Development

Test without publishing:

```bash
# Claude Code
claude --plugin-dir /path/to/plugins/hamel-tools

# Amp
amp --skill-dir /path/to/plugins/hamel-tools/skills
```

Validate the plugin:

```bash
claude plugin validate ./plugins/hamel-tools
```
