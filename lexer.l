%{
#include "parser.tab.h"
#include <string.h>
%}

%option noyywrap

%%

[0-9]+          { yylval.num = atoi(yytext); return NUMBER; }
"int"|"float"|"string"|"waypoint"|"flight_level" { yylval.str = strdup(yytext); return TYPE; }

[a-zA-Z_][a-zA-Z0-9_]*  { yylval.str = strdup(yytext); return IDENTIFIER; }
"->"            { return ARROW; }
"="             { return EQUALS; }
"{"             { return LBRACE; }
"}"             { return RBRACE; }
"("             { return LPAREN; }
")"             { return RPAREN; }
","             { return COMMA; }
"function"      { return FUNCTION; }
"if"            { return IF; }
"while"         { return WHILE; }
"return"        { return RETURN; }
";"             { return SEMICOLON; }
"\n"            { return NEWLINE; }
"//"            { /* ignore single-line comments */ }
[ \t\n]+        { /* ignore whitespace */ }
.               { /* catch-all for other characters */ }

%%


