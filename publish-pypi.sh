#!/usr/bin/env bash
set -e

echo "Cleaning old build artifacts..."
rm -rf build/ dist/ *.egg-info

echo "Building package..."
python -m build

echo "Uploading to PyPI..."
twine upload dist/*

echo "Done!"
