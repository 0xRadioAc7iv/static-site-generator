from enum import Enum

class TextType(Enum):
    TEXT = "text (plain)"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    

    def __eq__(self, node: "TextNode"):
        return (
            self.text == node.text and
            self.text_type == node.text_type and
            self.url == node.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"