grammar UseEffectGrammar;

prog: useEffectCall ;

useEffectCall: 'useEffect' '(' callback ',' dependencyArray ')' ';' ;

callback: '()' '=>' block
        | '(' params ')' '=>' block ;

params: ID (',' ID)* ;

dependencyArray: '[' (ID (',' ID)*)? ']' ;

block: '{' statement* '}' ;

statement: (exprStmt | returnStmt) ';' ;

exprStmt: ID '(' STRING? ')' ;

returnStmt: 'return' exprStmt ;

ID: [a-zA-Z_][a-zA-Z0-9_]* ;
STRING: '"' ~["]* '"' ;
WS: [ \t\r\n]+ -> skip ;