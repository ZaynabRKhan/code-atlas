import tree_sitter_python as tsp
from tree_sitter import Language
from tree_sitter import Parser as TSParser
import networkx as nx
import matplotlib.pyplot as plt

class TreeTraversal:
    def __init__(self):
        self.code = {}
        self.graph = nx.Graph()
        language = Language(tsp.language())
        pyparser = TSParser(language)
        file = "E:/Startup/code-atlas/repos/spreadsheet-assistant/agents/manager.py"
        with open(file, "rb") as f:
            self.code[file] = pyparser.parse(f.read())
            print("tree created")

    def traversePython(self):
        file = "E:/Startup/code-atlas/repos/spreadsheet-assistant/agents/manager.py"
        tree = self.code[file]
        root = tree.root_node
        assert root.type == 'module'
        # print(type(root.type))
        # print(root.start_point)
        # print(root.end_point)
        # print(root.children)
        # print()
        # print(root.children[1].text)
        # print()
        # print(root.children[1].children[0].text.decode())
        root_name = "::".join(file.split("repos/")[-1].split("/"))
        print(root_name)
        self.graph.add_node(root_name)
        for child in root.children:
            t = child.type
            if t == "import_from_statement":
                self.graph.add_node(child.children[3].text.decode())
                self.graph.add_edge(root_name, child.children[3].text.decode())
                self.graph.add_node(child.children[1].text.decode())
                self.graph.add_edge(child.children[3].text.decode(), child.children[1].text.decode())
                if len(child.children) >= 5:
                    self.graph.add_node(child.children[5].text.decode())
                    self.graph.add_edge(child.children[3].text.decode(), child.children[5].text.decode())
        print(list(self.graph.nodes))
        print(list(self.graph.edges))
        plt.figure(figsize=(8, 6))
        nx.draw(
            self.graph,
            with_labels=True,
            node_size=1000,
            node_color="lightblue",
            font_size=10,
            arrows=True,
        )

        plt.show()

tree = TreeTraversal()
tree.traversePython()