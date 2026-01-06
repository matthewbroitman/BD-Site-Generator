class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        strings = []
        if self.props == None or len(self.props) == 0:
            return ""
        for key,value in self.props.items():
            strings.append(f' {key}="{value}"')
        return "".join(strings)
    
    def __repr__(self):
        return (f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")

class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return f"{self.value}"
        if self.tag == "a":
            for key,value in self.props.items():
                return f'<{self.tag} {key}="{value}"> {self.value}</{self.tag}>'
        if self.tag == "img":
            for key,value in self.props.items():
                return f'<{self.tag} {key}="{value}" alt="{self.value}" />'
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No Tag")
        if self.children == None:
                raise ValueError("No Children")
        if self.children == []:
            raise ValueError("No Children - Empty List")
        else:
            concat_string=f"<{self.tag}{self.props_to_html()}>"
            for child in self.children:
                concat_string += child.to_html()
            return concat_string + f"</{self.tag}>"