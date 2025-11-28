import argparse
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env file at the very start
load_dotenv()

# Now import local modules
from .ai_logic import generate_challenge, analyze_code_quality
from .testing import run_testing_logic
from .files import save_challenge, set_active_challenge, get_active_challenge, handle_resume_logic

BANNER = """
         88    d8'  88888888ba,                 88               
         88   d8'   88      `"8b                ""               
         88   ""     88        `8b                                
 ,adPPYb,88         88         88   ,adPPYba,   88   ,adPPYba,   
a8"    `Y88         88         88  a8"     "8a  88  a8"     "8a  
8b       88         88         8P  8b       d8  88  8b       d8  
"8a,   ,d88         88      .a8P   "8a,   ,a8"  88  "8a,   ,a8"  
 `"8bbdP"Y8         88888888Y""     `"YbbdP""   88   `"YbbdP""   
                                               ,88               
                                             888P"               
A CLI tool for generating and testing daily programming challenges.
Author: Zor0ark
"""

def get_interactive_difficulty():
    """Prompts the user to select a difficulty from a menu."""
    print("Please choose a difficulty:")
    from .files import INTERACTIVE_CHOICES
    for i, choice in enumerate(INTERACTIVE_CHOICES):
        print(f"  {i+1}. {choice}")
    while True:
        try:
            choice = input("Enter your choice (number or name): ").strip()
            if choice.isdigit():
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(INTERACTIVE_CHOICES):
                    return INTERACTIVE_CHOICES[choice_idx]
            else:
                for valid_choice in INTERACTIVE_CHOICES:
                    if choice.lower() == valid_choice.lower():
                        return valid_choice
            print("Invalid choice. Please try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number or name.")

def main():
    """Main function to parse arguments and run the d'Dojo CLI."""
    print(BANNER)
    
    parser = argparse.ArgumentParser(
        description="d'Dojo is an interactive CLI tool designed to help you practice your coding skills by providing unique, AI-generated programming challenges.",
        epilog="""
Usage Examples:

  1. Generate a new challenge with a random difficulty:
     ddojo --new

  2. Generate a new 'Hard' challenge on the topic of 'Graphs':
     ddojo --new --difficulty hard --topic "Graphs"

  3. Resume a previous session (will list recent challenges to choose from):
     ddojo --resume
     
  4. List ALL previous challenges to resume from:
     ddojo --resume -a

  5. Test a solution against the currently active challenge:
     ddojo --submit /path/to/your/solution.cpp

Note: The '--submit' command is for non-interactive testing. During a '--new' or '--resume' session, you can submit files directly in the interactive prompt.
""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--new", action="store_true", help="Start a new challenge session.")
    action_group.add_argument("--resume", action="store_true", help="Resume a previous challenge session.")
    action_group.add_argument("--submit", type=str, metavar="FILE_PATH", help="Run a one-time test for a solution file against the active challenge.")

    new_group = parser.add_argument_group('options for --new')
    from .files import DIFFICULTY_LEVELS
    new_group.add_argument("--difficulty", type=str.lower, default=None, choices=[d.lower() for d in DIFFICULTY_LEVELS], help="Set the difficulty of the challenge.")
    new_group.add_argument("--topic", type=str, help="Specify a topic for the challenge.")

    resume_group = parser.add_argument_group('options for --resume')
    resume_group.add_argument("-a", "--all", action="store_true", help="Show all challenges when resuming, not just the most recent.")

    # If no arguments are provided, print help and exit.
    import sys
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    try:
        if args.new:
            difficulty = args.difficulty or get_interactive_difficulty()
            if difficulty.lower() == "surprise me!":
                difficulty = random.choice(DIFFICULTY_LEVELS)
            difficulty = difficulty.capitalize()
            topic_info = f" on the topic of '{args.topic}'" if args.topic else ""
            print(f"\nGenerating a new {difficulty} challenge{topic_info}...")
            
            from .display import clean_markdown_for_display
            
            challenge_text = generate_challenge(difficulty, args.topic)
            filepath = save_challenge(challenge_text)
            set_active_challenge(filepath)
            
            cleaned_content = clean_markdown_for_display(challenge_text)
            print("\\n" + "="*80)
            print(cleaned_content)
            print("="*80)
            
            print(f"Challenge saved to: {filepath}")
            print(f"This is now the active challenge.")
            from .testing import enter_submission_loop
            enter_submission_loop(filepath)
        elif args.resume:
            handle_resume_logic(args.all)
        elif args.submit:
            solution_path = args.submit
            challenge_path = get_active_challenge()
            if not challenge_path:
                print("Error: No active challenge has been set. Use '--new' or '--resume' first.")
                return
            if not os.path.exists(solution_path):
                print(f"Error: Solution file not found at '{solution_path}'.")
                return
            run_testing_logic(solution_path, challenge_path)
    except (ValueError, Exception) as e:
        print(f"An unexpected error occurred: {e}")
