class FunctionalComponentExpression(Expression):
    def __init__(self, name: str, params: List[str], body: Expression, line: int):
        super().__init__(line)
        self.name = name
        self.params = params
        self.body = body  # Element trả về

    def interpret(self, context):
        self.body.interpret(context)