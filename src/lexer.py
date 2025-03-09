"""
Lexer module for the Lunfardo programming language.

This module contains the Lexer class, which is responsible for tokenizing
the input source code into a sequence of tokens that can be processed by
the parser.
"""

from constants import *
from lunfardo_token import Position, Token
from errors.errors import IllegalCharBardo, ExpectedCharBardo
from typing import Tuple, List

class Lexer:
    """
    Lexer class for tokenizing Lunfardo source code.

    This class reads the input text and converts it into a sequence of tokens,
    which represent the smallest units of meaning in the language.
    """

    def __init__(self, fn, text) -> None:
        """
        Initialize the Lexer with a filename and input text.

        Args:
            fn (str): The name of the file being processed.
            text (str): The source code to be tokenized.
        """
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self) -> None:
        """
        Advance the lexer's position to the next character in the input.
        """
        self.pos = self.pos.copy()
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self) -> Tuple[List[Token], IllegalCharBardo | None]:
        """
        Generate a list of tokens from the input text.

        Returns:
            tuple: A tuple containing a list of tokens and an error (if any).
        """
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()

            elif self.current_char == '#':
                self.skip_comment()
                self.advance()

            elif self.current_char in ';\n':
                tokens.append(Token(TT_NEWLINE, pos_start = self.pos))
                self.advance()
            
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            
            elif self.current_char == '"':
                tok, error = self.make_string()
                if error:
                    return [], error
                tokens.append(tok)
            
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start = self.pos))
                self.advance()
            
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start = self.pos))
                self.advance()
            
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start = self.pos))
                self.advance()
            
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start = self.pos))
                self.advance()
            
            elif self.current_char == '^':
                tokens.append(Token(TT_POW, pos_start = self.pos))
                self.advance()
            
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start = self.pos))
                self.advance()
            
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start = self.pos))
                self.advance()
            
            elif self.current_char == '[':
                tokens.append(Token(TT_LSQUARE, pos_start = self.pos))
                self.advance()
            
            elif self.current_char == ']':
                tokens.append(Token(TT_RSQUARE, pos_start = self.pos))
                self.advance()

            elif self.current_char == '{':
                tokens.append(Token(TT_LCURLY, pos_start = self.pos))
                self.advance()
            
            elif self.current_char == '}':
                tokens.append(Token(TT_RCURLY, pos_start = self.pos))
                self.advance()
            
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start = self.pos))
                self.advance()
            
            elif self.current_char == ':':
                tokens.append(Token(TT_COLON, pos_start = self.pos))
                self.advance()

            elif self.current_char == '.':
                tokens.append(Token(TT_DOT, pos_start = self.pos))
                self.advance()
            
            elif self.current_char == '!':
                tok, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(tok)

            elif self.current_char == '=':
                tokens.append(self.make_equals())

            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())

            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharBardo(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start = self.pos))
        return tokens, None
    
    def make_number(self) -> Token:
        """
        Parse and create a number token (integer or float).

        Returns:
            Token: An INT or FLOAT token.
        """
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()
        
        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                
                dot_count += 1
                num_str += '.'
            
            else:
                num_str += self.current_char
            
            self.advance()
            
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        
        return Token(TT_FLOAT, float(num_str), pos_start, self.pos)
    
    def make_string(self) -> Token:
        """
        Parse and create a string token.

        Returns:
            Token: A STRING token.
        """
        string = ''
        pos_start = self.pos.copy()
        escape_char = False
        doublequotes_counter = 1
        self.advance()

        # Empty string
        if self.current_char == '"':
            self.advance()
            return Token(TT_STRING, string, pos_start, self.pos), None

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char is not None and (self.current_char != '"' or escape_char):
            if escape_char:
                string += escape_characters.get(self.current_char, self.current_char)
                escape_char	= False
            else:
                if self.current_char == '\\':
                    escape_char = True
                else:
                    string += self.current_char
            self.advance()
            
            if self.current_char == '"':
                doublequotes_counter += 1

        self.advance()

        if doublequotes_counter < 2:
            return None, ExpectedCharBardo(pos_start, self.pos, 'Se esperaba \'"\'')
        
        return Token(TT_STRING, string, pos_start, self.pos), None
    
    def make_identifier(self) -> Token:
        """
        Parse and create an identifier or keyword token.

        Returns:
            Token: An IDENTIFIER or KEYWORD token.
        """
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)
    
    def make_not_equals(self) -> Tuple[Token | None, ExpectedCharBardo | None]:
        """
        Parse and create a not-equals token.

        Returns:
            tuple: A tuple containing the NE token and an error (if any).
        """
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start = pos_start, pos_end = self.pos), None
        
        self.advance()
        return None, ExpectedCharBardo(pos_start, self.pos, "'=' (después de '!')")
    
    def make_equals(self) -> Token:
        """
        Parse and create an equals or double-equals token.

        Returns:
            Token: An EQ or EE token.
        """
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_EE

        return Token(tok_type, pos_start = pos_start, pos_end = self.pos)
    
    def make_less_than(self) -> Token:
        """
        Parse and create a less-than or less-than-or-equal token.

        Returns:
            Token: An LT or LTE token.
        """
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_LTE

        return Token(tok_type, pos_start = pos_start, pos_end = self.pos)
    
    def make_greater_than(self) -> Token:
        """
        Parse and create a greater-than or greater-than-or-equal token.

        Returns:
            Token: A GT or GTE token.
        """
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_GTE

        return Token(tok_type, pos_start = pos_start, pos_end = self.pos)
    
    def skip_comment(self) -> None:
        self.advance()

        while self.current_char not in ('\n', None):
            self.advance()