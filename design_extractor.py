import ast

def collectProgramDesign(path: str):
    with open(path, "r") as f:
        source = f.read()

    myast = ast.parse(source)
    #print(ast.dump(myast))
    root_funcs = set([anode.name for anode in myast.body if isinstance(anode, ast.FunctionDef)])

    root_classes = set([anode for anode in myast.body if isinstance(anode, ast.ClassDef)])

    ret_classes = {}

    for aclass in root_classes:
        class_name = aclass.name

        func_visitor = MyFuncDefVisitor()

        func_visitor.visit(aclass)
        funcs = func_visitor.getFunctions()

        attr_visitor = MyAttrVisitor(funcs)
        attr_visitor.visit(aclass)

        attrs = attr_visitor.getFields()

        ret_classes[class_name] = {"attrs": attrs, "funcs": funcs}

    return (root_funcs, ret_classes)


class MyAttrVisitor(ast.NodeVisitor):
    def __init__(self, funcs):
        super().__init__()
        self.fields = []
        self.funcs = funcs

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == "self" and node.attr not in self.funcs:
            self.fields.append(node.attr)
        return self.generic_visit(node)

    def getFields(self):
        return set(self.fields)


class MyFuncDefVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.funcs = []

    def visit_FunctionDef(self, node):
        self.funcs.append(node.name)
        return self.generic_visit(node)

    def getFunctions(self):
        return set(self.funcs)

if __name__ == "__main__":
    collectProgramDesign("./input.py")
