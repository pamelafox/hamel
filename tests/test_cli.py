"""Minimal tests for CLI tools."""

import os
import subprocess
import pytest

def run_cli(cmd: list[str]) -> subprocess.CompletedProcess:
    """Run CLI command via uv run and return result."""
    return subprocess.run(["uv", "run"] + cmd, capture_output=True, text=True, timeout=120)

def has_gemini_key() -> bool:
    return bool(os.environ.get("GEMINI_API_KEY"))

class TestTranscribe:
    def test_help(self):
        result = run_cli(["ai-transcribe", "--help"])
        assert result.returncode == 0
        assert "YouTube video URL" in result.stdout

    def test_transcribe_video(self):
        result = run_cli(["ai-transcribe", "https://youtu.be/dQw4w9WgXcQ"])
        assert result.returncode == 0
        assert "never gonna give you up" in result.stdout.lower()

    def test_transcribe_seconds(self):
        result = run_cli(["ai-transcribe", "https://youtu.be/dQw4w9WgXcQ", "--seconds"])
        assert result.returncode == 0
        assert "s]" in result.stdout

class TestChapters:
    def test_help(self):
        result = run_cli(["ai-chapters", "--help"])
        assert result.returncode == 0
        assert "YouTube video URL" in result.stdout

    @pytest.mark.skipif(not has_gemini_key(), reason="GEMINI_API_KEY not set")
    def test_chapters_video(self):
        result = run_cli(["ai-chapters", "https://youtu.be/dQw4w9WgXcQ"])
        assert result.returncode == 0
        assert "00:00" in result.stdout

class TestGem:
    def test_help(self):
        result = run_cli(["ai-gem", "--help"])
        assert result.returncode == 0
        assert "Gemini" in result.stdout

    @pytest.mark.skipif(not has_gemini_key(), reason="GEMINI_API_KEY not set")
    def test_gem_simple(self):
        result = run_cli(["ai-gem", "What is 2+2? Reply with just the number."])
        assert result.returncode == 0
        assert "4" in result.stdout

class TestAnnotateTalk:
    def test_help(self):
        result = run_cli(["ai-annotate-talk", "--help"])
        assert result.returncode == 0
        assert "YouTube video URL" in result.stdout
        assert "slide" in result.stdout.lower()

class TestZoom:
    def test_help(self):
        result = run_cli(["zoom", "--help"])
        assert result.returncode == 0
        assert "Zoom" in result.stdout
        assert "meeting" in result.stdout.lower()

class TestKit:
    def test_help(self):
        result = run_cli(["kit-broadcasts", "--help"])
        assert result.returncode == 0
        assert "Kit" in result.stdout
        assert "broadcasts" in result.stdout.lower()
