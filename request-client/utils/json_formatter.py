import json
from PyQt5.QtGui import QTextCharFormat, QColor, QFont


def format_json(json_str):
    """
    Format a JSON string with proper indentation.

    Args:
    json_str (str): A string containing JSON data.

    Returns:
    str: Formatted JSON string with proper indentation.
    """
    try:
        parsed = json.loads(json_str)
        return json.dumps(parsed, indent=4, sort_keys=True)
    except json.JSONDecodeError:
        return json_str  # Return original string if it's not valid JSON


def is_valid_json(json_str):
    """
    Check if a string is valid JSON.

    Args:
    json_str (str): A string to be validated as JSON.

    Returns:
    bool: True if the string is valid JSON, False otherwise.
    """
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False


def highlight_json(json_str):
    """
    Generate a list of QTextCharFormat objects for syntax highlighting JSON.

    Args:
    json_str (str): A string containing JSON data.

    Returns:
    list: A list of (start_index, length, QTextCharFormat) tuples for highlighting.
    """
    highlights = []

    # Define formats
    string_format = QTextCharFormat()
    string_format.setForeground(QColor("#008000"))  # Green

    number_format = QTextCharFormat()
    number_format.setForeground(QColor("#0000FF"))  # Blue

    bool_null_format = QTextCharFormat()
    bool_null_format.setForeground(QColor("#FF00FF"))  # Magenta

    key_format = QTextCharFormat()
    key_format.setForeground(QColor("#FF0000"))  # Red
    key_format.setFontWeight(QFont.Bold)

    # Simple parsing and highlighting
    in_string = False
    in_key = False
    start = 0

    for i, char in enumerate(json_str):
        if char == '"':
            if in_string:
                length = i - start + 1
                highlights.append((start, length, string_format if not in_key else key_format))
                in_string = False
                in_key = False
            else:
                in_string = True
                start = i
        elif char in '0123456789.-' and not in_string:
            if i == 0 or json_str[i - 1] not in '0123456789.':
                start = i
            if i == len(json_str) - 1 or json_str[i + 1] not in '0123456789.':
                length = i - start + 1
                highlights.append((start, length, number_format))
        elif char == ':' and not in_string:
            in_key = True
        elif char.lower() in ('t', 'f', 'n') and not in_string:
            if json_str[i:i + 4].lower() in ('true', 'null') or json_str[i:i + 5].lower() == 'false':
                length = 4 if json_str[i:i + 4].lower() in ('true', 'null') else 5
                highlights.append((i, length, bool_null_format))

    return highlights

