%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void yyerror(const char *s);
int yylex(void);

%}

%locations

%union {
    int num;    
    char* str;  
}

%token <num> NUMBER
%token <str> IDENTIFIER TYPE
%token ARROW EQUALS LBRACE RBRACE LPAREN RPAREN COMMA FUNCTION IF WHILE RETURN NEWLINE SEMICOLON

%%

program:
    statements
    ;

statements:
      statement
    | statements statement
    ;

statement:
      assignment
    | function
    | if_statement
    | while_statement
    | return_statement NEWLINE 
    ;

assignment:
    IDENTIFIER ARROW TYPE EQUALS expression NEWLINE
    ;

function:
    FUNCTION IDENTIFIER LPAREN RPAREN LBRACE statements RBRACE
    ;

if_statement:
    IF LPAREN expression RPAREN statement
    ;

while_statement:
    WHILE LPAREN expression RPAREN LBRACE statements RBRACE
    ;

expression:
      NUMBER
    | IDENTIFIER
    | expression '+' expression
    | expression '-' expression
    | expression '*' expression
    | expression '/' expression
    ;

return_statement:
    RETURN expression
    ;

%%
void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    printf("Parsing...\n");
    yyparse();
    return 0;
}

