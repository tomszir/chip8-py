import pygame as pg

from .base import Driver
from ..theme import Theme


class GraphicsDriver(Driver):
  def __init__(self, chip8, scale=8):
    super().__init__(chip8)

    self.scale = scale
    self.display = pg.display.set_mode((64 * scale, 32 * scale))
    self.theme = Theme.DEFAULT

    pg.display.set_caption("Chip8")

  def handle_cycle(self):
    if not self.chip8.vram_changed:
      return

    # Clear display
    self.display.fill(self.bg)

    # Draw visible pixles
    for x in range(64):
      for y in range(32):
        if not self.chip8.vram[y][x] == 1:
          continue
        rect = (x * self.scale, y * self.scale, self.scale, self.scale)
        pg.draw.rect(self.display, self.fg, rect)

    self.chip8.vram_changed = False
    pg.display.flip()

  @property
  def bg(self):
    return self.theme.value[0]

  @property
  def fg(self):
    return self.theme.value[1]
