from dfa256 import DFA
from enum import Enum

class Scanner:
  class Token(Enum):
  #Palabras reservadas (tipos, bifurcadores, for, etc)
    TVIDEO = 1
    TTIME = 2
    FOR = 3
    IN = 4
    IF = 5
    ELSE = 6
    PRINT = 7
    PLAY = 8
    AND = 9
    OR = 10
    XOR = 11
    NOT = 12
    ID = 13
  #Símbolos (Operadores lógicos, aritméticos, comparadores, etc)
    CONCAT = 14
    REPEAT = 15
    ACCEL = 16
    ASSIGN = 17

    EQUALITY = 18
    LESS_THAN = 19
    MORE_THAN = 20
    LESS_EQ_THAN = 21
    MORE_EQ_THAN = 22
    NOT_EQUAL = 23

    OR_BRACKET = 24#OPEN ROUND BRACKET
    CR_BRACKET = 25#CLOSED ROUND BRACKET
    OS_BRACKET = 26#OPEN SQUARE BRACKET
    CS_BRACKET = 27#CLOSED SQUARE BRACKET
    OPEN_BRACE = 28
    CLOSED_BRACE = 29

    VIDEO_SLICE = 30
    RANGE = 31
    TIMESTAMP_SEP = 32

    JUMP_LINE = 33

  #Literales
    STRING = 34
    TIME = 35


  def __init__(self, code):
    self.dfa = self.build_automata()
    self.seekp = -1
    self.code = code

  def build_automata(self):
    T = self.Token
    final_states = [(2, T.STRING), (3, T.TIME), (4, T.TIME), (5, T.ID), (6, T.ASSIGN),
                    (7, T.EQUALITY), (8, T.LESS_THAN), (9, T.LESS_EQ_THAN), (10, T.MORE_THAN),
                    (11, T.MORE_EQ_THAN), (13, T.NOT_EQUAL), (15, T.RANGE), (16, T.ACCEL),
                    (17, T.TIMESTAMP_SEP), (18, T.VIDEO_SLICE), (19, T.OPEN_BRACE),
                    (20, T.CLOSED_BRACE), (21, T.OR_BRACKET), (22, T.CR_BRACKET),
                    (23, T.CONCAT), (24, T.REPEAT), (25, T.OS_BRACKET), (26, T.CS_BRACKET),
                    (27, T.JUMP_LINE)]

    dfa_transitions = {(0, '"', 1), (0, '0', 3), (0, '1..9', 4),
                       (0, 'a..z\|A..Z\|_', 5), (0, '=', 6),
                       (0, '<', 8), (0, '>', 10), (0, '!', 12),
                       (0, '.', 14), (0, ':', 17), (0, '{', 19),
                       (0, '}', 20), (0, '(', 21), (0, ')', 22),
                       (0, '+', 23), (0, '*', 24), (0, '[', 25),
                       (0, ']', 26), (0, '\n', 27), (1, ' ..■', 1),
                       (1, '"', 2), (4, '0..9', 4), (5, '0..9\|a..z\|A..Z\|_', 5),
                       (12, '=', 13), (14, '.', 15), (14, 'x', 16)}

    return DFA(28, final_states, dfa_transitions)

  def getchar(self):
    self.seekp += 1

    if self.seekp < len(self.code):
      return self.code[self.seekp]
    return None

  def peekchar(self):
    peekp = None

    if self.seekp + 1 < len(self.code):
      peekp = self.code[self.seekp + 1]
    return peekp
  
  def backchar(self):
    if self.seekp != -1:
      self.seekp -= 1

  def eof(self):
    return self.seekp == len(self.code)
  
  def scan(self):
    tokens = []
    errors = []
    lexeme = ''
    line = 1
    
    while not self.eof():
      next_char = self.getchar()
      if next_char is not None:
        if next_char == '#':
          while self.getchar() != '\n':
            pass
          line += 1
          continue

        if next_char == '\n':
          line += 1

        result = self.dfa.read(next_char)
        lexeme += next_char

        if result == -1:
          if lexeme != ' ':
            errors.append((lexeme, f'({line}:{self.seekp})'))
          lexeme = ''
        else:
          if result != 0:
            tokens.append((lexeme[:-1], result))
            lexeme = ''
            self.backchar()
    return tokens, errors
  
with open("fine.txt", "r") as archivo:
  code_body = archivo.read()

scanner = Scanner(code_body)
tokens, errors = scanner.scan()
print(tokens)
print(tokens[-1])
print(errors)