from dfa256 import DFA

class Scanner:
  def __init__(self, dfa, code):
    self.dfa = dfa
    self.seekp = -1
    self.code = code

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

  def eof(self):
    return self.seekp == len(self.code)
  
  def scan(self):
    tokens = []
    errors = []
    lexeme = ''
    line = 0
    while not self.eof():
      next_char = self.peekchar()
      if next_char == '\n':
        line += 1
      result = self.dfa.read(next_char)
      if result > 0:
        tokens.append((lexeme, result))
      elif result == -1:
        errors.append((lexeme, line, self.seekp))