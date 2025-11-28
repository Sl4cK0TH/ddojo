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

- **Multi-Language Support:**
  - Automated testing engine supports solutions in **C, C++, Java, JavaScript, and Python**.

- **Automated Testing & Grading:**
  - Professional 3-part grading system (Correctness, Code Quality, Efficiency).
  - AI-powered "Dojo Master" that provides feedback on code quality and algorithmic efficiency.

- **User Experience & Workflow:**
  - Project structured as a standard, installable Python package using PDM.
  - `install.sh` script for fully automated installation, including prerequisite checks.
  - Interactive submission loop that waits for user input after a challenge is generated.
  - Command history (Arrow Up/Down) and line editing via the `readline` library.
  - Session management with `--resume` to continue previous challenges.
  - Comprehensive help manual with usage examples (`--help`).
  - Custom ASCII art banner and project branding.
  - Formatted terminal output that removes markdown and draws boxes around code blocks.

- **Documentation & Setup:**
  - Detailed `README.md` with instructions for installation, configuration, and usage.
  - `.env.example` file for straightforward API key setup.
  - This `CHANGELOG.md` file to track project evolution.
  - `.gitignore` configured to exclude user-generated files and build artifacts.

### Changed

- **Project Structure:** Refactored from a single script to a modular `src` layout.
- **AI Judging:** The AI judge's instructions were refined to focus on contest-style evaluation (correctness, efficiency, hardcoding) rather than enterprise "best practices".
- **Output Label:** Renamed "AI Feedback" to "Dojo Master" in the final report.

### Fixed

- Resolved multiple Python bugs related to `SyntaxError`, import order (`GEMINI_API_KEY` not found), and incorrect file paths that arose during refactoring.
- Corrected `pdm` configuration (`distribution = false`) to ensure the `ddojo` command could be installed correctly.
- Fixed a regular expression bug in the test case parser that caused it to fail.