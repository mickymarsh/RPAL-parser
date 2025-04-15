from .validTokens import validToken, validTokenTypes

import re

def tokenize(text):

    tokens = []
    tokenPatterns = dict(
        Comment = r'//.*',
        Keyword = r'(let|in|fn|where|aug|or|not|gr|ge|ls|le|eq|ne|true|false|nil|dummy|within|and|rec)\b',
        String = r'\'(?:\\\'|[^\'])*\'',
        Identifier = r'[a-zA-Z][a-zA-Z0-9_]*',
        Integer = r'\d+',
        Operator = r'[+\-*<>&.@/:=~|$\#!%^_\[\]{}"\'?]+',
        Space = r'[ \t\n]+',
        Punction = r'[();,]'
    )

    while text:
        matched = False
        for key,value in tokenPatterns.items():
            match = re.match(value, text) #It only matches if the pattern starts at the beginning

            if match:
                # debugging
                print("Matched pattern:", key)       # <--- this is your key!
                print("Matched value :", match.group(0))

                if(key == "Space" or key == "Comment"):
                    matched = True
                    text = text[match.end():]
                else:
                    try:
                        tokenType = validTokenTypes[key]
                        tokens.append(validToken(tokenType, match.group(0)))
                        text = text[match.end():]
                        matched = True
                    except KeyError:
                            raise ValueError(f"Token type '{key}' is not a valid TokenType")
   
                break

            else:
                continue

        if not matched:
            print("Error: Unable to tokenize input")
    
    return tokens
