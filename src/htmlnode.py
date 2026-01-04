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

    