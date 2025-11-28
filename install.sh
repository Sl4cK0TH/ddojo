#!/bin/bash

# This script automates the build and global installation of the d'Dojo CLI tool.
# It will automatically install 'pdm' if it is not found.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- d'Dojo Installer ---"

# 1. Check for pdm and install if missing
if ! command -v pdm &> /dev/null; then
    echo "› 'pdm' not found. Installing it now..."
    curl -sSL https://pdm-project.org/install-pdm.py | python3 -
    
    # The PDM installer typically places the executable in ~/.local/bin
    # We need to add this to the current script's PATH to find the command.
    export PATH="$HOME/.local/bin:$PATH"
    echo "› PDM installed."
else
    echo "› 'pdm' is already installed."
fi

# 2. Check for pipx
echo "› Checking for required tool 'pipx'..."
if ! command -v pipx &> /dev/null; then
    echo "Error: 'pipx' is not installed. This script requires pipx to make the 'ddojo' command globally available."
    echo "You can usually install it with: python3 -m pip install --user pipx"
    echo "Then ensure it's on your PATH with: python3 -m pipx ensurepath"
    exit 1
fi
echo "› All required tools found."

# 3. Sync project dependencies using pdm
echo "› Installing project dependencies..."
pdm install

# 4. Build the project wheel using pdm
echo "› Building the ddojo package..."
pdm build

# 5. Find the built wheel file in the dist/ directory
WHEEL_FILE=$(find dist -name "*.whl" | head -n 1)
if [ -z "$WHEEL_FILE" ]; then
    echo "Error: Build failed. Could not find a wheel file in the dist/ directory."
    exit 1
fi
echo "› Found package: $WHEEL_FILE"

# 6. Install globally using pipx. --force will handle re-installation if it already exists.
echo "› Installing 'ddojo' command globally with pipx..."
pipx install --force "$WHEEL_FILE"

# 7. Success message
echo ""
echo "✅ Installation complete!"
echo "To use the 'ddojo' command, please open a NEW terminal, or reload your shell profile (e.g., 'source ~/.bashrc')."