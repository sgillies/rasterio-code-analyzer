import ast
import sys


class Analyst(ast.NodeVisitor):
    """Analyze code for reads of Rasterio datasets opened in 'w' mode

    This class joins nodes that call rasterio.open() with nodes that call
    read(), using the name that the result of the former is bound to and the
    name of the latter's instance. It will miss in some situations, as when
    rasterio is imported as another name, or when the opened dataset is
    received by a function under a different name.
    """

    def __init__(self):
        super().__init__()
        self.open_calls_mode_w = {}
        self.read_calls = {}
        self.tree = None

    def visit_Call(self, node):
        if node.func.value.id == "rasterio" and node.func.attr == "open" and len(
            node.args
        ) > 1 and node.args[
            1
        ].s == "w":
            if isinstance(node.parent, ast.withitem):
                self.open_calls_mode_w[node.parent.optional_vars.id] = node
            elif isinstance(node.parent, ast.Assign):
                self.open_calls_mode_w[node.parent.targets[0].id] = node
        if node.func.attr == "read":
            self.read_calls[node.func.value.id] = node

    def analyze(self, code):
        self.tree = add_parents(ast.parse(code))
        self.visit(self.tree)

    def report(self):
        intersection = set(self.read_calls.keys()).intersection(
            set(self.open_calls_mode_w.keys())
        )
        joined_records = [
            {
                "name": name,
                "open": self.open_calls_mode_w[name],
                "read": self.read_calls[name],
            }
            for name in intersection
        ]
        return joined_records


def add_parents(tree):
    """For every node in the tree add a reference to its parent"""
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node
    return tree


if __name__ == "__main__":
    code = sys.stdin.read()
    tree = add_parents(ast.parse(code))
    finder = Analyst()
    finder.visit(tree)
    print(finder.report())
