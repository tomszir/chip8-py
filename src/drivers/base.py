class Driver:
  def __init__(self, chip8):
    self.chip8 = chip8

  def handle_cycle(self):
    raise NotImplementedError
