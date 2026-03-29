import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from summarizer.model import generate_summary


def test_simple_function():
    code = "def add(a, b):\n    return a + b"
    summary = generate_summary(code)
    assert isinstance(summary, str), "Summary should be a string"
    assert len(summary) > 0, "Summary should not be empty"
    print(f"[✓] test_simple_function passed\n    Summary: {summary}")


def test_factorial():
    code = (
        "def factorial(n):\n"
        "    if n == 0:\n"
        "        return 1\n"
        "    return n * factorial(n - 1)"
    )
    summary = generate_summary(code)
    assert isinstance(summary, str)
    assert len(summary) > 0
    print(f"[✓] test_factorial passed\n    Summary: {summary}")


def test_class_code():
    code = (
        "class Stack:\n"
        "    def __init__(self):\n"
        "        self.items = []\n"
        "    def push(self, item):\n"
        "        self.items.append(item)\n"
        "    def pop(self):\n"
        "        return self.items.pop()"
    )
    summary = generate_summary(code)
    assert isinstance(summary, str)
    print(f"[✓] test_class_code passed\n    Summary: {summary}")


if __name__ == "__main__":
    print("\n--- Running Summarizer Tests ---\n")
    test_simple_function()
    test_factorial()
    test_class_code()
    print("\n[✓] All summarizer tests passed!\n")
