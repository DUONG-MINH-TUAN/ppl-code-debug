lexer grammar codeDebugLexer;

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

BIGINT_LITERAL: [0-9]+ 'n';

FUNCTION: 'function';
EXPORT: 'export default';
SYMBOL_FUNC: 'Symbol()';

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


NUMBER: [0-9];

WS: [ \t\r\n]+ -> skip;


mode DATE_MODE;
SPACE: [ \t\r\n]+;  
DATE_IDENTIFIER: 'Date';
DATE_MODE_LEFT_PARENTHESIS: '(';
DATE_MODE_RIGHT_PARENTHESIS: ')';
DATE_FUNC: SPACE DATE_IDENTIFIER SPACE? DATE_MODE_LEFT_PARENTHESIS SPACE? DATE_MODE_RIGHT_PARENTHESIS -> popMode;