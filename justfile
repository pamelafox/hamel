# hamel package justfile

# Show available commands
default:
    @just --list

# Install package in development mode
install:
    uv pip install -e .

# Install dev dependencies (nbdev, build tools)
install-dev:
    uv pip install -e . nbdev build twine pytest

# Run tests
test:
    uv run pytest tests/ -v

# Export notebooks to Python modules
export:
    uv run nbdev_export

# Clean notebooks (remove outputs, etc.)
clean:
    uv run nbdev_clean

# Bump version (increments patch version in settings.ini)
bump:
    uv run nbdev_bump_version

# Build package (creates dist/)
build:
    rm -rf build/ dist/ *.egg-info hamel.egg-info/
    uv run python -m build

# Publish to PyPI (builds and uploads)
publish:
    uv run nbdev_pypi

# Full release: bump version, export, test, and publish
release:
    @echo "Running tests..."
    just test
    @echo "Bumping version..."
    just bump
    @echo "Exporting notebooks..."
    just export
    @echo "Publishing to PyPI..."
    just publish
    @echo "Done! Don't forget to commit and push."

# Create GitHub release with changelog
release-gh:
    uv run nbdev_release_gh

# Show current version
version:
    @grep "^version" settings.ini | cut -d'=' -f2 | tr -d ' '

# Prepare for release (export, test, clean)
prepare:
    uv run nbdev_prepare
