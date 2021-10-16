import pygame as pg
from pygame import key

from ..theme import Theme
from ..processor import Processor

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


class InputDriver:
  def __init__(self, chip8):
    self.chip8 = chip8

  def get_key(self):
    keys_pressed = pg.key.get_pressed()

    for k, pg_key in KEY_MAP.items():
      if keys_pressed[pg_key]:
        return k
    return None

  def process_input(self, processor: Processor):
    keys = pg.key.get_pressed()

    for k, pk in KEY_MAP.items():
      i = int(k, 16)
      processor.keys_pressed[i] = True if keys[pk] else False

    for e in pg.event.get():
      if e.type == pg.QUIT:
        self.chip8.running = False
      if e.type == pg.KEYDOWN:
        if e.key == pg.K_F1:
          self.chip8.load_rom(processor.rom)
        elif e.key == pg.K_F2:
          self.chip8.graphics.next_theme()
