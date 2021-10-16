import pygame as pg

from ..theme import Theme


class GraphicsDriver:
  def __init__(self, scale=8):
    self.scale = scale
    self.theme = Theme.DEFAULT

    self.display_size = (64 * scale, 32 * scale)
    self.display = pg.display.set_mode(self.display_size)

    pg.display.set_icon(pg.image.load('icon.png'))
    pg.display.set_caption("Chip8")

  def draw(self, frame_buffer: list[int]):
    self.display.fill(self.bg)

    for x in range(64):
      for y in range(32):
        pos = x + (y << 6)

        if not frame_buffer[pos] == 1:
          continue

        rect = (x * self.scale, y * self.scale, self.scale, self.scale)
        pg.draw.rect(self.display, self.fg, rect)
    pg.display.update()

  def next_theme(self):
    themes = Theme._member_names_

    theme_index = themes.index(self.theme.name) + 1
    theme_index = 0 if theme_index >= len(themes) else theme_index

    self.theme = Theme[themes[theme_index]]

  @property
  def bg(self):
    return self.theme.value[0]

  @property
  def fg(self):
    return self.theme.value[1]
