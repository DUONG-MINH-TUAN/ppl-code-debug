class ClassComponentExpression(Expression):
    def __init__(self, name: str, methods: List[Expression], line: int):
        super().__init__(line)
        self.name = name
        self.methods = methods

    def interpret(self, context):
        for method in self.methods:
            method.interpret(context)