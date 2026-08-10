import ast

from babel.messages.extract import extract_python


def extract_errors(file_object, keywords, comment_tags, options):
    """
    Extracts translatable strings from Python source files.

    Parameters:
    - file_object: File object with the source code.
    - keywords: Keywords marking translatable calls.
    - comment_tags: Comment tags for translator context.
    - options: Extraction options (e.g. encoding).

    Returns:
    - Generator: Sequence of (lineno, funcname, message, comments) tuples.
    """
    file_object.seek(0)
    yield from extract_python(file_object, keywords, comment_tags, options)

    file_object.seek(0)
    encoding = options.get("encoding", "utf-8")
    source = file_object.read().decode(encoding)
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        func = node.func
        name = func.id if isinstance(func, ast.Name) else (
            func.attr if isinstance(func, ast.Attribute) else None
        )

        if not name or not name.endswith("Error"):
            continue

        if not node.args:
            continue

        first = node.args[0]

        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            yield node.lineno, "", first.value, []