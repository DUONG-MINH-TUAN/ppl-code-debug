parser grammar codeDebugParser;

options {
    tokenVocab=codeDebugLexer;  
}

// Parser rules 
program: main_structure EOF; 

main_structure: (import_statement)? function_declaration*;

// Function declaration with unique IDENTIFIER
function_declaration: FUNCTION IDENTIFIER parameter_list body_function
                    | EXPORT FUNCTION IDENTIFIER parameter_list body_function;

// Parameter in functional component
parameter_list: LEFT_PARENTHESIS parameter* RIGHT_PARENTHESIS 
              | LEFT_PARENTHESIS LEFT_BRACE parameter* RIGHT_BRACE RIGHT_PARENTHESIS;
parameter: IDENTIFIER (COMMA IDENTIFIER)*;    

// Body of the functional component
body_function: LEFT_BRACE content* RIGHT_BRACE; 

// Content of the body of the function
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
       | variableDeclaration stat_breakDown;

// Types of variable
variableTypes: CONST | VAR | LET;

// General variable declaration
variableDeclaration: variableTypes IDENTIFIER EQUAL (stringValue | NUMBER | boolean | BIGINT_LITERAL | NULL | SYMBOL_FUNC | array | NEW DATE_FUNC);

// Values for types 
array: LEFT_SQUARE_BRACKET arrayValue* RIGHT_SQUARE_BRACKET;
numberArray: NUMBER (COMMA NUMBER)*;
stringArray: stringValue (COMMA stringValue)*;
arrayArray: array (COMMA array)*;
arrayValue: numberArray | stringArray | arrayArray;
stringValue: STRING_VALUE;

// Element with matching open and close tags
element: openTag elementContent* closeTag
    | fragmentOpen elementContent* fragmentClose
    | emptyFragment;
emptyFragment: LEFT_ANGLE_BRACKET RIGHT_ANGLE_BRACKET LEFT_ANGLE_BRACKET SLASH RIGHT_ANGLE_BRACKET; // <></>
fragmentOpen: LEFT_ANGLE_BRACKET RIGHT_ANGLE_BRACKET; // <>
fragmentClose: LEFT_ANGLE_BRACKET SLASH RIGHT_ANGLE_BRACKET; // </>
openTag: LEFT_ANGLE_BRACKET IDENTIFIER RIGHT_ANGLE_BRACKET;
closeTag: LEFT_ANGLE_BRACKET SLASH IDENTIFIER RIGHT_ANGLE_BRACKET; // Ensure IDENTIFIER matches openTag

// Content of the element
elementContent: element | valueIndicator;
valueIndicator: LEFT_BRACE IDENTIFIER RIGHT_BRACE;  

// Primitive data
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

// Hook declaration
stateSetter: variableTypes statePair EQUAL USE_STATE initialValue;
statePair: LEFT_SQUARE_BRACKET IDENTIFIER COMMA IDENTIFIER RIGHT_SQUARE_BRACKET;
initialValue: LEFT_PARENTHESIS valueForInitialization* RIGHT_PARENTHESIS;
valueForInitialization: IDENTIFIER | NUMBER+ | array | stringValue;

// useEffect
useEffectCall: USE_EFFECT LEFT_PARENTHESIS callbackFunction COMMA dependencyArray RIGHT_PARENTHESIS;
callbackFunction: LEFT_PARENTHESIS RIGHT_PARENTHESIS IMPLIE LEFT_BRACE content* RIGHT_BRACE;
dependencyArray: LEFT_SQUARE_BRACKET parameter* RIGHT_SQUARE_BRACKET; 

// useCallback
useCallbackCall: USE_CALLBACK LEFT_PARENTHESIS callbackFunction COMMA dependencyArray RIGHT_PARENTHESIS;

// arrow function
arrowFunction: variableTypes IDENTIFIER EQUAL parameter_list IMPLIE LEFT_BRACE content* RIGHT_BRACE;   

// Statement
hook: USE_EFFECT | USE_CALLBACK | USE_MEMO | USE_STATE;
import_statement: IMPORT LEFT_BRACE hook (COMMA hook)* RIGHT_BRACE FROM REACT stat_breakDown;
return_statement: RETURN LEFT_PARENTHESIS element RIGHT_PARENTHESIS;

// Console.log command
consoleCommand: CONSOLE DOT LOG LEFT_PARENTHESIS (stringValue | IDENTIFIER)? RIGHT_PARENTHESIS;

// Statement Breakdown
stat_breakDown: NEWLINE (SEMICOLON)? | SEMICOLON;

// Error Handling
errorRule: .+? (SEMICOLON | RIGHT_BRACE | EOF);