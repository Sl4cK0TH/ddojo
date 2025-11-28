# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-28

This is the initial public release of d'Dojo, a feature-rich CLI tool for programming practice.

### Added

- **Core Functionality:**
    - AI-powered challenge generation using the Google Gemini API (`--new`).
    - Support for customizable difficulty and topics.
    - Saving of generated challenges to a `challenges/` directory.

- **Automated Testing & Grading:**
    - Multi-language testing engine supporting C, C++, Java, JavaScript, and Python.
    - Professional 3-part grading system (Correctness, Code Quality, Efficiency).
    - AI-powered "Dojo Master" that provides feedback on code quality and algorithmic efficiency.

- **User Experience & Workflow:**
    - Project refactored into an installable Python package using PDM and `pyproject.toml`.
    - `install.sh` script for fully automated build and global installation.
    - Interactive submission loop that waits for user input after a challenge is generated.
    - Command history (Arrow Up/Down) and line editing in the submission prompt via the `readline` library.
    - Session management with `--resume` to continue previous challenges.
    - Comprehensive help manual and usage examples (`--help`).
    - Custom ASCII art banner and project branding.
    - Enhanced terminal display that formats markdown into a clean view with boxed code blocks.

- **Documentation & Setup:**
    - Detailed `README.md` with instructions for installation and usage.
    - `.env.example` file and instructions for API key configuration.
    - Git repository setup instructions, including `.gitignore` for user-generated files.

### Changed

- **Project Structure:** Migrated from a single Python script to a modular `src` layout.
- **AI Prompts:** Refined AI prompts to generate language-agnostic challenges and provide contest-focused judging.
- **Exit Logic:** Changed from instant-exit on 'q' to `q` + Enter to accommodate `readline` history features.

### Fixed

- Resolved multiple Python bugs related to `SyntaxError`, import order (`GEMINI_API_KEY not found`), and incorrect `replace` operations.
- Corrected PDM configuration (`distribution = false`) to allow package installation.
- Fixed a regex pattern that failed to parse test cases.
