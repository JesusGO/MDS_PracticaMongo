
class Publication:

    allowed_nodes = {"author", "title", "pages", "year"}

    def __init__(self, node):
        self.node = node
        self.type = node.nodeName
        self.title = ''
        self.authors = []
        self.pages = ''
        self.year = ''

    def exec_node(self):
        self.type = self.node.nodeName
        self.exec_childs_node()

    def exec_childs_node(self):

        for child in self.node.childNodes:            
            if child.nodeName in self.allowed_nodes:
                value = child.firstChild.nodeValue
                if child.nodeName == 'author':
                    self.authors.append(value)
                if child.nodeName == 'title':
                    self.title = value
                if child.nodeName == 'pages':
                    self.pages = value
                if child.nodeName == 'year':
                    self.year = value
                    if self.year != '':
                        self.year = int(self.year)

    def serialize(self):
        return {
            "type": self.type,
            "title": self.title,
            "authors": self.authors,
            "pages": self.pages,
            "year": self.year
        }