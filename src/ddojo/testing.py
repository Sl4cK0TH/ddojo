import os
import re
import subprocess
import readline
import glob
from .ai_logic import analyze_code_quality

HISTORY_FILE = os.path.expanduser("~/.ddojo_history")

def run_testing_logic(solution_path, challenge_path):
    """Parses, compiles, and runs a solution in one of several languages."""

    def parse_test_cases(text):
        pattern = r"#### Input\s*```\s*(.*?)\s*```\s*#### Output\s*```\s*(.*?)\s*```"
        matches = re.findall(pattern, text, re.DOTALL)
        return [{"input": i, "output": o} for i, o in matches]

    # --- 1. Language-Specific Setup ---
    lang_ext = os.path.splitext(solution_path)[1]
    compile_cmd, run_cmd, cleanup_files = None, None, []
    
    lang_map = {
        '.c': 'C',
        '.cpp': 'C++',
        '.py': 'Python',
        '.js': 'JavaScript',
        '.java': 'Java'
    }
    lang_name = lang_map.get(lang_ext, 'Unknown')
    
    print(f"\n--- Running tests for {os.path.basename(challenge_path)} (Language: {lang_name}) ---")

    if lang_ext in ['.c', '.cpp']:
        executable = "ddojo_solution"
        compiler = 'g++' if lang_ext == '.cpp' else 'gcc'
        compile_cmd = [compiler, '-std=c++17' if lang_ext == '.cpp' else '-std=c11', solution_path, '-o', executable]
        run_cmd = [f'./{executable}']
        cleanup_files.append(executable)
    elif lang_ext == '.java':
        class_name = os.path.splitext(os.path.basename(solution_path))[0]
        compile_cmd = ['javac', solution_path]
        run_cmd = ['java', class_name]
        cleanup_files.append(f'{class_name}.class') 
    elif lang_ext == '.js':
        run_cmd = ['node', solution_path]
    elif lang_ext == '.py':
        run_cmd = ['python3', solution_path]
    else:
        print(f"Error: Unsupported file type '{lang_ext}'. Cannot test.")
        return

    # --- 2. Parse Test Cases ---
    try:
        with open(challenge_path, 'r') as f: challenge_text = f.read()
    except FileNotFoundError:
        print(f"Error: Challenge file not found at {challenge_path}"); return

    test_cases = parse_test_cases(challenge_text)
    if not test_cases:
        print("Error: Could not parse test cases."); return

    # --- 3. Compilation (if needed) ---
    if compile_cmd:
        print(f"Compiling {lang_ext} solution...")
        compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
        if compile_result.returncode != 0:
            print("\n--- Compilation Failed ---"); print(compile_result.stderr); return
        print("Compilation successful.")
    
    # --- 4. Test Execution ---
    results = []
    timed_out = False
    try:
        print("\n--- Running Test Cases ---")
        for i, case in enumerate(test_cases):
            print(f"  Test Case {i+1}/{len(test_cases)}...", end=' ', flush=True)
            status = "Wrong Answer"
            try:
                run_result = subprocess.run(run_cmd, input=case["input"], capture_output=True, text=True, timeout=3)
                if run_result.returncode != 0: status = "Runtime Error"
                elif run_result.stdout.strip() == case["output"].strip(): status = "PASSED"
            except subprocess.TimeoutExpired:
                status = "Time Limit Exceeded"; timed_out = True
            print(status); results.append(status)
    finally:
        # --- 5. Cleanup ---
        for file_to_clean in cleanup_files:
            if os.path.exists(file_to_clean):
                os.remove(file_to_clean)
        if lang_ext == '.java':
            for java_class in glob.glob('*.class'):
                os.remove(java_class)

    # --- 6. Score Calculation & Final Report (Same as before) ---
    correctness_score = results.count("PASSED") * 12
    quality_score, efficiency_score = 0, 0
    ai_feedback = "AI analysis was not run."

    if results.count("PASSED") == len(test_cases):
        print("\nAll test cases passed! Analyzing code quality and efficiency...")
        analysis = analyze_code_quality(solution_path, challenge_text)
        ai_feedback = analysis.get('feedback', 'Could not get feedback.')
        if analysis.get("verdict") == "PASS": quality_score = 20
        if timed_out:
             efficiency_score = 0
             ai_feedback += " (Note: Efficiency score is 0 due to a test case timing out.)"
        elif analysis.get("efficiency_verdict") == "PASS": efficiency_score = 20
    else:
        ai_feedback = "Fix the failed test cases to receive AI feedback on quality and efficiency."

    print("\n--- Final Grade ---")
    print(f"- Correctness:  {correctness_score}/60")
    print(f"- Code Quality: {quality_score}/20")
    print(f"- Efficiency:   {efficiency_score}/20")
    print("--------------------")
    total_score = correctness_score + quality_score + efficiency_score
    print(f"Total Score: {total_score}/100")
    print(f"\\nDojo Master: {ai_feedback}")
    print("--------------------")

def enter_submission_loop(challenge_path):
    """The interactive loop for submitting solutions, with readline history."""
    if os.path.exists(HISTORY_FILE):
        readline.read_history_file(HISTORY_FILE)
    
    try:
        while True:
            solution_path = input("Submit File ('q' to exit): ").strip()
            
            if solution_path.lower() == 'q':
                break
            
            if not os.path.exists(solution_path):
                print(f"Error: File not found at '{solution_path}'. Please check the path and try again.")
                continue
            
            # Only add valid, existing file paths to history
            readline.add_history(solution_path)
            run_testing_logic(solution_path, challenge_path)

    except KeyboardInterrupt:
        # Catch Ctrl+C and treat it as a clean exit request
        print() # Move to a new line after the ^C character
    finally:
        # Save history on exit, whether by 'q' or Ctrl+C
        readline.write_history_file(HISTORY_FILE)
        print("Exiting d'Dojo session.")

