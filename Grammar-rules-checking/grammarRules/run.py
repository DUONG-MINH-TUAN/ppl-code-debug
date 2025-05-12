# # import sys, os
# # import subprocess
# # import unittest
# # from antlr4 import *


# # # Define your variables
# # DIR = os.path.dirname(__file__)
# # ANTLR_JAR = 'C:\\Users\\Admin\\Documents\\anltr4.9.2\\antlr4-4.9.2-complete.jar'
# # CPL_Dest = 'CompiledFiles'
# # SRC = 'codeDebug.g4'
# # TESTS = os.path.join(DIR, './tests')


# # def printUsage():
# #     print('python Hello.py gen')
# #     print('python Hello.py test')


# # def printBreak():
# #     print('-----------------------------------------------')


# # def generateAntlr2Python():
# #     print('Antlr4 is running...')
# #     subprocess.run(['java', '-jar', ANTLR_JAR, '-o', CPL_Dest, '-no-listener', '-Dlanguage=Python3', SRC])
# #     print('Generate successfully')

# # def runTest():
# #     print('Running testcases...')
    
# #     from CompiledFiles.codeDebugLexer import codeDebugLexer
# #     from CompiledFiles.codeDebugParser import codeDebugParser
# #     from antlr4.error.ErrorListener import ErrorListener

# #     class CustomErrorListener(ErrorListener):
# #         def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
# #             print(f"Input rejected: {msg}")
# #             exit(1)  # Exit the program with an error

# #     filename = '001.txt'
# #     inputFile = os.path.join(DIR, './tests', filename)    

# #     print('List of token: ')
# #     lexer = codeDebugLexer(FileStream(inputFile))        
# #     tokens = []
# #     token = lexer.nextToken()
# #     while token.type != Token.EOF:
# #         tokens.append(token.text)
# #         token = lexer.nextToken()
# #     tokens.append('<EOF>')
# #     print(','.join(tokens))    

# #     # test
# #     input_stream = FileStream(inputFile)
# #     lexer = codeDebugLexer(input_stream)
# #     stream = CommonTokenStream(lexer)
# #     parser = codeDebugParser(stream)
# #     tree = parser.program()  # Start parsing at the `program` rule

# #     # Print the parse tree (for debugging)
# #     print(tree.toStringTree(recog=parser))
# #     # end of test

    
# #     # Reset the input stream for parsing and catch the error
# #     lexer = codeDebugLexer(FileStream(inputFile))
# #     token_stream = CommonTokenStream(lexer)

# #     parser = codeDebugParser(token_stream)   
# #     parser.removeErrorListeners()
# #     parser.addErrorListener(CustomErrorListener())    
# #     try:
# #         parser.program()
# #         print("Input accepted")
# #     except SystemExit:        
# #         pass
    
# #     printBreak()
# #     print('Run tests completely')

# # def main(argv):
# #     print('Complete jar file ANTLR  :  ' + str(ANTLR_JAR))
# #     print('Length of arguments      :  ' + str(len(argv)))    
# #     printBreak()

# #     if len(argv) < 1:
# #         printUsage()
# #     elif argv[0] == 'gen':
# #         generateAntlr2Python()    
# #     elif argv[0] == 'test':       
# #         runTest()
# #     else:
# #         printUsage()


# # if __name__ == '__main__':
# #     main(sys.argv[1:])     
    
    


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
        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            print(f"Input rejected: {msg}")
            exit(1)  # Thoát chương trình khi có lỗi

    filename = '002.txt'
    inputFile = os.path.join(DIR, './tests', filename)    

    print('List of token: ')
    lexer = codeDebugLexer(FileStream(inputFile))        
    tokens = []
    token = lexer.nextToken()
    while token.type != Token.EOF:
        tokens.append(token.text)
        token = lexer.nextToken()
    tokens.append('<EOF>')
    print(','.join(tokens))    

    # Chỉ phân tích với bộ lắng nghe lỗi tùy chỉnh
    lexer = codeDebugLexer(FileStream(inputFile))
    token_stream = CommonTokenStream(lexer)
    parser = codeDebugParser(token_stream)   
    parser.removeErrorListeners()
    parser.addErrorListener(CustomErrorListener())    
    try:
        tree = parser.program()
        print(tree.toStringTree(recog=parser))  # In cây phân tích nếu thành công
        print("Input accepted")
    except SystemExit:
        pass
    
    printBreak()
    print('Run tests completely')

# def runTest():
#     print('Running testcases...')
    
#     from CompiledFiles.codeDebugLexer import codeDebugLexer
#     from CompiledFiles.codeDebugParser import codeDebugParser
#     from antlr4.error.ErrorListener import ErrorListener

#     class CustomErrorListener(ErrorListener):
#         def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
#             print(f"Input rejected: {msg}")
#             exit(1)  # Exit the program with an error

#     filename = '001.txt'
#     inputFile = os.path.join(DIR, './tests', filename)    

#     print('List of token: ')
#     lexer = codeDebugLexer(FileStream(inputFile))        
#     tokens = []
#     token = lexer.nextToken()
#     while token.type != Token.EOF:
#         tokens.append(token.text)
#         token = lexer.nextToken()
#     tokens.append('<EOF>')
#     print(','.join(tokens))    

#     # Test parsing
#     input_stream = FileStream(inputFile)
#     lexer = codeDebugLexer(input_stream)
#     stream = CommonTokenStream(lexer)
#     parser = codeDebugParser(stream)
#     tree = parser.program()  # Start parsing at the `program` rule

#     # Print the parse tree (for debugging)
#     print(tree.toStringTree(recog=parser))
#     # End of test

#     # Reset the input stream for parsing and catch the error
#     lexer = codeDebugLexer(FileStream(inputFile))
#     token_stream = CommonTokenStream(lexer)

#     parser = codeDebugParser(token_stream)   
#     parser.removeErrorListeners()
#     parser.addErrorListener(CustomErrorListener())    
#     try:
#         parser.program()
#         print("Input accepted")
#     except SystemExit:        
#         pass
    
#     printBreak()
#     print('Run tests completely')

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


