import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Keywords
    KEYWORD = "KEYWORD"
    # Identifiers and literals
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    ASSIGN = "ASSIGN"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    # Delimiters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    # Special
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __str__(self):
        return f"<{self.type.value}, '{self.value}', Line:{self.line}, Col:{self.column}>"

class LexicalAnalyzer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Define keywords
        self.keywords = {
            'if', 'else', 'while', 'for', 'int', 'float', 
            'return', 'void', 'main', 'print', 'class', 'public'
        }
        
        # Token specifications (pattern, token_type)
        self.token_specs = [
            ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),
            ('FLOAT', r'\d+\.\d+'),
            ('INTEGER', r'\d+'),
            ('STRING', r'"[^"]*"'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('GREATER_EQUAL', r'>='),
            ('LESS_EQUAL', r'<='),
            ('EQUAL', r'=='),
            ('NOT_EQUAL', r'!='),
            ('ASSIGN', r'='),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULTIPLY', r'\*'),
            ('DIVIDE', r'/'),
            ('LESS_THAN', r'<'),
            ('GREATER_THAN', r'>'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('SEMICOLON', r';'),
            ('COMMA', r','),
            ('WHITESPACE', r'[ \t]+'),
            ('NEWLINE', r'\n'),
        ]
        
        # Combine all patterns into one regex
        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' 
                                     for name, pattern in self.token_specs)
        self.pattern = re.compile(self.token_regex)
    
    def current_char(self) -> Optional[str]:
        if self.position < len(self.source):
            return self.source[self.position]
        return None
    
    def analyze(self) -> List[Token]:
        """Main method to tokenize the source code"""
        for match in self.pattern.finditer(self.source):
            token_type = match.lastgroup
            token_value = match.group()
            
            # Skip whitespace
            if token_type == 'WHITESPACE':
                self.column += len(token_value)
                continue
            
            # Handle newlines
            if token_type == 'NEWLINE':
                self.line += 1
                self.column = 1
                continue
            
            # Create token
            if token_type == 'IDENTIFIER':
                # Check if identifier is a keyword
                if token_value in self.keywords:
                    token = Token(TokenType.KEYWORD, token_value, 
                                self.line, self.column)
                else:
                    token = Token(TokenType.IDENTIFIER, token_value, 
                                self.line, self.column)
            else:
                # Map token type string to TokenType enum
                try:
                    token = Token(TokenType[token_type], token_value, 
                                self.line, self.column)
                except KeyError:
                    token = Token(TokenType.UNKNOWN, token_value, 
                                self.line, self.column)
            
            self.tokens.append(token)
            self.column += len(token_value)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def print_tokens(self):
        """Print all tokens in a formatted manner"""
        print("\n" + "="*70)
        print("LEXICAL ANALYSIS RESULTS")
        print("="*70)
        print(f"{'Token Type':<20} {'Lexeme':<20} {'Line':<8} {'Column':<8}")
        print("-"*70)
        
        for token in self.tokens:
            if token.type != TokenType.EOF:
                print(f"{token.type.value:<20} {token.value:<20} "
                      f"{token.line:<8} {token.column:<8}")
        
        print("="*70)
        print(f"Total Tokens: {len(self.tokens) - 1}")  # Exclude EOF
        print("="*70)

# Example usage
if __name__ == "__main__":
    # Sample source code
    source_code = """
    int main() {
        int x = 10;
        float y = 20.5;
        // This is a comment
        if (x < y) {
            print("x is less than y");
            return 0;
        }
        /* Multi-line
           comment */
        x = x + 1;
    }
    """
    
    print("SOURCE CODE:")
    print(source_code)
    
    # Create lexer and analyze
    lexer = LexicalAnalyzer(source_code)
    tokens = lexer.analyze()
    
    # Print results
    lexer.print_tokens()
    
    # Print individual tokens (optional)
    print("\nDETAILED TOKEN LIST:")
    for token in tokens:
        if token.type != TokenType.EOF:
            print(token)