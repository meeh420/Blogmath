# -*- coding: utf-8 -*-

import re
import sys

TOKEN_IDENTIFIER = 1
TOKEN_KEYWORD = 2
TOKEN_NUMBER = 3
TOKEN_OPERATION = 4
TOKEN_BRACEOPEN = 5
TOKEN_BRACECLOSE = 6
TOKEN_ASSIGN = 7
TOKEN_SEMICOLON = 8

RESERVED_KEYWORDS = ["var", "lambda"]

re_identifier = re.compile("^[a-zA-Z][a-zA-Z0-9_]*")
re_number = re.compile("^[0-9]+\.?[0-9]*")
OPERATIONS = ["+", "-", "*", "/", "^"]

# For nice output used in Token.__str__ and Token.get_type_string 
tokens_natural = {
    TOKEN_IDENTIFIER: "Identifier",
    TOKEN_KEYWORD: "Keyword",
    TOKEN_NUMBER: "Number",
    TOKEN_OPERATION: "Operation",
    TOKEN_BRACEOPEN: "Open brace",
    TOKEN_BRACECLOSE: "Closed brace",
    TOKEN_ASSIGN: "Assign",
    TOKEN_SEMICOLON: "Semicolon",
}

class Token(object):
    def __init__(self, line, col, typ, content):
        self.line = line
        self.col = col
        self.type = typ
        self.content = content
    
    def get_type_string(self):
        return tokens_natural[self.type]
    
    def __str__(self):
        return "<Token line=%d col=%d type=%s content='%s'>" % \
            (self.line, self.col, self.get_type_string(), self.content)

def error(line, col, msg):
    sys.exit("[Syntaxerror Line %d Col %d] %s" % (line, col, msg))

def tokenize(src):
    tokens = []
    
    line = 1
    col = 1
    
    while len(src) > 0:
        if re_identifier.match(src):
            content = re_identifier.findall(src)[0]
            
            if content in RESERVED_KEYWORDS:
                tokens.append(Token(line, col, TOKEN_KEYWORD, content))
            else:
                tokens.append(Token(line, col, TOKEN_IDENTIFIER, content))
            
            src = src[len(content):] # Anfang des src verschieben
            col += len(content) # Column addieren
        elif re_number.match(src):
            content = re_number.findall(src)[0]
            tokens.append(Token(line, col, TOKEN_NUMBER, content))
            
            src = src[len(content):] # Anfang des src verschieben
            col += len(content) # Column addieren
        elif src.startswith("//"):
            # Behandlung des Kommentars
            while len(src) > 0 and src[0] != "\n":
                src = src[1:]
            
            # Zeilenende erreicht
            line += 1
            col = 1
            src = src[1:]
        elif src[0] == ";":
            tokens.append(Token(line, col, TOKEN_SEMICOLON, src[0]))
            col += 1
            src = src[1:]
        elif src[0] == "=":
            tokens.append(Token(line, col, TOKEN_ASSIGN, src[0]))
            col += 1
            src = src[1:]
        elif src[0] in OPERATIONS:
            tokens.append(Token(line, col, TOKEN_OPERATION, src[0]))
            col += 1
            src = src[1:]
        elif src[0] == "(":
            tokens.append(Token(line, col, TOKEN_BRACEOPEN, src[0]))
            col += 1
            src = src[1:]
        elif src[0] == ")":
            tokens.append(Token(line, col, TOKEN_BRACECLOSE, src[0]))
            col += 1
            src = src[1:]
        elif src[0] in [" ", "\t", "\r"]:
            # Whitespace ignorieren
            col += 1
            src = src[1:]
        elif src[0] == '\n':
            # Zeilenumbruch weitestgehend ignorieren, jedoch Zeile und Spalte aktualisieren
            line += 1
            col = 1
            src = src[1:]
        else:
            error(line, col, "Unknown character '%c' (%d)" % (src[0], ord(src[0])))
    
    return tokens

if __name__ == "__main__":
    # Test tokenize
    
    tokens = tokenize("""
    var c = 2; // Exponent
    var s = 0.5;

    // Funktion zur Potenzierung
    lambda pow(a) = a^c;
    
    // Funktion zum Wurzelziehen
    lambda sqrt(a) = a^s;

    // Ergebnis berechnen von 5^2
    var result = pow(5);
    
    // Ergebnis berechnen von 25^0.5 (Wurzel von 25)
    var result2 = sqrt(result);

    // Ergebnis ausgeben
    print(result);   // Gibt 25 aus
    print(result2);  // Gibt 5 aus
    """.strip())

    for token in tokens:
        print token
