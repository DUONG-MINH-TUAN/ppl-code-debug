lexer grammar codeDebugLexer;

// Định nghĩa các token cơ bản
NEW: 'new' -> pushMode(DATE_MODE);

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
NULL: 'null';
FOR: 'for';  
OF: 'of';    
IF: 'if';    
ELSE: 'else'; 
ADD: '+';    
SUB: '-';       
MUL: '*';    
DIV: '/';

BIGINT_LITERAL: [0-9]+ 'n';

FUNCTION: 'function';
EXPORT: 'export default';
SYMBOL_FUNC: 'Symbol()';

USE_EFFECT: 'useEffect';
USE_STATE: 'useState';
USE_CALLBACK: 'useCallback';
USE_MEMO: 'useMemo';

LEFT_ANGLE_BRACKET: '<';
RIGHT_ANGLE_BRACKET: '>';
LEFT_PARENTHESIS: '(';
RIGHT_PARENTHESIS: ')';
LEFT_BRACE: '{';
RIGHT_BRACE: '}';
LEFT_SQUARE_BRACKET: '[';
RIGHT_SQUARE_BRACKET: ']';
COMMA: ',';
EQUAL: '=';
SINGLE_QUOTE: '\'';
DOUBLE_QUOTE: '"';
SEMICOLON: ';';
IMPLIE: '=>';
DOT: '.';

// Nhận diện thẻ mở JSX và đẩy vào TAG_MODE
JSX_OPEN_TAG: LEFT_ANGLE_BRACKET [a-zA-Z][a-zA-Z0-9]* -> pushMode(TAG_MODE);
// Nhận diện thẻ đóng JSX
JSX_CLOSE_TAG: LEFT_ANGLE_BRACKET DIV -> pushMode(TAG_MODE);
// Nhận diện fragment mở
JSX_FRAGMENT_OPEN: LEFT_ANGLE_BRACKET RIGHT_ANGLE_BRACKET -> pushMode(TAG_MODE);
// Nhận diện fragment đóng
JSX_FRAGMENT_CLOSE: LEFT_ANGLE_BRACKET DIV RIGHT_ANGLE_BRACKET -> pushMode(TAG_MODE);

// Định nghĩa IDENTIFIER
IDENTIFIER: [a-zA-Z][a-zA-Z0-9]*;

NUMBER: [0-9][0-9]*;

WS: [ \t\r\n]+ -> skip;

fragment STRING_CONTENT: (~["'\\] | '\\' ["'\\])*;
SINGLE_QUOTE_STRING: '\'' STRING_CONTENT '\'' -> type(STRING_VALUE);
DOUBLE_QUOTE_STRING: '"' STRING_CONTENT '"' -> type(STRING_VALUE);
STRING_VALUE: SINGLE_QUOTE_STRING | DOUBLE_QUOTE_STRING;

// Mode để xử lý thẻ HTML/JSX
mode TAG_MODE;
TAG_SLASH: '/' -> type(DIV);
TAG_TEXT: ~[<>}{]+;
TAG_IDENTIFIER: [a-zA-Z][a-zA-Z0-9]* -> type(IDENTIFIER);
TAG_RIGHT_ANGLE_BRACKET: '>' -> type(RIGHT_ANGLE_BRACKET), popMode;
TAG_LEFT_ANGLE_BRACKET: '<' -> type(LEFT_ANGLE_BRACKET);
TAG_WS: [ \t\r\n]+ -> skip;

mode DATE_MODE;
SPACE: [ \t\r\n]+;  
DATE_IDENTIFIER: 'Date';
DATE_MODE_LEFT_PARENTHESIS: '(';
DATE_MODE_RIGHT_PARENTHESIS: ')';
DATE_FUNC: SPACE DATE_IDENTIFIER SPACE? DATE_MODE_LEFT_PARENTHESIS SPACE? DATE_MODE_RIGHT_PARENTHESIS -> popMode;