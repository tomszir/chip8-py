import time
import numpy as np
import pygame as pg

from random import randint
from typing import Optional, cast

from .rom import ROM
from .theme import Theme
from .state import State, StateType
from .drivers import Driver, AudioDriver, InputDriver, GraphicsDriver

DEBUG_MODE = False


class Chip8:
  def __init__(self, rom_path: Optional[str] = None):
    self.running = True
    self.current_instruction = 0

    self.rom: Optional[ROM] = None

    self.drivers: dict[str, Driver] = {
        'audio': AudioDriver(self),
        'graphics': GraphicsDriver(self),
        'input': InputDriver(self)
    }

    self.v = [0] * 16
    self.stack = [0] * 16

    self.ram = [0] * 0xfff
    self.vram = np.zeros((32, 64), dtype=int).tolist()
    self.vram_changed = False

    self.i = 0
    self.pc = 0x200
    self.sp = 0

    self.delay_timer = 0
    self.sound_timer = 0

    self.keys_pressed = [False] * 16

    self.clock = pg.time.Clock()
    self.fps = 1000
    self.timer_fps = 60
    self.t = time.time()

    # If a rom path is speicfied load a ROM
    if rom_path != None:
      self.load_rom_from_path(cast(str, rom_path))

  def load_rom_from_path(self, rom_path: str):
    rom = cast(ROM, ROM.load_from_file(cast(str, rom_path)))
    self.load_rom(rom)

  def load_rom(self, rom: ROM):
    self.rom = rom
    self.v = [0] * 16
    self.stack = [0] * 16
    self.sp = 0
    self.pc = 0x200
    self.i = 0
    self.vram = np.zeros((32, 64), dtype=int).tolist()
    self.vram_changed = False
    self.ram = self.rom.data

  def set_theme(self, theme: Theme):
    cast(GraphicsDriver, self.drivers['graphics']).theme = theme

  def run(self):
    while self.running:
      self.run_cycle()
      self.drivers['input'].handle_cycle()
      self.drivers['graphics'].handle_cycle()
      self.drivers['audio'].handle_cycle()
      self.clock.tick(self.fps)

  def run_cycle(self):
    # Timers run 60 times per second
    if time.time() - self.t > 1 / self.timer_fps:
      if self.delay_timer > 0:
        self.delay_timer -= 1

      if self.sound_timer > 0:
        self.sound_timer -= 1
      self.t = time.time()

    opcode = self.get_current_opcode()

    if DEBUG_MODE:
      print(f"[{self.current_instruction}] Running opcode - {hex(opcode)}")
    self.current_instruction += 1

    # Execute and get return state of opcode
    state = self.run_opcode(opcode)

    # Handle empty opcode functions
    if state == None:
      state = State.NotImplemented()
    state_type, addr = state

    # Handle current state
    if state_type in [StateType.NEXT, StateType.SKIP, StateType.BLOCK]:
      self.pc += addr
      self.pc &= 0xfff
    elif state_type == StateType.JUMP:
      self.pc = addr
    else:
      raise NotImplementedError

  def get_current_opcode(self):
    return (self.ram[self.pc] << 8) | self.ram[self.pc + 1]

  def run_opcode(self, opcode: int):
    # Opcode nibbles
    n1 = (opcode & 0xf000) >> 12
    n2 = (opcode & 0x0f00) >> 8
    n3 = (opcode & 0x00f0) >> 4
    n4 = (opcode & 0x000f)

    # Variables
    x = n2
    y = n3
    n = n4
    kk = opcode & 0x00ff
    nnn = opcode & 0x0fff

    # 0x0
    if n1 == 0x00:
      if n3 == 0x0e:
        if n4 == 0x0e:
          return self.op_00ee()
        return self.op_00e0()
    # 0x1
    elif n1 == 0x01:
      return self.op_1nnn(nnn)
    # 0x2
    elif n1 == 0x02:
      return self.op_2nnn(nnn)
    # 0x3
    elif n1 == 0x03:
      return self.op_3xkk(x, kk)
    # 0x4
    elif n1 == 0x04:
      return self.op_4xkk(x, kk)
    # 0x5
    elif n1 == 0x05:
      return self.op_5xy0(x, y)
    # 0x06
    elif n1 == 0x06:
      return self.op_6xkk(x, kk)
    # 0x07
    elif n1 == 0x07:
      return self.op_7xkk(x, kk)
    # 0x08
    elif n1 == 0x08:
      if n4 == 0x00:
        return self.op_8xy0(x, y)
      elif n4 == 0x01:
        return self.op_8xy1(x, y)
      elif n4 == 0x02:
        return self.op_8xy2(x, y)
      elif n4 == 0x03:
        return self.op_8xy3(x, y)
      elif n4 == 0x04:
        return self.op_8xy4(x, y)
      elif n4 == 0x05:
        return self.op_8xy5(x, y)
      elif n4 == 0x06:
        return self.op_8xy6(x, y)
      elif n4 == 0x07:
        return self.op_8xy7(x, y)
      elif n4 == 0x0e:
        return self.op_8xye(x, y)
    # 0x09
    elif n1 == 0x09:
      return self.op_9xy0(x, y)
    # 0x0a
    elif n1 == 0x0a:
      return self.op_annn(nnn)
    # 0x0b
    elif n1 == 0x0b:
      return self.op_bnnn(nnn)
    # 0x0c
    elif n1 == 0x0c:
      return self.op_cxkk(x, kk)
    # 0x0d
    elif n1 == 0x0d:
      return self.op_dxyn(x, y, n)
    # 0x0e
    elif n1 == 0x0e:
      if n3 == 0x09:
        if n4 == 0x0e:
          return self.op_ex9e(x)
      elif n3 == 0x0a:
        if n4 == 0x01:
          return self.op_exa1(x)
    # 0x0f
    elif n1 == 0x0f:
      if n3 == 0x00:
        if n4 == 0x07:
          return self.op_fx07(x)
        elif n4 == 0x0a:
          return self.op_fx0a(x)
      elif n3 == 0x01:
        if n4 == 0x05:
          return self.op_fx15(x)
        elif n4 == 0x08:
          return self.op_fx18(x)
        elif n4 == 0x0e:
          return self.op_fx1e(x)
      elif n3 == 0x02:
        if n4 == 0x09:
          return self.op_fx29(x)
      elif n3 == 0x03:
        if n4 == 0x03:
          return self.op_fx33(x)
      elif n3 == 0x05:
        if n4 == 0x05:
          return self.op_fx55(x)
      elif n3 == 0x06:
        return self.op_fx65(x)

    return State.NotImplemented()

  def op_00e0(self):
    """
    Clear the display.
    """
    for x in range(64):
      for y in range(32):
        self.vram[y][x] = 0
    self.vram_changed = True
    return State.Next()

  def op_00ee(self):
    """
    Return from a subroutine.
    """
    self.sp -= 1
    return State.Jump(self.stack[self.sp])

  def op_1nnn(self, nnn):
    """
    Jump to location nnn.
    """
    return State.Jump(nnn)

  def op_2nnn(self, nnn):
    """
    Call subroutine at nnn.
    """
    self.stack[self.sp] = self.pc + 2
    self.sp += 1
    return State.Jump(nnn)

  def op_3xkk(self, x, kk):
    """
    Skip next instruction if Vx = kk.
    """
    return State.SkipIf(self.v[x] == kk)

  def op_4xkk(self, x, kk):
    """
    Skip next instruction if Vx != kk.
    """
    return State.SkipIf(self.v[x] != kk)

  def op_5xy0(self, x, y):
    """
    Skip next instruction if Vx = Vy.
    """
    return State.SkipIf(self.v[x] == self.v[y])

  def op_6xkk(self, x, kk):
    """
    Set Vx = kk.
    """
    self.v[x] = kk
    return State.Next()

  def op_7xkk(self, x, kk):
    """
    Set Vx = Vx + kk.
    """
    self.v[x] += kk
    self.v[x] &= 0xff
    return State.Next()

  def op_8xy0(self, x, y):
    """
    Set Vx = Vy.
    """
    self.v[x] = self.v[y]
    return State.Next()

  def op_8xy1(self, x, y):
    """
    Set Vx = Vx OR Vy.
    """
    self.v[x] |= self.v[y]
    return State.Next()

  def op_8xy2(self, x, y):
    """
    Set Vx = Vx AND Vy.
    """
    self.v[x] &= self.v[y]
    return State.Next()

  def op_8xy3(self, x, y):
    """
    Set Vx = Vx XOR Vy.
    """
    self.v[x] ^= self.v[y]
    return State.Next()

  def op_8xy4(self, x, y):
    """
    Set Vx = Vx + Vy, set VF = carry.
    """
    result = self.v[x] + self.v[y]
    self.v[0xf] = 1 if result > 255 else 0
    self.v[x] = result & 0xff
    return State.Next()

  def op_8xy5(self, x, y):
    """
    Set Vx = Vx - Vy, set VF = NOT borrow.
    """
    result = self.v[x] - self.v[y]
    self.v[0xf] = 1 if result > 0 else 0
    self.v[x] = result if result > 0 else 0xff - abs(result)
    return State.Next()

  def op_8xy6(self, x, y):
    """
    Set Vx = Vx SHR 1.
    """
    self.v[0x0f] = self.v[x] & 1
    self.v[x] >>= 1
    return State.Next()

  def op_8xy7(self, x, y):
    """
    Set Vx = Vy - Vx, set VF = NOT borrow.
    """
    result = self.v[y] - self.v[x]
    self.v[0xf] = 1 if result > 0 else 0
    self.v[x] = result if result > 0 else 0xff - abs(result)
    return State.Next()

  def op_8xye(self, x, y):
    """
    Set Vx = Vx SHL 1.
    """
    self.v[0xf] = (self.v[x] & 0b10000000) >> 7
    self.v[x] <<= 1
    self.v[x] &= 0xff
    return State.Next()

  def op_9xy0(self, x, y):
    """
    Skip next instruction if Vx != Vy.
    """
    return State.SkipIf(self.v[x] != self.v[y])

  def op_annn(self, nnn):
    """
    Set I = nnn.
    """
    self.i = nnn
    return State.Next()

  def op_bnnn(self, nnn):
    """
    Jump to location nnn + V0.
    """
    return State.Jump(nnn + self.v[0])

  def op_cxkk(self, x, kk):
    """
    Set Vx = random byte AND kk.
    """
    self.v[x] = kk & randint(0, 255)
    return State.Next()

  def op_dxyn(self, x, y, n):
    """
    Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.
    """
    x = self.v[x] & 63
    y = self.v[y] & 31

    self.v[0xf] = 0

    for yline in range(n):
      yy = (y + yline) & 31
      pixel = self.ram[self.i + yline]

      for xline in range(8):
        if pixel & (0x80 >> xline) != 0:
          xx = (x + xline) & 63

          if self.vram[yy][xx] == 1:
            self.v[0xf] = 1
          self.vram[yy][xx] ^= 1
    self.vram_changed = True
    return State.Next()

  def op_ex9e(self, x):
    """
    Skip next instruction if key with the value of Vx is pressed.
    """
    return State.SkipIf(self.keys_pressed[self.v[x]])

  def op_exa1(self, x):
    """
    Skip next instruction if key with the value of Vx is not pressed.
    """
    return State.SkipIf(not self.keys_pressed[self.v[x]])

  def op_fx07(self, x):
    """
    Set Vx = delay timer value.
    """
    self.v[x] = self.delay_timer
    return State.Next()

  def op_fx0a(self, x):
    """
    Wait for a key press, store the value of the key in Vx.
    """
    key_pressed = self.drivers['input'].get_key()

    if key_pressed == None:
      return State.Next()

    self.v[x] = key_pressed
    return State.Block()

  def op_fx15(self, x):
    """
    Set delay timer = Vx.
    """
    self.delay_timer = self.v[x]
    return State.Next()

  def op_fx18(self, x):
    """
    Set sound timer = Vx.
    """
    self.sound_timer = self.v[x]
    return State.Next()

  def op_fx1e(self, x):
    """
    Set I = I + Vx. Set Vf to 1 if it overflows.
    """
    self.v[0xf] = 1 if self.i + self.v[x] > 0xfff else 0
    self.i += self.v[x]
    self.i &= 0xfff
    return State.Next()

  def op_fx29(self, x):
    """
    Set I = location of sprite for digit Vx.
    """
    self.i = self.v[x] * 0x5
    self.i &= 0xfff
    return State.Next()

  def op_fx33(self, x):
    """
    Store BCD representation of Vx in memory locations I, I+1, and I+2.
    """
    vx = self.v[x]
    self.ram[self.i] = vx // 100
    self.ram[self.i + 1] = (vx // 10) % 10
    self.ram[self.i + 2] = (vx % 100) % 10
    return State.Next()

  def op_fx55(self, x):
    """
    Store registers V0 through Vx in memory starting at location I.
    """
    for i in range(x + 1):
      self.ram[self.i + i] = self.v[i]
    return State.Next()

  def op_fx65(self, x):
    """
    Read registers V0 through Vx from memory starting at location I.
    """
    for i in range(x + 1):
      self.v[i] = self.ram[self.i + i]
    return State.Next()
