import sys
import json
from antlr4 import *
from UseEffectGrammarLexer import UseEffectGrammarLexer
from UseEffectGrammarParser import UseEffectGrammarParser
from antlr4.error.ErrorListener import ErrorListener

class MyErrorListener(ErrorListener):
    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Syntax error at line {line}:{column} - {msg}")

def check_grammar(input_text):
    input_stream = InputStream(input_text)
    lexer = UseEffectGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = UseEffectGrammarParser(stream)
    
    error_listener = MyErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)
    
    # Gọi rule khởi đầu (prog)
    parser.prog()
    
    if error_listener.errors:
        return {"success": False, "errors": error_listener.errors}
    return {"success": True, "message": "Valid useEffect syntax"}

if __name__ == '__main__':
    input_text = sys.argv[1]
    result = check_grammar(input_text)
    print(json.dumps(result))