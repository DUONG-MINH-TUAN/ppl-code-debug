
import sys, os
import subprocess
from antlr4 import *

# Define your variables
DIR = os.path.dirname(__file__)
ANTLR_JAR = 'C:\\Users\\Admin\\Documents\\anltr4.9.2\\antlr4-4.9.2-complete.jar'
CPL_Dest = 'CompiledFiles'
LEXER_SRC = 'codeDebugLexer.g4'  # File lexer grammar
PARSER_SRC = 'codeDebugParser.g4'  # File parser grammar
TESTS = os.path.join(DIR, './tests')


def printUsage():
    print('python run.py gen')
    print('python run.py test')

def printBreak():
    print('-----------------------------------------------')

def generateAntlr2Python():
    print('Antlr4 is running...')
    # Tạo thư mục CompiledFiles nếu chưa tồn tại
    os.makedirs(CPL_Dest, exist_ok=True)
    
    # Tạo lexer từ codeDebugLexer.g4
    print(f'Generating lexer from {LEXER_SRC}...')
    subprocess.run(['java', '-jar', ANTLR_JAR, '-o', CPL_Dest, '-no-listener', '-Dlanguage=Python3', LEXER_SRC])
    
    # Tạo parser từ codeDebugParser.g4
    print(f'Generating parser from {PARSER_SRC}...')
    subprocess.run(['java', '-jar', ANTLR_JAR, '-o', CPL_Dest, '-no-listener', '-Dlanguage=Python3', PARSER_SRC])
    
    print('Generate successfully')

def runTest():
    print('Running testcases...')
    
    from CompiledFiles.codeDebugLexer import codeDebugLexer
    from CompiledFiles.codeDebugParser import codeDebugParser
    from antlr4.error.ErrorListener import ErrorListener


    class CustomErrorListener(ErrorListener):
        def __init__(self, input_content):
            # the list of errors 
            self.errors = []
            self.input_lines = input_content.splitlines()

        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            token_map = {
                'RIGHT_PARENTHESIS': 'closing parenthesis `)`',
                'LEFT_PARENTHESIS': 'opening parenthesis `(`',
                'RIGHT_BRACE': 'closing brace `}`',
                'LEFT_BRACE': 'opening brace `{`',
                'SEMICOLON': 'semicolon `;`',
                'COMMA': 'comma `,`',
                'EQUAL': 'equals sign `=`',
                'IMPLIE': 'arrow `=>`'
            }
            error_message = f"Syntax error at line {line}, column {column}: "
            suggestion = ""
            offending_token = offendingSymbol.text if offendingSymbol else "<unknown>"
            if "missing" in msg:
                missing_token = msg.split("missing ")[1].split(" at")[0].strip()
                missing_token = token_map.get(missing_token, missing_token)
                error_message += f"Missing {missing_token} before '{offending_token}'."
                suggestion = f"Check and add a {missing_token} at the appropriate position."
            elif "mismatched input" in msg:
                expected_token = msg.split("expecting ")[1].strip() if "expecting" in msg else "<unknown>"
                expected_token = token_map.get(expected_token, expected_token)
                error_message += f"Found '{offending_token}' but expected {expected_token}."
                suggestion = f"Check the syntax near '{offending_token}' and ensure {expected_token} is used correctly."
            else:
                error_message += msg
                suggestion = "Review the syntax at this line."
            if line <= len(self.input_lines):
                error_message += f"\nLine {line}: {self.input_lines[line-1].strip()}"
                error_message += f"\n{' ' * (column + len(str(line)) + 2)}^"
            if suggestion:
                error_message += f"\nSuggestion: {suggestion}"
            self.errors.append(error_message)
            print(error_message)

    filename = '001.txt'
    inputFile = os.path.join(DIR, './tests', filename)    

    with open(inputFile, 'r', encoding='utf-8') as f:
        input_content = f.read()

    print('List of token: ')
    lexer = codeDebugLexer(FileStream(inputFile))        
    tokens = []
    token = lexer.nextToken()
    while token.type != Token.EOF:
        tokens.append(token.text)
        token = lexer.nextToken()
    tokens.append('<EOF>')
    print(','.join(tokens))    

    
    lexer = codeDebugLexer(FileStream(inputFile))
    token_stream = CommonTokenStream(lexer)
    parser = codeDebugParser(token_stream)   
    parser.removeErrorListeners()
    error_listener = CustomErrorListener(input_content)
    parser.addErrorListener(error_listener)    
    
    # print parse tree
    try:
        tree = parser.program()
        print(tree.toStringTree(recog=parser))  
    except SystemExit:
        pass
    
    # check if errors are existed or not  
    if error_listener.errors:
        print("Errors found:")
        for error in error_listener.errors:
            print(error)
    else:
        print("Input accepted")


    printBreak()
    print('Run tests completely')

def main(argv):
    print('Complete jar file ANTLR  :  ' + str(ANTLR_JAR))
    print('Length of arguments      :  ' + str(len(argv)))    
    printBreak()

    if len(argv) < 1:
        printUsage()
    elif argv[0] == 'gen':
        generateAntlr2Python()    
    elif argv[0] == 'test':       
        runTest()
    else:
        printUsage()

if __name__ == '__main__':
    main(sys.argv[1:])


