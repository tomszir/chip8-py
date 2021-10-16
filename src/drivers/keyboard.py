import pygame as pg
from pygame import key

from .base import Driver
from ..theme import Theme

KEY_MAP = {
    '0x0': pg.K_x,
    '0x1': pg.K_1,
    '0x2': pg.K_2,
    '0x3': pg.K_3,
    '0x4': pg.K_q,
    '0x5': pg.K_w,
    '0x6': pg.K_e,
    '0x7': pg.K_a,
    '0x8': pg.K_s,
    '0x9': pg.K_d,
    '0xa': pg.K_z,
    '0xb': pg.K_c,
    '0xc': pg.K_4,
    '0xd': pg.K_r,
    '0xe': pg.K_f,
    '0xf': pg.K_v,
}


class InputDriver(Driver):
  def __init__(self, chip8):
    super().__init__(chip8)

  def get_key(self):
    keys_pressed = pg.key.get_pressed()

    for k, pg_key in KEY_MAP.items():
      if keys_pressed[pg_key]:
        return k
    return None

  def handle_cycle(self):
    for e in pg.event.get():
      if e.type == pg.QUIT:
        self.chip8.running = False
      elif e.type == pg.KEYDOWN:
        if e.key == pg.K_F1:
          self.handle_theme_change()
        elif e.key == pg.K_F2:
          self.chip8.load_rom(self.chip8.rom)
    self.handle_chip8_input()

  def handle_theme_change(self):
    # TODO: Move to graphics driver
    theme_list = Theme._member_names_
    cur_theme = self.chip8.drivers['graphics'].theme

    current_theme_index = theme_list.index(cur_theme.name)
    new_theme_index = current_theme_index + 1

    if new_theme_index > len(theme_list) - 1:
      new_theme_index = 0

    self.chip8.drivers['graphics'].theme = Theme[theme_list[new_theme_index]]

  def handle_chip8_input(self):
    keys = pg.key.get_pressed()

    for k, pg_key in KEY_MAP.items():
      self.chip8.keys_pressed[int(k, 16)] = True if keys[pg_key] else False
