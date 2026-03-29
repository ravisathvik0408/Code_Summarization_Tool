def get_code_from_user():
    """
    Accepts multi-line Python code from the user via terminal.
    User types code and presses Enter on an empty line to finish.
    """
    print("=" * 50)
    print("  NLP-Based Code Summarization Tool")
    print("=" * 50)
    print("\nPaste your Python code below.")
    print("Press ENTER on an empty line when done:\n")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    if not lines:
        print("\n[ERROR] No code was entered.")
        return None

    return "\n".join(lines)
