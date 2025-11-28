#!/bin/bash

# This script automates the build and global installation of the d'Dojo CLI tool.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- d'Dojo Installer ---"

# --- 1. Prerequisite Checks ---
echo "› Checking for required tools..."
MISSING_TOOLS=false

check_command() {
    CMD=$1
    if ! command -v "$CMD" &> /dev/null; then
        echo "  - Command not found: '$CMD'"
        MISSING_TOOLS=true
    fi
}

check_command gcc
check_command g++
check_command java
check_command javac
check_command node
check_command pdm
check_command pipx

if [ "$MISSING_TOOLS" = true ]; then
    echo -e "\nError: Missing required system dependencies."
    echo "Please install the missing tools using your system's package manager."
    echo "Example commands:"
    echo "  - For C/C++ compilers on Debian/Ubuntu: sudo apt install build-essential"
    echo "  - For C/C++ compilers on Fedora/CentOS: sudo dnf groupinstall 'Development Tools'"
    echo "  - For Java (JDK) on Debian/Ubuntu:       sudo apt install default-jdk"
    echo "  - For Java (JDK) on Fedora/CentOS:       sudo dnf install java-latest-openjdk-devel"
    echo "  - For Node.js (JavaScript):            Follow instructions at https://nodejs.org/"
    echo "  - For PDM:                             curl -sSL https://pdm-project.org/install-pdm.py | python3 -"
    echo "  - For pipx:                            python3 -m pip install --user pipx && python3 -m pipx ensurepath"
    echo -e "\nAfter installing the dependencies, please run this script again."
    exit 1
fi
echo "› All required tools found."

# --- 2. Python Project Installation ---

# Sync project dependencies using pdm
echo "› Installing project dependencies..."
pdm install

# Build the project wheel using pdm
echo "› Building the ddojo package..."
pdm build

# Find the built wheel file in the dist/ directory
WHEEL_FILE=$(find dist -name "*.whl" | head -n 1)
if [ -z "$WHEEL_FILE" ]; then
    echo "Error: Build failed. Could not find a wheel file in the dist/ directory."
    exit 1
fi
echo "› Found package: $WHEEL_FILE"

# Install globally using pipx. --force will handle re-installation if it already exists.
echo "› Installing 'ddojo' command globally with pipx..."
pipx install --force "$WHEEL_FILE"

# --- 3. Success Message ---
echo ""
echo "✅ Installation complete!"
echo "To use the 'ddojo' command, please open a NEW terminal, or reload your shell profile (e.g., 'source ~/.bashrc')."
