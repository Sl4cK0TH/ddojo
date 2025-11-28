import re

def _format_code_block_as_box(code_content):
    """Takes a string of code and draws a box around it."""
    # Sanitize and split lines, handling potential empty code blocks
    lines = code_content.strip().split('\n')
    if not lines or not any(lines):
        return ""
    
    max_len = max(len(line) for line in lines)
    
    top_border = f"  +{"=" * (max_len + 2)}+"
    bottom_border = top_border
    
    boxed_lines = [top_border]
    for line in lines:
        padded_line = line.ljust(max_len)
        boxed_lines.append(f"  | {padded_line} |")
    boxed_lines.append(bottom_border)
    
    return '\n'.join(boxed_lines)

def clean_markdown_for_display(text):
    """
    Cleans raw markdown text for better terminal display.
    - Removes headers
    - Removes bold markers
    - Formats code blocks into a drawn box
    """
    # First, handle code blocks by replacing them with a formatted box
    # The lambda function calls our helper for each match found
    processed_text = re.sub(r'```[a-zA-Z]*\n(.*?)\n```', lambda m: _format_code_block_as_box(m.group(1)), text, flags=re.DOTALL)
    
    # Then, handle simpler line-by-line formatting
    lines = processed_text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove headers like #, ##, etc.
        line = re.sub(r'^#+\s*', '', line)
        # Remove ** for bold, but keep the text
        line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)
