grammar codeDebug;

// Parser rules 
program: main_structure; 

// syntax
main_structure: (import_statement)? function_declaration identifierValue+ parameter_list body_function;

//parameter in functional component
parameter_list:     LEFT_PARENTHESIS parameter* RIGHT_PARENTHESIS 
                |   LEFT_PARENTHESIS LEFT_BRACE parameter* RIGHT_BRACE RIGHT_PARENTHESIS;
parameter: identifierValue (COMMA identifierValue)*;    
//function declaration
function_declaration:FUNCTION | EXPORT FUNCTION;

//body of the functional component
body_function: LEFT_BRACE content* RIGHT_BRACE; 

// content of the body of the function
content:    stateSetter (SEMICOLON)?
        |   useEffectCall (SEMICOLON)?
        |   arrowFunction (SEMICOLON)?
        |   consoleCommand (SEMICOLON)?
        |   useCallbackCall (SEMICOLON)?    
        |   return_statement (SEMICOLON)?;


// types of variable
variableTypes: CONST | VAR | LET;

//values for types 
numberArray: NUMBER (COMMA NUMBER)*;
stringArray: stringValue (COMMA stringValue)*;
arrayValue: numberArray | stringArray;
stringValue: 
                DOUBLE_QUOTE identifierValue* DOUBLE_QUOTE 
        |       SINGLE_QUOTE identifierValue* SINGLE_QUOTE
        |       DOUBLE_QUOTE NUMBER* DOUBLE_QUOTE
        |       SINGLE_QUOTE NUMBER* SINGLE_QUOTE;
identifierValue: IDENTIFIER_LOWERCASE | IDENTIFIER_UPPERCASE;

//element
element: openTag elementContent* closeTag | emptyFragment;  
emptyFragment: LEFT_ANGLE_BRACKET RIGHT_ANGLE_BRACKET LEFT_ANGLE_BRACKET SLASH RIGHT_ANGLE_BRACKET;

//open tag
openTag: LEFT_ANGLE_BRACKET identifierValue* RIGHT_ANGLE_BRACKET;

//close tag
closeTag: LEFT_ANGLE_BRACKET SLASH identifierValue* RIGHT_ANGLE_BRACKET;

//content of the element
elementContent: element | valueIndicator;
valueIndicator: LEFT_BRACE identifierValue+ RIGHT_BRACE;  


//variable declaration

// primitive data

// string
stringDeclaration: variableTypes identifierValue+ EQUAL stringValue;

// number
numberDeclaration: variableTypes identifierValue+ EQUAL NUMBER+;

// boolean
booleanDeclaration: variableTypes identifierValue+ EQUAL 
boolean: TRUE | FALSE;

//hook declaration

// useState 
stateSetter: variableTypes statePair EQUAL USE_STATE initialValue;
statePair: LEFT_SQUARE_BRACKET identifierValue+ COMMA identifierValue+ RIGHT_SQUARE_BRACKET;
initialValue: LEFT_PARENTHESIS valueForInitialization* RIGHT_PARENTHESIS;
valueForInitialization: identifierValue+ | NUMBER+ | array | stringValue;
array: LEFT_SQUARE_BRACKET arrayValue* RIGHT_SQUARE_BRACKET;

// useEffect
useEffectCall: USE_EFFECT LEFT_PARENTHESIS callbackFunction COMMA dependencyArray RIGHT_PARENTHESIS;
callbackFunction: LEFT_PARENTHESIS RIGHT_PARENTHESIS IMPLIE LEFT_BRACE content* RIGHT_BRACE;
dependencyArray: LEFT_SQUARE_BRACKET parameter* RIGHT_SQUARE_BRACKET; 

// useCallback
useCallbackCall: USE_CALLBACK LEFT_PARENTHESIS callbackFunction COMMA dependencyArray RIGHT_PARENTHESIS;

// arrow function
arrowFunction: variableTypes identifierValue+ EQUAL parameter_list IMPLIE LEFT_BRACE content* RIGHT_BRACE;   

//normal function


//statement
hook: USE_EFFECT | USE_CALLBACK | USE_MEMO | USE_STATE;
import_statement: IMPORT LEFT_BRACE hook* RIGHT_BRACE FROM REACT (SEMICOLON)?;
return_statement: RETURN LEFT_PARENTHESIS element RIGHT_PARENTHESIS;

//console.log command
consoleCommand: CONSOLE DOT LOG LEFT_PARENTHESIS stringValue RIGHT_PARENTHESIS;

//tokens
RETURN: 'return';
CONST: 'const';
VAR: 'var';
LET:'let';
IMPORT:'import';
FROM:'from';
REACT:'react';
CONSOLE:'console';
LOG:'log';
TRUE:'true';
FALSE:'false';

FUNCTION: 'function';
EXPORT: 'export default';

USE_EFFECT:'useEffect';
USE_STATE:'useState';
USE_CALLBACK:'useCallback';
USE_MEMO:'useMemo';

LEFT_PARENTHESIS:'(';
RIGHT_PARENTHESIS:')';
LEFT_BRACE:'{';
RIGHT_BRACE:'}';
LEFT_SQUARE_BRACKET:'[';
RIGHT_SQUARE_BRACKET:']';
COMMA: ',';
EQUAL:'=';
SINGLE_QUOTE:'\'';
DOUBLE_QUOTE:'\u0022';
LEFT_ANGLE_BRACKET: '<';
RIGHT_ANGLE_BRACKET:'>';
SLASH: '/';
SEMICOLON: ';';
IMPLIE:'=>';
DOT:'.';

IDENTIFIER_UPPERCASE: [A-Z];
IDENTIFIER_LOWERCASE: [a-z];

NUMBER:[0-9]; 

WS: [ \t\r\n]+ -> skip;
