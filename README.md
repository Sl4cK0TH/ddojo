<div align="center">

```
         88    d8'  88888888ba,                 88               
         88   d8'   88      `"8b                ""               
         88  ""     88        `8b                                
 ,adPPYb,88         88         88   ,adPPYba,   88   ,adPPYba,   
a8"    `Y88         88         88  a8"     "8a  88  a8"     "8a  
8b       88         88         8P  8b       d8  88  8b       d8  
"8a,   ,d88         88      .a8P   "8a,   ,a8"  88  "8a,   ,a8"  
 `"8bbdP"Y8         88888888Y"'     `"YbbdP"'   88   `"YbbdP"'   
                                               ,88               
                                             888P"               
```
</div>

<h1 align="center">d'Dojo</h1>

<p align="center">
  A CLI tool for generating and testing daily programming challenges.
  <br />
  <b>Author:</b> Zor0ark
</p>

---

`d'Dojo` is an interactive command-line tool designed to help you practice your coding skills. It uses AI to generate unique, high-quality programming challenges and provides an automated grading system to test your solutions in real-time.

## Features

- **AI-Powered Challenges:** Generate new programming problems on-demand with the `--new` flag.
- **Multi-Language Support:** Test solutions written in **C, C++, Java, JavaScript, and Python**.
- **Detailed Grading System:** Receive a score out of 100 broken down into:
    - **Correctness (60 pts):** Based on passing 5 visible test cases.
    - **Code Quality (20 pts):** AI analysis of readability and for hardcoding.
    - **Efficiency (20 pts):** AI analysis of the solution's algorithmic complexity (Big O).
- **Interactive Session:** After generating a challenge, enter an interactive loop to test your solution files repeatedly.
- **Command History:** The submission prompt features command history and full line-editing, just like your terminal.
- **Session Management:** Use `--resume` to pick up where you left off on a previous challenge.
- **Customizable:** Specify a difficulty (`Easy`, `Medium`, `Hard`, `Insane`) and a topic (e.g., "Graphs", "Dynamic Programming").

## Configuration

Before you can run the application, you need to provide your Google Gemini API key.

1.  In the root of the `ddojo` directory, copy the example environment file:
    ```bash
    cp .env.example .env
    ```

2.  Open the newly created `.env` file and replace `"Your-API-Key-Here"` with your actual Gemini API key. The file should look like this:
    ```
    GEMINI_API_KEY="AIz...Your...Key...Here"
    ```

The application is now configured to use your API key. The `.env` file is included in `.gitignore` and will not be committed to your repository.

## Requirements

Before installation, please ensure you have the following tools installed and available on your system's PATH:

- **Python 3.8+**
- **pipx** (`python3 -m pip install --user pipx`)
- **Git**
- **Language Runtimes/Compilers:**
    - `gcc` (for C)
    - `g++` (for C++)
    - `node` (for JavaScript)
    - A Java JDK (for `javac` and `java`)

## Installation

You can install `d'Dojo` using either the automatic script or the manual method.

### Automatic Installation (Recommended)

The provided `install.sh` script automates the entire process.

1.  **Make the script executable:**
    ```bash
    chmod +x install.sh
    ```
2.  **Run the script:**
    ```bash
    ./install.sh
    ```
This script will automatically install `pdm` if needed, build the project, and use `pipx` to install the `ddojo` command globally.

### Manual Installation

If you prefer to have more control over the installation steps:

1.  **Install Core Tools:**
    Make sure `pdm` and `pipx` are installed.
    ```bash
    # Install PDM
    curl -sSL https://pdm-project.org/install-pdm.py | python3 -
    
    # Install pipx
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    ```

2.  **Install Project Dependencies:**
    This command reads the `pyproject.toml` file and installs libraries like `google-generativeai`.
    ```bash
    pdm install
    ```

3.  **Build the Package:**
    This bundles the application into a distributable wheel file in the `dist/` directory.
    ```bash
    pdm build
    ```

4.  **Install Globally with pipx:**
    Install the wheel file from the `dist/` directory.
    ```bash
    pipx install dist/ddojo-*.whl
    ```

After installation via either method, open a **new terminal** to start using the `ddojo` command.

## Usage

Here are some of the main ways to use `d'Dojo`:

- **Generate a new challenge with a random difficulty:**
  ```bash
  ddojo --new
  ```

- **Generate a new 'Hard' challenge on the topic of 'Graphs':**
  ```bash
  ddojo --new --difficulty hard --topic "Graphs"
  ```

- **Resume a previous session (will list recent challenges to choose from):**
  ```bash
  ddojo --resume
  ```
  
- **List ALL previous challenges to resume from:**
  ```bash
  ddojo --resume -a
  ```

- **See all available options and commands:**
  ```bash
  ddojo --help
  ```
