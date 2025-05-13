parser grammar codeDebugParser;

options {
    tokenVocab=codeDebugLexer;  // Tham chiếu đến lexer grammar
}

// Parser rules 
program: main_structure; 

// syntax
main_structure: (import_statement)? function_declaration IDENTIFIER parameter_list body_function;

//main_structure: testContent;

//testContent: dateDeclaration (SEMICOLON)? | return_statement (SEMICOLON)?;
//main_structure: HELLO ;


//parameter in functional component
parameter_list:     LEFT_PARENTHESIS parameter* RIGHT_PARENTHESIS 
                |   LEFT_PARENTHESIS LEFT_BRACE parameter* RIGHT_BRACE RIGHT_PARENTHESIS;
parameter: IDENTIFIER (COMMA IDENTIFIER)*;    
//function declaration
function_declaration:FUNCTION | EXPORT FUNCTION;

//body of the functional component
body_function: LEFT_BRACE content* RIGHT_BRACE; 

// content of the body of the function
content:    stateSetter (SEMICOLON)?
        |   useEffectCall (SEMICOLON)?
        |   bigIntDeclaration (SEMICOLON)?
        |   numberDeclaration (SEMICOLON)?
        |   stringDeclaration (SEMICOLON)?
        |   arrowFunction (SEMICOLON)?
        |   consoleCommand (SEMICOLON)?
        |   useCallbackCall (SEMICOLON)?
        |   dateDeclaration (SEMICOLON)?   
        |   return_statement (SEMICOLON)?;


// types of variable
variableTypes: CONST | VAR | LET;

//values for types 
numberArray: NUMBER (COMMA NUMBER)*;
stringArray: stringValue (COMMA stringValue)*;
arrayValue: numberArray | stringArray;
stringValue: 
                DOUBLE_QUOTE DOUBLE_QUOTE 
        |       SINGLE_QUOTE SINGLE_QUOTE
        |       DOUBLE_QUOTE NUMBER* DOUBLE_QUOTE
        |       SINGLE_QUOTE NUMBER* SINGLE_QUOTE;


//element
element: openTag elementContent* closeTag
    | fragmentOpen elementContent* fragmentClose
    | emptyFragment;
emptyFragment: LEFT_ANGLE_BRACKET RIGHT_ANGLE_BRACKET LEFT_ANGLE_BRACKET SLASH RIGHT_ANGLE_BRACKET; // <></>
fragmentOpen: LEFT_ANGLE_BRACKET RIGHT_ANGLE_BRACKET; // <>
fragmentClose: LEFT_ANGLE_BRACKET SLASH RIGHT_ANGLE_BRACKET; // </>
//open tag
openTag: LEFT_ANGLE_BRACKET IDENTIFIER RIGHT_ANGLE_BRACKET;

//close tag
closeTag: LEFT_ANGLE_BRACKET SLASH IDENTIFIER RIGHT_ANGLE_BRACKET;

//content of the element
elementContent: element | valueIndicator;
valueIndicator: LEFT_BRACE IDENTIFIER RIGHT_BRACE;  


//variable declaration

// primitive data

// string
stringDeclaration: variableTypes IDENTIFIER EQUAL stringValue;

// number
numberDeclaration: variableTypes IDENTIFIER EQUAL NUMBER+;

// boolean
booleanDeclaration: variableTypes IDENTIFIER EQUAL boolean;
boolean: TRUE | FALSE;

// bigInt 
bigIntDeclaration: variableTypes IDENTIFIER EQUAL BIGINT_LITERAL;  

//Do not use the BIGINT TOKEN with the value of 'n' in isolation as it may cause ambiguity.

// undefined value
undefinedDeclaration: variableTypes IDENTIFIER;

// null value
nullDeclaration: variableTypes IDENTIFIER EQUAL NULL;

// symbol value
symbolDeclaration: variableTypes IDENTIFIER EQUAL SYMBOL_FUNC;

// array declaration
arrayDeclaration: variableTypes IDENTIFIER EQUAL array;

// date declaration 
dateDeclaration: variableTypes IDENTIFIER EQUAL NEW SPACE DATE_FUNC;


//hook declaration

// useState 
stateSetter: variableTypes statePair EQUAL USE_STATE initialValue;
statePair: LEFT_SQUARE_BRACKET IDENTIFIER COMMA IDENTIFIER RIGHT_SQUARE_BRACKET;
initialValue: LEFT_PARENTHESIS valueForInitialization* RIGHT_PARENTHESIS;
valueForInitialization: IDENTIFIER | NUMBER+ | array | stringValue;
array: LEFT_SQUARE_BRACKET arrayValue* RIGHT_SQUARE_BRACKET;

// useEffect
useEffectCall: USE_EFFECT LEFT_PARENTHESIS callbackFunction COMMA dependencyArray RIGHT_PARENTHESIS;
callbackFunction: LEFT_PARENTHESIS RIGHT_PARENTHESIS IMPLIE LEFT_BRACE content* RIGHT_BRACE;
dependencyArray: LEFT_SQUARE_BRACKET parameter* RIGHT_SQUARE_BRACKET; 

// useCallback
useCallbackCall: USE_CALLBACK LEFT_PARENTHESIS callbackFunction COMMA dependencyArray RIGHT_PARENTHESIS;

// arrow function
arrowFunction: variableTypes IDENTIFIER EQUAL parameter_list IMPLIE LEFT_BRACE content* RIGHT_BRACE;   

//normal function


//statement
hook: USE_EFFECT | USE_CALLBACK | USE_MEMO | USE_STATE;
import_statement: IMPORT LEFT_BRACE hook* RIGHT_BRACE FROM REACT (SEMICOLON)?;
return_statement: RETURN LEFT_PARENTHESIS element RIGHT_PARENTHESIS;

//console.log command
consoleCommand: CONSOLE DOT LOG LEFT_PARENTHESIS stringValue RIGHT_PARENTHESIS;
