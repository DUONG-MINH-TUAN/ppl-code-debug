grammar grammar_checker;

// Parser rules
program: main_structure;

// Syntax
main_structure: (import_statement)? function_keyword identifierValue parameter_list body_function;

// Parameter in functional component
parameter_list: LEFT_PARENTHESIS parameter* RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS LEFT_BRACE parameter* RIGHT_BRACE RIGHT_PARENTHESIS;
parameter: identifierValue (COMMA identifierValue)*;

// Function declaration (sửa đổi để chấp nhận cú pháp cơ bản)
function_keyword: FUNCTION | EXPORT FUNCTION;

// Body of the functional component
body_function: LEFT_BRACE content* RIGHT_BRACE;

// Content of the body of the function
content: stateSetter SEMICOLON?
       | useEffectCall SEMICOLON?
       | arrowFunction SEMICOLON?
       | consoleCommand SEMICOLON?
       | useCallbackCall SEMICOLON?
       | return_statement SEMICOLON?
       | variableDeclaration SEMICOLON?
       | expression SEMICOLON?;

// Types of variable
variableTypes: CONST | VAR | LET;

// Values for types
numberArray: NUMBER (COMMA NUMBER)*;
stringArray: stringValue (COMMA stringValue)*;
arrayValue: numberArray | stringArray;
stringValue: DOUBLE_QUOTE (IDENTIFIER | NUMBER)* DOUBLE_QUOTE
           | SINGLE_QUOTE (IDENTIFIER | NUMBER)* SINGLE_QUOTE;
identifierValue: IDENTIFIER;

// Element
element: openTag elementContent* closeTag | emptyFragment;
emptyFragment: LEFT_ANGLE_BRACKET RIGHT_ANGLE_BRACKET LEFT_ANGLE_BRACKET SLASH RIGHT_ANGLE_BRACKET;

// Open tag
openTag: LEFT_ANGLE_BRACKET identifierValue RIGHT_ANGLE_BRACKET;

// Close tag
closeTag: LEFT_ANGLE_BRACKET SLASH identifierValue RIGHT_ANGLE_BRACKET;

// Content of the element
elementContent: element | valueIndicator | TEXT;
valueIndicator: LEFT_BRACE (IDENTIFIER | NUMBER | stringValue | boolean) RIGHT_BRACE;
TEXT: [a-zA-Z0-9 ]+;

// Variable declaration
variableDeclaration: variableTypes identifierValue EQUAL (NUMBER | stringValue | boolean | array);

// Primitive data
stringDeclaration: variableTypes identifierValue EQUAL stringValue;
numberDeclaration: variableTypes identifierValue EQUAL NUMBER;
booleanDeclaration: variableTypes identifierValue EQUAL boolean;
boolean: TRUE | FALSE;

// Hook declaration

// useState
stateSetter: variableTypes statePair EQUAL USE_STATE initialValue;
statePair: LEFT_SQUARE_BRACKET identifierValue COMMA identifierValue RIGHT_SQUARE_BRACKET;
initialValue: LEFT_PARENTHESIS valueForInitialization RIGHT_PARENTHESIS;
valueForInitialization: identifierValue | NUMBER | array | stringValue;
array: LEFT_SQUARE_BRACKET arrayValue RIGHT_SQUARE_BRACKET;

// useEffect
useEffectCall: USE_EFFECT LEFT_PARENTHESIS callbackFunction COMMA dependencyArray RIGHT_PARENTHESIS;
callbackFunction: LEFT_PARENTHESIS RIGHT_PARENTHESIS IMPLIE LEFT_BRACE content* (RETURN LEFT_PARENTHESIS RIGHT_PARENTHESIS IMPLIE LEFT_BRACE content* RIGHT_BRACE)? RIGHT_BRACE;
dependencyArray: LEFT_SQUARE_BRACKET (identifierValue (COMMA identifierValue)*)? RIGHT_SQUARE_BRACKET;

// useCallback
useCallbackCall: USE_CALLBACK LEFT_PARENTHESIS callbackFunction COMMA dependencyArray RIGHT_PARENTHESIS;

// Arrow function
arrowFunction: variableTypes identifierValue EQUAL parameter_list IMPLIE LEFT_BRACE content* RIGHT_BRACE;

// Statement
hook: USE_EFFECT | USE_CALLBACK | USE_MEMO | USE_STATE;
import_statement: IMPORT LEFT_BRACE hook (COMMA hook)* RIGHT_BRACE FROM REACT SEMICOLON?;
return_statement: RETURN LEFT_PARENTHESIS element RIGHT_PARENTHESIS;

// Console.log command
consoleCommand: CONSOLE DOT LOG LEFT_PARENTHESIS stringValue RIGHT_PARENTHESIS;

// Expression (hỗ trợ JavaScript tổng quát)
expression: identifierValue (EQUAL (NUMBER | stringValue | boolean | array))?;

// Tokens
RETURN: 'return';
CONST: 'const';
VAR: 'var';
LET: 'let';
IMPORT: 'import';
FROM: 'from';
REACT: 'react';
CONSOLE: 'console';
LOG: 'log';
TRUE: 'true';
FALSE: 'false';

FUNCTION: 'function';
EXPORT: 'export';

USE_EFFECT: 'useEffect';
USE_STATE: 'useState';
USE_CALLBACK: 'useCallback';
USE_MEMO: 'useMemo';

LEFT_PARENTHESIS: '(';
RIGHT_PARENTHESIS: ')';
LEFT_BRACE: '{';
RIGHT_BRACE: '}';
LEFT_SQUARE_BRACKET: '[';
RIGHT_SQUARE_BRACKET: ']';
COMMA: ',';
EQUAL: '=';
SINGLE_QUOTE: '\'';
DOUBLE_QUOTE: '\u0022';
LEFT_ANGLE_BRACKET: '<';
RIGHT_ANGLE_BRACKET: '>';
SLASH: '/';
SEMICOLON: ';';
IMPLIE: '=>';
DOT: '.';

IDENTIFIER: [a-zA-Z][a-zA-Z0-9]*;
NUMBER: [0-9]+;

WS: [ \t\r\n]+ -> skip;