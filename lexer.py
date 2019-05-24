# Lexical analyzer
# Copyright 2019 Art Layese <artiskool@gmail.com>

from constants import *
from token import Token

class Lexer(object):

    def __init__(self, text):
        self.lines = text.split("\n")
        if len(self.lines) == 0:
            self.error()
        self.line = -1
        self.next_line()

    def process_text(self, text):
        lines = text.split("\n")
        new_lines = []
        for line in lines:
            clean_line = line.strip()
            if clean_line and clean_line[0] == '*': # ignore comment
                continue
            new_lines.append(line)
        return "\n".join(new_lines)

    def next_line(self):
        self.line += 1
        if self.line < len(self.lines):
            line = self.lines[self.line].strip()
            if len(line) == 0 or line[0] == '*': # comment
                return self.next_line()
            else:
                self.pos = 0
                self.text = ' ' + self.lines[self.line] # MUST add space before or after
                self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def next_char(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.next_line()


    def error(self):
        raise Exception('Invalid character ' + self.current_char)


    def peek(self, step=1):
        peek_pos = self.pos + step
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]


    def look_back(self, step=1):
        back_pos = self.pos - step
        if back_pos > len(self.text) - 1:
            return None
        else:
            return self.text[back_pos]


    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.next_char()

    def skip_comment(self):
        while self.current_char != '}':
            self.next_char()
        self.next_char()  # the closing curly brace

    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.next_char()

        if self.current_char == '.':
            result += self.current_char
            self.next_char()

            while (
                self.current_char is not None and
                self.current_char.isdigit()
            ):
                result += self.current_char
                self.next_char()

            token = Token('FLOAT_CONST', float(result))
        else:
            token = Token('INT_CONST', int(result))

        return token

    def char(self):
        if self.current_char == '\'':
            char = ''
        else:
            char = self.current_char # this is char
            self.next_char() # move to close single quote
        self.next_char() # move to next character
        return Token('CHAR_CONST', char)

    def string(self):
        result = ''
        while self.current_char is not None:
            if self.current_char == '[' and self.peek(2) == ']': # first
                self.next_char()
                continue
            if self.look_back() == '[' and self.peek() == ']': # middle
                result += self.current_char
                self.next_char()
                continue
            if self.current_char == ']' and self.look_back(2) == '[': # last
                self.next_char()
                continue
            if self.current_char == '"':
                self.next_char()
                break
            result += self.current_char if self.current_char != '#' else "\n"
            self.next_char()
        if result in ['TRUE', 'FALSE']:
            return Token('BOOL_CONST', result)
        return Token('STRING_CONST', result)

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.next_char()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.next_char()
                self.skip_comment()
                continue

            if self.current_char == 'A' and self.peek() == 'S':
                self.next_char()
                self.next_char()
                return Token(AS, 'AS')

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '=' and self.peek() == '=':
                self.next_char()
                self.next_char()
                return Token(EQUAL, '==')

            if self.current_char == '=':
                self.next_char()
                return Token(ASSIGN, '=')

            if self.current_char == ';':
                self.next_char()
                return Token(SEMI, ';')

            if self.current_char == ':':
                self.next_char()
                return Token(COLON, ':')

            if self.current_char == ',':
                self.next_char()
                return Token(COMMA, ',')

            if self.current_char == '+':
                self.next_char()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.next_char()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.next_char()
                return Token(MUL, '*')

            if self.current_char == '%':
                self.next_char()
                return Token(MOD, '%')

            if self.current_char == '/':
                self.next_char()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.next_char()
                return Token(LEFT_PAREN, '(')

            if self.current_char == ')':
                self.next_char()
                return Token(RIGHT_PAREN, ')')

            if self.current_char == '[':
                self.next_char()
                return Token(LEFT_BRACE, '[')

            if self.current_char == ']':
                self.next_char()
                return Token(RIGHT_BRACE, ']')

            if self.current_char == '.':
                self.next_char()
                return Token(DOT, '.')

            if self.current_char == '&':
                self.next_char()
                return Token(AMPERSAND, '&')

            if self.current_char == '>' and self.peek() == '=':
                self.next_char()
                self.next_char()
                return Token(GREATER_EQUAL, '>=')

            if self.current_char == '>':
                self.next_char()
                return Token(GREATER_THAN, '>')

            if self.current_char == '<' and self.peek() == '>':
                self.next_char()
                self.next_char()
                return Token(NOT_EQUAL, '<>')

            if self.current_char == '<' and self.peek() == '=':
                self.next_char()
                self.next_char()
                return Token(LESSER_EQUAL, '<=')

            if self.current_char == '<':
                self.next_char()
                return Token(LESSER_THAN, '<')

            if self.current_char == '\'':
                self.next_char()
                return self.char()

            if self.current_char == '"':
                self.next_char()
                return self.string()

            self.error()

        return Token(EOF, None)

