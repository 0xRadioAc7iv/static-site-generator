class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        result = ""
        for key in self.props:
            result += f" {key}=\"{self.props[key]}\""
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list["HTMLNode"], props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("tag is required")
        
        children_html = ""
        
        for child in self.children:
            if isinstance(child, ParentNode):
                nested_parent_html = ""

                for ch in child.children:
                    nested_parent_html += ch.to_html()

                children_html += f"<{child.tag}{self.props_to_html()}>{nested_parent_html}</{child.tag}>"
                continue

            if child.value is None or child.value == "":
                raise ValueError("This nodes's child node does not contain a value")

            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None: raise ValueError("value is required")
        if self.tag is None: return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props_to_html()})"