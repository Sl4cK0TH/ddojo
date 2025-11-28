import os
import glob
from datetime import datetime

# --- Configuration ---
CHALLENGES_DIR = "challenges"
CONTEXT_FILE = ".ddojo_context"
DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard", "Insane"]
INTERACTIVE_CHOICES = ["Surprise Me!"] + DIFFICULTY_LEVELS

def save_challenge(text):
    """Saves the given challenge text to a timestamped file."""
    if not os.path.exists(CHALLENGES_DIR):
        os.makedirs(CHALLENGES_DIR)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    try:
        title_line = next(line for line in text.splitlines() if line.startswith("# "))
        clean_title = title_line.replace("# ", "").strip().replace(" ", "_").lower()
    except (StopIteration, IndexError):
        clean_title = "challenge"
    
    filepath = os.path.join(CHALLENGES_DIR, f"{timestamp}_{clean_title}.md")
    with open(filepath, "w") as f:
        f.write(text)
    return filepath

def set_active_challenge(challenge_path):
    """Saves the path of the active challenge to the context file."""
    with open(CONTEXT_FILE, "w") as f:
        f.write(challenge_path)

def get_active_challenge():
    """Retrieves the active challenge path from the context file."""
    if not os.path.exists(CONTEXT_FILE):
        return None
    with open(CONTEXT_FILE, "r") as f:
        return f.read().strip()

def handle_resume_logic(show_all):
    """Lists challenges and allows the user to resume one."""
    print("\n--- Resuming a Challenge ---")
    
    # Correctly reference the testing module for the submission loop
    from .testing import enter_submission_loop

    challenge_files = glob.glob(os.path.join(CHALLENGES_DIR, "*.md"))
    challenge_files.sort(key=os.path.getmtime, reverse=True)
    
    if not challenge_files:
        print("No challenges found to resume.")
        return

    limit = None if show_all else 5
    files_to_show = challenge_files[:limit]

    print("Please select a challenge to resume:")
    for i, file_path in enumerate(files_to_show):
        clean_name = os.path.basename(file_path).replace("_", " ").replace(".md", "")
        print(f"  {i+1}. {clean_name}")

    while True:
        try:
            choice_str = input("Enter your choice (number): ").strip()
            if not choice_str: continue
            
            if choice_str.lower() == 'q':
                print("Exiting.")
                break

            choice_idx = int(choice_str) - 1
            if 0 <= choice_idx < len(files_to_show):
                selected_path = files_to_show[choice_idx]
                
                print(f"\\nResuming challenge: {os.path.basename(selected_path)}")
                set_active_challenge(selected_path)
                
                with open(selected_path, 'r') as f:
                    print("\\n" + "="*80)
                    print(f.read())
                    print("="*80)

                enter_submission_loop(selected_path)
                break
            else:
                print("Invalid number. Please choose a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\\nExiting.")
            break
