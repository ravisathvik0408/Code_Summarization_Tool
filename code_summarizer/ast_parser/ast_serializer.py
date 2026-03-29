import ast


def ast_to_dict(node):
    """
    Recursively converts an AST node into a readable Python dictionary.

    Args:
        node: An ast.AST node

    Returns:
        dict: A dictionary representation of the AST
    """
    if isinstance(node, ast.AST):
        result = {"node_type": type(node).__name__}
        for field, value in ast.iter_fields(node):
            result[field] = ast_to_dict(value)
        return result
    elif isinstance(node, list):
        return [ast_to_dict(item) for item in node]
    else:
        return node


def get_function_names(tree) -> list:
    """
    Extracts all function names from the AST.

    Args:
        tree: Parsed AST tree

    Returns:
        list: Names of all functions found
    """
    return [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    ]


def get_ast_summary_info(tree) -> dict:
    """
    Returns a high-level structural summary from the AST.

    Args:
        tree: Parsed AST tree

    Returns:
        dict: Summary of code structure
    """
    info = {
        "functions": [],
        "classes": [],
        "imports": [],
        "num_lines": 0
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            info["functions"].append(node.name)
        elif isinstance(node, ast.ClassDef):
            info["classes"].append(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in getattr(node, "names", []):
                info["imports"].append(alias.name)

    return info
