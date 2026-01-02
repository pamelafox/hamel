# hamel-tools Plugin for Claude Code

CLI tools for processing YouTube videos, Zoom recordings, and newsletters.

## Installation

```bash
# Add the marketplace
/plugin marketplace add hamelsmu/hamel

# Install the plugin
/plugin install hamel-tools@hamel
```

## Available Skills

| Skill | Command | Description |
|-------|---------|-------------|
| YouTube Transcribe | `/hamel-tools:youtube-transcribe` | Download YouTube video transcripts |
| YouTube Chapters | `/hamel-tools:youtube-chapters` | Generate chapter summaries for YouTube videos |
| Annotate Talk | `/hamel-tools:annotate-talk` | Create annotated blog posts from technical talks |
| Gem | `/hamel-tools:gem` | General-purpose Gemini API interface |
| Kit | `/hamel-tools:kit` | Manage Kit/ConvertKit newsletter broadcasts |
| Zoom | `/hamel-tools:zoom` | Process Zoom transcripts and office hours Q&A |

## Prerequisites

These skills require the `hamel_tools` CLI package to be installed:

```bash
pip install git+https://github.com/hamelsmu/hamel.git#subdirectory=hamel_tools
```

Required environment variables:
- `GEMINI_API_KEY` - For YouTube chapters, annotate-talk, and gem skills
- `KIT_API_KEY` - For Kit newsletter skill
- `JINA_READER_KEY` - For annotate-talk skill

## Development

To test locally without publishing:

```bash
claude --plugin-dir ./plugins/hamel-tools
```

## Validation

```bash
claude plugin validate ./plugins/hamel-tools
```
