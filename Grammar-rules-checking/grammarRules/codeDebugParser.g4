parser grammar codeDebugParser;

options {
    tokenVocab=codeDebugLexer;  
}

// Parser rules 
program: main_structure EOF; 

main_structure: (import_statement)? (statement_or_function)*;

statement_or_function: statement | function_declaration | functionalComponent | classComponent;

// Function declaration
function_declaration: FUNCTION IDENTIFIER parameter_list body_function
                   | EXPORT FUNCTION IDENTIFIER parameter_list body_function;

parameter_list: LEFT_PARENTHESIS parameter* RIGHT_PARENTHESIS 
              | LEFT_PARENTHESIS LEFT_BRACE parameter* RIGHT_BRACE RIGHT_PARENTHESIS;
parameter: IDENTIFIER (COMMA IDENTIFIER)*;    

body_function: LEFT_BRACE content* RIGHT_BRACE; 

content: stateSetter stat_breakDown
       | useEffectCall stat_breakDown
       | bigIntDeclaration stat_breakDown
       | numberDeclaration stat_breakDown
       | stringDeclaration stat_breakDown
       | arrowFunction stat_breakDown
       | arrayDeclaration stat_breakDown
       | consoleCommand stat_breakDown
       | useCallbackCall stat_breakDown
       | dateDeclaration stat_breakDown   
       | return_statement stat_breakDown
       | variableDeclaration stat_breakDown
       | forStatement stat_breakDown
       | ifStatement stat_breakDown;

variableTypes: CONST | VAR | LET;

variableDeclaration: variableTypes IDENTIFIER EQUAL (stringValue | NUMBER | boolean | BIGINT_LITERAL | NULL | SYMBOL_FUNC | array | NEW DATE_FUNC | arrowFunction);
statement: variableDeclaration stat_breakDown
         | consoleCommand stat_breakDown
         | ifStatement
         | forStatement
         | useEffectCall stat_breakDown
         | useCallbackCall stat_breakDown
         | stateSetter stat_breakDown
         | bigIntDeclaration stat_breakDown
         | numberDeclaration stat_breakDown
         | stringDeclaration stat_breakDown
         | arrowFunction stat_breakDown
         | arrayDeclaration stat_breakDown
         | dateDeclaration stat_breakDown;

array: LEFT_SQUARE_BRACKET arrayValue* RIGHT_SQUARE_BRACKET;
numberArray: NUMBER (COMMA NUMBER)*;
stringArray: stringValue (COMMA stringValue)*;
arrayArray: array (COMMA array)*;
arrayValue: numberArray | stringArray | arrayArray;
stringValue: STRING_VALUE;

// JSX Element
element: openTag elementContent* closeTag
       | fragmentOpen elementContent* fragmentClose
       | emptyFragment
       | selfClosingTag;
emptyFragment: JSX_FRAGMENT_OPEN TAG_FRAGMENT_CLOSE;
fragmentOpen: JSX_FRAGMENT_OPEN;
fragmentClose: TAG_FRAGMENT_CLOSE;
openTag: JSX_OPEN_TAG TAG_RIGHT_ANGLE_BRACKET | TAG_OPEN_TAG TAG_RIGHT_ANGLE_BRACKET;
closeTag: TAG_CLOSE_TAG;
selfClosingTag: TAG_SELF_CLOSING_TAG;

elementContent: element | valueIndicator | TAG_TEXT;
valueIndicator: LEFT_BRACE IDENTIFIER RIGHT_BRACE;  

stringDeclaration: variableTypes IDENTIFIER EQUAL stringValue;
numberDeclaration: variableTypes IDENTIFIER EQUAL NUMBER+;
booleanDeclaration: variableTypes IDENTIFIER EQUAL boolean;
boolean: TRUE | FALSE;
bigIntDeclaration: variableTypes IDENTIFIER EQUAL BIGINT_LITERAL;  
undefinedDeclaration: variableTypes IDENTIFIER;
nullDeclaration: variableTypes IDENTIFIER EQUAL NULL;
symbolDeclaration: variableTypes IDENTIFIER EQUAL SYMBOL_FUNC;
arrayDeclaration: variableTypes IDENTIFIER EQUAL array;
dateDeclaration: variableTypes IDENTIFIER EQUAL NEW DATE_FUNC;

stateSetter: variableTypes statePair EQUAL USE_STATE initialValue;
statePair: LEFT_SQUARE_BRACKET IDENTIFIER COMMA IDENTIFIER RIGHT_SQUARE_BRACKET;
initialValue: LEFT_PARENTHESIS valueForInitialization* RIGHT_PARENTHESIS;
valueForInitialization: IDENTIFIER | NUMBER+ | array | stringValue;

useEffectCall: USE_EFFECT LEFT_PARENTHESIS callbackFunction COMMA dependencyArray RIGHT_PARENTHESIS;
callbackFunction: LEFT_PARENTHESIS RIGHT_PARENTHESIS IMPLIE LEFT_BRACE content* RIGHT_BRACE;
dependencyArray: LEFT_SQUARE_BRACKET parameter* RIGHT_SQUARE_BRACKET; 

useCallbackCall: USE_CALLBACK LEFT_PARENTHESIS callbackFunction COMMA dependencyArray RIGHT_PARENTHESIS;

arrowFunction: parameter_list IMPLIE (LEFT_BRACE content* RIGHT_BRACE | element);

hook: USE_EFFECT | USE_CALLBACK | USE_MEMO | USE_STATE;
import_statement: IMPORT LEFT_BRACE hook (COMMA hook)* RIGHT_BRACE FROM REACT stat_breakDown;
return_statement: RETURN element stat_breakDown;

consoleCommand: CONSOLE DOT LOG LEFT_PARENTHESIS (stringValue | IDENTIFIER)? RIGHT_PARENTHESIS;

stat_breakDown: SEMICOLON?;

functionalComponent: (FUNCTION | CONST) IDENTIFIER parameter_list IMPLIE element;

classComponent: CLASS IDENTIFIER EXTENDS IDENTIFIER LEFT_BRACE (methodDeclaration)* RIGHT_BRACE;
methodDeclaration: IDENTIFIER parameter_list body_function;

forStatement: FOR LEFT_PARENTHESIS IDENTIFIER OF IDENTIFIER RIGHT_PARENTHESIS block;

ifStatement: IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS block (ELSE block)?;

block: LEFT_BRACE blockContent* RIGHT_BRACE;
blockContent: stateSetter stat_breakDown
            | useEffectCall stat_breakDown
            | bigIntDeclaration stat_breakDown
            | numberDeclaration stat_breakDown
            | stringDeclaration stat_breakDown
            | arrowFunction stat_breakDown
            | arrayDeclaration stat_breakDown
            | consoleCommand stat_breakDown
            | useCallbackCall stat_breakDown
            | dateDeclaration stat_breakDown   
            | variableDeclaration stat_breakDown;

expression: valueIndicator                     # varExpr
          | NUMBER                              # numExpr
          | stringValue                         # strExpr
          | boolean                             # boolExpr
          | expression op=(MUL | DIV) expression  # mulDivExpr
          | expression op=(ADD | SUB) expression  # addSubExpr
          | LEFT_PARENTHESIS expression RIGHT_PARENTHESIS # parenExpr;

errorRule: .+? (SEMICOLON | RIGHT_BRACE | EOF);