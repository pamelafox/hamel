# Claude Instructions for hamel package

## Project Overview

This is an nbdev-based Python package providing CLI tools for content creation:
- `ai-transcribe` - YouTube transcripts
- `ai-chapters` - YouTube chapter generation
- `ai-annotate-talk` - Blog posts from technical talks
- `ai-gem` - Multimodal Gemini API
- `zoom` - Zoom meeting transcripts
- `kit-broadcasts` - Kit newsletter fetching

## Key Files

- `settings.ini` - Package config (version, dependencies, console_scripts)
- `nbs/` - Jupyter notebooks (source of truth for modules)
- `hamel/` - Generated Python modules (via nbdev_export)
- `skills/` - Claude/Amp skill definitions
- `tests/test_cli.py` - CLI tests

## Development Commands

Use the justfile for common tasks:

```bash
just install-dev  # Install with dev dependencies
just test         # Run tests
just export       # Export notebooks to modules
just version      # Show current version
```

## Releasing a New Version

### Quick Release (recommended)
```bash
just release
```

This runs tests, bumps version, exports, and publishes to PyPI.

### Manual Release Steps
```bash
just test         # Ensure tests pass
just bump         # Increment version in settings.ini
just export       # Export notebooks to Python modules
just publish      # Build and upload to PyPI
```

### Individual nbdev Commands
```bash
nbdev_bump_version    # Increment version
nbdev_export          # Export notebooks
nbdev_pypi            # Build and publish
nbdev_prepare         # Export, test, and clean
nbdev_release_gh      # Create GitHub release
```

## Adding a New CLI Tool

1. Create the CLI module in `hamel/` (e.g., `hamel/foo_cli.py`)
2. Add entry point to `settings.ini` console_scripts:
   ```
   console_scripts = ...existing... foo=hamel.foo_cli:main
   ```
3. Create skill in `skills/foo/SKILL.md`
4. Add test in `tests/test_cli.py`
5. Update `skills/README.md`
6. Update `.claude-plugin/marketplace.json`
7. Reinstall: `just install`
8. Run tests: `just test`
9. Release: `just release`

## Testing

```bash
just test                              # Run all tests
uv run pytest tests/test_cli.py -v     # Verbose output
uv run pytest tests/test_cli.py -k Kit # Run specific test
```

## Environment Variables

Required for various tools:
- `GEMINI_API_KEY` - ai-chapters, ai-annotate-talk, ai-gem
- `JINA_READER_KEY` - ai-annotate-talk
- `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET`, `ZOOM_ACCOUNT_ID` - zoom
- `KIT_API_KEY` - kit-broadcasts
