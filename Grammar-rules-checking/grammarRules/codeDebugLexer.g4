lexer grammar codeDebugLexer;

// Mode mặc định
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
CLASS: 'class';
EXTENDS: 'extends';
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

// Nhận diện thẻ JSX trong mode mặc định
JSX_OPEN_TAG: LEFT_ANGLE_BRACKET IDENTIFIER -> pushMode(TAG_MODE);
JSX_FRAGMENT_OPEN: LEFT_ANGLE_BRACKET RIGHT_ANGLE_BRACKET -> pushMode(TAG_MODE);

// Định nghĩa IDENTIFIER
IDENTIFIER: [a-zA-Z][a-zA-Z0-9]*;

// Định nghĩa số
NUMBER: [0-9][0-9]*;

// Định nghĩa chuỗi
fragment STRING_CONTENT: (~["'\\] | '\\' ["'\\])*;
SINGLE_QUOTE_STRING: '\'' STRING_CONTENT '\'' -> type(STRING_VALUE);
DOUBLE_QUOTE_STRING: '"' STRING_CONTENT '"' -> type(STRING_VALUE);
STRING_VALUE: SINGLE_QUOTE_STRING | DOUBLE_QUOTE_STRING;

WS: [ \t\r\n]+ -> skip;

// Mode để xử lý thẻ HTML/JSX
mode TAG_MODE;
TAG_SLASH: '/';
TAG_RIGHT_ANGLE_BRACKET: '>';
TAG_LEFT_ANGLE_BRACKET: '<';
TAG_OPEN_TAG: TAG_LEFT_ANGLE_BRACKET IDENTIFIER -> pushMode(TAG_MODE); // Thẻ mở lồng nhau
TAG_TEXT: ~[<>{}]+; // Nội dung văn bản
TAG_WS: [ \t\r\n]+ -> skip;
TAG_CLOSE_TAG: TAG_LEFT_ANGLE_BRACKET TAG_SLASH IDENTIFIER TAG_RIGHT_ANGLE_BRACKET -> popMode; // Thẻ đóng
TAG_SELF_CLOSING_TAG: TAG_LEFT_ANGLE_BRACKET IDENTIFIER TAG_SLASH TAG_RIGHT_ANGLE_BRACKET -> popMode; // Thẻ tự đóng
TAG_FRAGMENT_CLOSE: TAG_LEFT_ANGLE_BRACKET TAG_SLASH TAG_RIGHT_ANGLE_BRACKET -> popMode; // Fragment đóng

// Mode để xử lý Date
mode DATE_MODE;
SPACE: [ \t\r\n]+;  
DATE_IDENTIFIER: 'Date';
DATE_MODE_LEFT_PARENTHESIS: '(';
DATE_MODE_RIGHT_PARENTHESIS: ')';
DATE_FUNC: SPACE? DATE_IDENTIFIER SPACE? DATE_MODE_LEFT_PARENTHESIS SPACE? DATE_MODE_RIGHT_PARENTHESIS -> popMode;