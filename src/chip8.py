import pygame as pg

from typing import Optional, cast

from .rom import ROM
from .drivers import AudioDriver, InputDriver, GraphicsDriver
from .processor import Processor


class Chip8:
  DEBUG_MODE = False

  def __init__(self, rom_path: Optional[str] = None):
    self.running = True
    self.rom: Optional[ROM] = None

    self.input = InputDriver(self)
    self.audio = AudioDriver()
    self.graphics = GraphicsDriver()

    if rom_path != None:
      self.load_rom_from_path(cast(str, rom_path))

  def load_rom_from_path(self, rom_path: str):
    """
    Loads a Chip8 ROM directly from a file path.
    """
    self.load_rom(ROM.load_from_file(rom_path))

  def load_rom(self, rom: ROM):
    """
    Loads a ROM and restarts the interpreter.
    """
    self.rom = rom
    self.processor = Processor(self, rom)
    pg.display.set_caption(f"Chip8 - {rom.name}")

  def run(self):
    while self.running:
      self.graphics.draw(self.processor.frame_buffer)
      self.input.process_input(self.processor)
      self.audio.process_audio(self.processor)
      self.processor.run_cycle()
