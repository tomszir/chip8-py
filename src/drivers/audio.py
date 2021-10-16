import winsound

from .base import Driver


class AudioDriver(Driver):
  def __init__(self, chip8):
    super().__init__(chip8)

  def handle_cycle(self):
    if self.chip8.sound_timer > 0:
      winsound.Beep(2500, 10)
