# Hamel's Content Creation Skills

AI agent skills for content creation from video and audio sources. These skills wrap CLI tools that process YouTube videos, Zoom recordings, and other media into written content.

## Available Skills

| Skill | Description |
|-------|-------------|
| **youtube-transcribe** | Download YouTube video transcripts with timestamps |
| **youtube-chapters** | Generate chapter summaries with timestamps using AI |
| **annotate-talk** | Create annotated blog posts from technical talks with slides |
| **gem** | Multimodal AI processing for PDFs, images, videos, and documents |
| **zoom** | Download Zoom meeting transcripts |
| **kit** | Fetch Kit (ConvertKit) newsletter broadcasts |

## Installation

### Prerequisites

Install the `hamel` Python package which provides the underlying CLI tools:

```bash
pip install hamel
```

Some tools require API keys:
- `GEMINI_API_KEY` - Required for youtube-chapters, annotate-talk, gem
- `JINA_READER_KEY` - Required for annotate-talk
- `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET`, `ZOOM_ACCOUNT_ID` - Required for zoom
- `KIT_API_KEY` - Required for kit

### For Amp

**Install all hamel-tools skills:**

```bash
amp skill add hamelsmu/hamel
```

**Or install individual skills:**

```bash
amp skill add hamelsmu/hamel/youtube-transcribe
amp skill add hamelsmu/hamel/youtube-chapters
amp skill add hamelsmu/hamel/annotate-talk
amp skill add hamelsmu/hamel/gem
amp skill add hamelsmu/hamel/zoom
amp skill add hamelsmu/hamel/kit
```

**Install recommended Anthropic skills:**

```bash
amp skill add anthropics/skills/frontend-design
amp skill add anthropics/skills/xlsx
```

**List installed skills:**

```bash
amp skill list
```

Skills are installed to `.agents/skills/` in your workspace. See [Amp Manual - Agent Skills](https://ampcode.com/manual#agent-skills) for details.

### For Claude Code

**Add marketplaces:**

```bash
/plugin marketplace add hamelsmu/hamel
/plugin marketplace add anthropics/skills
/plugin marketplace add anthropics/claude-code
```

**Install hamel-tools skills:**

```bash
/plugin install youtube-transcribe@hamelsmu-hamel
/plugin install youtube-chapters@hamelsmu-hamel
/plugin install annotate-talk@hamelsmu-hamel
/plugin install gem@hamelsmu-hamel
/plugin install zoom@hamelsmu-hamel
/plugin install kit@hamelsmu-hamel
```

**Install recommended Anthropic skills:**

```bash
/plugin install frontend-design@anthropic-agent-skills
/plugin install xlsx@anthropic-agent-skills
```

**Install recommended Anthropic plugins:**

```bash
/plugin install ralph-wiggum@claude-code-plugins
/plugin install hookify@claude-code-plugins
/plugin install plugin-dev@claude-code-plugins
```

See [Claude Code Plugin Docs](https://code.claude.com/docs/en/plugin-marketplaces) for details.

### For Claude (Web/Desktop)

1. Download the skill folder you want (e.g., `youtube-transcribe/`)
2. Zip the folder
3. Go to Settings > Capabilities > Skills > Upload Skills
4. Upload the zip file and enable the skill

See [Claude Skills Help](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) for details.

### Manual Installation

Copy skill directories to:
- `.agents/skills/` in your workspace (recommended)
- `~/.config/agents/skills/` globally
- `.claude/skills/` (also supported)

## Usage Examples

Once installed, the agent automatically uses these skills when relevant:

- "Transcribe this YouTube video" → uses youtube-transcribe
- "Generate chapters for this talk" → uses youtube-chapters
- "Turn this conference talk into a blog post" → uses annotate-talk
- "Summarize this PDF" → uses gem
- "Get transcripts from my Zoom calls" → uses zoom
- "Fetch my newsletters from Kit" → uses kit

Or invoke the CLI tools directly:

```bash
ai-transcribe "https://youtu.be/VIDEO_ID"
ai-chapters "https://youtu.be/VIDEO_ID"
ai-annotate-talk "https://youtu.be/VIDEO_ID" slides.pdf output_images/
ai-gem "Summarize this" document.pdf
zoom 123456789 -o transcript.vtt
kit-broadcasts -o newsletters.json
```

## License

MIT
