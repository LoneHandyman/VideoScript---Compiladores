class DFA:

  ERROR = -1
  KEEP_READING = 0

  class State:

    def __init__(self, id):
      self.id = id
      self.transitions = {}
      self.final = -1

    def is_final(self):
      return self.final != -1

    def set_type(self, type=-1):
      self.final = type

    def set_transition(self, symbols, st_end):
      for symbol in symbols:
        if '..' in symbol:
          start, end = symbol.split('..')
          start = ord(start)
          end = ord(end)
          assert(start <= end)
          for char_code in range(start, end + 1):
            self.transitions[char_code] = st_end
        else:
          self.transitions[ord(symbol)] = st_end

    def next(self, symbol):
      if ord(symbol) in self.transitions:
        return self.transitions[ord(symbol)]
      return None

    def info(self):
      print(f'id:{self.id}, final:{self.final}')
      for symbol, end in self.transitions.items():
        print(f'\t{symbol} -> S{end}')

  def __init__(self, st_count, st_finals, transitions) -> None:
    assert(st_count > 0)
    self.states = [self.State(_) for _ in range(st_count)]
    self.current = self.states[0]
    for st, token in st_finals:
      self.states[st].set_type(token)

    for st_from, symbols, st_end in transitions:
      self.states[st_from].set_transition(list(symbols.split('\|')), st_end)

  def reset(self):
    self.current = self.states[0]

  def read(self, symbol):
    next = self.current.next(symbol)
    if next is None:
      if self.current.is_final():
        val = self.current.final
        self.reset()
        return val
      return self.ERROR
    
    self.current = self.states[next]
    return self.KEEP_READING
  
  def display(self):
    for state in self.states:
      state.info()