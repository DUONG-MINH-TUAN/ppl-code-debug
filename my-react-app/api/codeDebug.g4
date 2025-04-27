grammar codeDebug;

// Parser rules 
program: main_structure; 

// syntax
//main_structure: function_declaration IDENTIFIER parameter_list body_function;
main_structure: function_declaration identifierValue+ parameter_list body_function;

//parameter in functional component
parameter_list:     LEFT_PARENTHESIS identifierValue* RIGHT_PARENTHESIS 
                |   LEFT_PARENTHESIS LEFT_BRACE identifierValue* RIGHT_BRACE RIGHT_PARENTHESIS;



//function declaration
function_declaration:FUNCTION | EXPORT FUNCTION;

//body of the functional component
body_function: LEFT_BRACE content* RIGHT_BRACE; 

// content of the body of the function
content:    stateSetter 
        |   return_statement;
return_statement: RETURN LEFT_PARENTHESIS element RIGHT_PARENTHESIS;


// types of variable
variableTypes: CONST | VAR | LET;


stateSetter: variableTypes statePair EQUAL USE_STATE initialValue (SEMICOLON)?;
statePair: LEFT_SQUARE_BRACKET identifierValue+ COMMA identifierValue+ RIGHT_SQUARE_BRACKET;
initialValue: LEFT_PARENTHESIS valueForInitialization* RIGHT_PARENTHESIS;
valueForInitialization: identifierValue+ | NUMBER+ | array;
array: LEFT_SQUARE_BRACKET arrayValue RIGHT_SQUARE_BRACKET;

//values for types 
numberArray: numberArray COMMA NUMBER+ | NUMBER+;
stringArray: stringArray COMMA identifierValue+ | identifierValue;
arrayValue: numberArray | stringArray;
stringValue: DOUBLE_QUOTE identifierValue+ DOUBLE_QUOTE | SINGLE_QUOTE identifierValue+ SINGLE_QUOTE;
identifierValue: IDENTIFIER_LOWERCASE | IDENTIFIER_UPPERCASE;

//element
element: openTag elementContent* closeTag | emptyFragment;  

emptyFragment: LEFT_ANGLE_BRACKET RIGHT_ANGLE_BRACKET LEFT_ANGLE_BRACKET SLASH RIGHT_ANGLE_BRACKET;  // <></>
//open tag
openTag: LEFT_ANGLE_BRACKET identifierValue* RIGHT_ANGLE_BRACKET;

//close tag
closeTag: LEFT_ANGLE_BRACKET SLASH identifierValue* RIGHT_ANGLE_BRACKET;

//content of the element
elementContent: element | valueIndicator;
valueIndicator: LEFT_BRACE identifierValue+ RIGHT_BRACE;  


//hook declaration


//tokens
RETURN: 'return';
CONST: 'const';
VAR: 'var';
LET:'let';

FUNCTION: 'function';
EXPORT: 'export default';

USE_EFFECT:'useEffect';
USE_STATE:'useState';

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

IDENTIFIER_UPPERCASE: [A-Z];
IDENTIFIER_LOWERCASE: [a-z];

NUMBER:[0-9]; 

WS: [ \t\r\n]+ -> skip;
