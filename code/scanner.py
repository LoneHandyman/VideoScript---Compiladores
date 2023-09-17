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
    DECIMAL = 36

  #Otros
    WHITE_SPACE = 37

  def __init__(self, code):
    self.dfa, self.reserved_words = self.build_lex()
    self.seekp = -1
    self.code = code + '$'

  def build_lex(self):
    T = self.Token
    final_states = [(2, T.STRING), (3, T.TIME), (4, T.TIME), (5, T.ID), (6, T.ASSIGN),
                    (7, T.EQUALITY), (8, T.LESS_THAN), (9, T.LESS_EQ_THAN), (10, T.MORE_THAN),
                    (11, T.MORE_EQ_THAN), (13, T.NOT_EQUAL), (15, T.RANGE), (16, T.ACCEL),
                    (17, T.TIMESTAMP_SEP), (18, T.VIDEO_SLICE), (19, T.OPEN_BRACE),
                    (20, T.CLOSED_BRACE), (21, T.OR_BRACKET), (22, T.CR_BRACKET),
                    (23, T.CONCAT), (24, T.REPEAT), (25, T.OS_BRACKET), (26, T.CS_BRACKET),
                    (27, T.JUMP_LINE), (29, T.DECIMAL), (30, T.DECIMAL), (31, T.WHITE_SPACE)]

    dfa_transitions = {(0, '"', 1), (0, '0', 3), (0, '1..9', 4),
                       (0, 'a..z\|A..Z\|_', 5), (0, '=', 6),
                       (0, '<', 8), (0, '>', 10), (0, '!', 12),
                       (0, '.', 14), (0, ':', 17), (0, '{', 19),
                       (0, '}', 20), (0, '(', 21), (0, ')', 22),
                       (0, '+', 23), (0, '*', 24), (0, '[', 25),
                       (0, ']', 26), (0, '\n', 27), (1, ' \|!\|#..■', 1),
                       (1, '"', 2), (4, '0..9', 4), (5, '0..9\|a..z\|A..Z\|_', 5),
                       (12, '=', 13), (14, '.', 15), (14, 'x', 16),
                       (17, ':', 18), (3, ',', 28), (4, ',', 28), (28, '0..9', 29), 
                       (29, '0..9', 30), (0, ' ', 31)}
    
    reserved_words = {'video': T.TVIDEO, 'time': T.TTIME, 'print': T.PRINT, 'play': T.PLAY,
                      'if': T.IF, 'else': T.ELSE, 'for': T.FOR, 'in': T.IN, 'and': T.AND,
                      'or': T.OR, 'xor': T.XOR, 'not': T.NOT}

    return DFA(32, final_states, dfa_transitions), reserved_words

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
  
  def scan(self):
    tokens = []
    errors = []
    lexeme = ''
    line = 1
    chcount = 0
    while self.peekchar():
      next_char = self.getchar()
      if next_char is not None:
        if next_char == '#':
          while self.getchar() != '\n':
            pass
          line += 1
          chcount = 0
          continue

        result = self.dfa.read(next_char)
        if result == 0:
          lexeme += next_char

        elif result == -1:
          errors.append((lexeme, f'({line}:{chcount})'))
          if len(lexeme) and lexeme[-1] == '\n':
            line += 1
            chcount = 0
          lexeme = ''
          self.dfa.reset()
        else:
          #Renombrar los tokens ids a palabras reservadas si lo requieren
          if result == self.Token.ID:
            if lexeme in self.reserved_words:
              result = self.reserved_words[lexeme]
          if result != self.Token.WHITE_SPACE:
            tokens.append((lexeme, result, f'({line}:{chcount})'))
          if result == self.Token.JUMP_LINE:
            line += 1
            chcount = 0
          lexeme = ''
          self.backchar()
          chcount -= 1
      chcount += 1
    return tokens, errors[:-1]