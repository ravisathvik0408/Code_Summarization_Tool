import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ast_parser.parser import parse_to_ast
from ast_parser.ast_serializer import get_ast_summary_info, get_function_names


def test_valid_code():
    code = "def add(a, b):\n    return a + b"
    tree = parse_to_ast(code)
    assert tree is not None, "AST should be generated for valid code"
    print("[✓] test_valid_code passed")


def test_invalid_code():
    code = "def broken(:"
    tree = parse_to_ast(code)
    assert tree is None, "AST should be None for invalid code"
    print("[✓] test_invalid_code passed")


def test_function_extraction():
    code = "def foo():\n    pass\ndef bar():\n    pass"
    tree = parse_to_ast(code)
    names = get_function_names(tree)
    assert "foo" in names and "bar" in names
    print("[✓] test_function_extraction passed")


def test_ast_info():
    code = "import os\nclass MyClass:\n    def method(self):\n        pass"
    tree = parse_to_ast(code)
    info = get_ast_summary_info(tree)
    assert "MyClass" in info["classes"]
    assert "method" in info["functions"]
    assert "os" in info["imports"]
    print("[✓] test_ast_info passed")


if __name__ == "__main__":
    print("\n--- Running AST Parser Tests ---\n")
    test_valid_code()
    test_invalid_code()
    test_function_extraction()
    test_ast_info()
    print("\n[✓] All AST tests passed!\n")
