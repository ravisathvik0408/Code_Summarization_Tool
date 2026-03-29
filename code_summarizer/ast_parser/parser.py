import ast


def parse_to_ast(code: str):
    """
    Parses Python source code into an AST (Abstract Syntax Tree).

    Args:
        code (str): Raw Python source code

    Returns:
        ast.Module: Parsed AST tree, or None if syntax error
    """
    try:
        tree = ast.parse(code)
        print("\n[✓] AST Parsed Successfully")
        return tree
    except SyntaxError as e:
        print(f"\n[✗] Syntax Error in code: {e}")
        return None
