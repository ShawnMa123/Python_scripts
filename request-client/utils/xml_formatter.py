import xml.dom.minidom
import xml.etree.ElementTree as ET
from PyQt5.QtGui import QTextCharFormat, QColor, QFont


def format_xml(xml_str):
    """
    Format an XML string with proper indentation.

    Args:
    xml_str (str): A string containing XML data.

    Returns:
    str: Formatted XML string with proper indentation.
    """
    try:
        dom = xml.dom.minidom.parseString(xml_str)
        return dom.toprettyxml(indent="  ")
    except Exception:
        return xml_str  # Return original string if it's not valid XML


def is_valid_xml(xml_str):
    """
    Check if a string is valid XML.

    Args:
    xml_str (str): A string to be validated as XML.

    Returns:
    bool: True if the string is valid XML, False otherwise.
    """
    try:
        ET.fromstring(xml_str)
        return True
    except ET.ParseError:
        return False


def highlight_xml(xml_str):
    """
    Generate a list of QTextCharFormat objects for syntax highlighting XML.

    Args:
    xml_str (str): A string containing XML data.

    Returns:
    list: A list of (start_index, length, QTextCharFormat) tuples for highlighting.
    """
    highlights = []

    # Define formats
    tag_format = QTextCharFormat()
    tag_format.setForeground(QColor("#800000"))  # Maroon
    tag_format.setFontWeight(QFont.Bold)

    attribute_format = QTextCharFormat()
    attribute_format.setForeground(QColor("#FF0000"))  # Red

    value_format = QTextCharFormat()
    value_format.setForeground(QColor("#0000FF"))  # Blue

    comment_format = QTextCharFormat()
    comment_format.setForeground(QColor("#008000"))  # Green
    comment_format.setFontItalic(True)

    # Simple parsing and highlighting
    in_tag = False
    in_attribute = False
    in_value = False
    in_comment = False
    start = 0

    for i, char in enumerate(xml_str):
        if char == '<' and not in_comment:
            if xml_str[i:i + 4] == '<!--':
                in_comment = True
                start = i
            else:
                in_tag = True
                start = i
        elif char == '>' and not in_comment:
            if in_tag:
                length = i - start + 1
                highlights.append((start, length, tag_format))
                in_tag = False
        elif char == '=' and in_tag and not in_value:
            in_attribute = True
            attr_start = start
            start = i + 1
        elif char in ('"', "'") and in_tag:
            if in_value:
                length = i - start + 1
                highlights.append((start, length, value_format))
                in_value = False
                start = i + 1
            else:
                in_value = True
                if in_attribute:
                    length = start - attr_start
                    highlights.append((attr_start, length, attribute_format))
                    in_attribute = False
                start = i
        elif in_comment and xml_str[i:i + 3] == '-->':
            length = i - start + 3
            highlights.append((start, length, comment_format))
            in_comment = False

    return highlights

