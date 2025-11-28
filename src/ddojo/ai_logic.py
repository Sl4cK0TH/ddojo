import os
import json
import google.generativeai as genai

# --- Configuration ---
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

def generate_challenge(difficulty, topic=None):
    """Generates a new programming challenge."""
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not found.")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
    topic_instruction = f"The challenge topic must be focused on: '{topic}'." if topic else ""
    
    prompt = f"""
    Generate a programming challenge. {topic_instruction}
    The output must be in Markdown format and strictly follow this structure:

    # [Challenge Title]
    ## Difficulty
    {difficulty}
    ## Description
    [A concise and clear description of the problem to be solved.]
    ## Grading Criteria
    - **Correctness (60 points):** Awarded for passing the 5 visible test cases (12 points each).
    - **Code Quality (20 points):** Awarded by an AI review for clean, non-hardcoded code.
    - **Efficiency (20 points):** Awarded by an AI review for using an optimal algorithm (judged by Big O complexity).
    ## Constraints
    [A list of any constraints on the input values or other limitations.]
    ## Test Cases
    [Provide exactly 5 distinct test cases. For each, provide an input and output.]
    ### Test Case 1
    #### Input
    ```
    [Input for Test Case 1]
    ```
    #### Output
    ```
    [Output for Test Case 1]
    ```
    ### Test Case 2
    ... (repeat for test cases 2, 3, 4, 5)
    """
    response = model.generate_content(prompt)
    return response.text

def analyze_code_quality(solution_path, challenge_text):
    """Sends code to Gemini to act as a programming contest judge."""
    if not API_KEY:
        return {"verdict": "ERROR", "feedback": "API Key missing, cannot perform quality check."}
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)

    try:
        with open(solution_path, 'r') as f:
            user_code = f.read()
    except FileNotFoundError:
        return {"verdict": "ERROR", "feedback": "Solution file not found."}

    prompt = f"""
    You are a strict but fair programming contest judge. Your goal is to verify the quality and efficiency of a solution that has already passed all functional test cases.

    **Context:**
    The user is solving this challenge:
    {challenge_text}

    **User's Solution:**
    ```cpp
    {user_code}
    ```

    **Your Judging Criteria:**

    1.  **Language Agnostic:** The user can submit a solution in any language (C++, Python, Java, etc.). **Do not penalize the user or fail the `verdict` based on the language they chose.** Your evaluation of quality and efficiency should be independent of the language.

    2.  **Hardcoding & Readability (`verdict`):**
        *   Your primary task is to check for hardcoding.
        *   The `verdict` should be "FAIL" **only if** you detect hardcoding or if the code is exceptionally unreadable/obfuscated.
        *   The `verdict` should be "PASS" if the code implements a general algorithm.

    3.  **Efficiency (`efficiency_verdict`):**
        *   Analyze the algorithmic complexity (Big O). The `efficiency_verdict` should be "FAIL" if the algorithm is clearly sub-optimal (e.g., brute-force O(n^2) when a O(n log n) solution is expected).

    4.  **Feedback (`feedback`):**
        *   Your feedback must be concise (1-2 sentences).
        *   Prioritize the most critical issue. If efficiency is bad, comment on that. If quality failed due to hardcoding, state that.
        *   If the verdicts for quality and efficiency are both "PASS", you may provide a brief, secondary suggestion for a minor code style or best practice improvement as a helpful tip.

    **Output Format:**
    Respond with a JSON object strictly in this format (no markdown formatting):
    {{
        "verdict": "PASS" or "FAIL",
        "hardcoded": true or false,
        "efficiency_verdict": "PASS" or "FAIL",
        "feedback": "Your concise feedback."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        clean_response = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_response)
    except Exception as e:
        return {"verdict": "ERROR", "feedback": f"AI Analysis failed: {str(e)}"}
