import time
from random import randint

from .rom import ROM
from .font import Font
from .state import State, StateType


class Processor:
  def __init__(self, chip8, rom: ROM, font: list[int] = Font.DEFAULT):
    self.chip8 = chip8

    self.rom = rom
    self.font = font

    self.V = [0] * 16
    self.stack = [0] * 16
    self.frame_buffer = [0] * 64 * 32
    self.memory = [0] * 4096
    self.keys_pressed = [False] * 16

    self.I = 0
    self.sp = 0
    self.pc = 0x200

    self.delay_timer = 0
    self.sound_timer = 0

    self.time = 0
    self.timer_delay = 1/60
    self.clock_speed = 1/1400

    self.opcode = 0

    self.operations = [
        self.op_00e_,
        self.op_1nnn,
        self.op_2nnn,
        self.op_3xkk,
        self.op_4xkk,
        self.op_5xy0,
        self.op_6xkk,
        self.op_7xkk,
        self.op_8xy_,
        self.op_9xy0,
        self.op_annn,
        self.op_bnnn,
        self.op_cxkk,
        self.op_dxyn,
        self.op_ex__,
        self.op_fx__
    ]

    self.operations_8xy_ = [
        self.op_8xy0,
        self.op_8xy1,
        self.op_8xy2,
        self.op_8xy3,
        self.op_8xy4,
        self.op_8xy5,
        self.op_8xy6,
        self.op_8xy7,
        self.op_none,
        self.op_none,
        self.op_none,
        self.op_none,
        self.op_none,
        self.op_8xye,
    ]

    self.operations_fx__ = [
        self.op_fx0_,
        self.op_fx1_,
        self.op_fx29,
        self.op_fx33,
        self.op_none,
        self.op_fx55,
        self.op_fx65
    ]

    self.load_font_into_memory()
    self.load_rom_into_memory()

  def set_font(self, font: list[int]):
    self.font = font
    self.load_font_into_memory()

  def load_font_into_memory(self):
    for i in range(len(self.font)):
      self.memory[i] = self.font[i]

  def load_rom_into_memory(self):
    for i in range(len(self.rom.data)):
      self.memory[i + 0x200] = self.rom.data[i]

  def run_cycle(self):
    if time.time() - self.time > self.timer_delay:
      if self.delay_timer > 0:
        self.delay_timer -= 1
      if self.sound_timer > 0:
        self.sound_timer -= 1
      self.time = time.time()

    self.opcode = self.get_opcode()
    [state_type, addr] = self.operations[(self.opcode & 0xf000) >> 12]()

    if state_type in [StateType.NEXT, StateType.SKIP]:
      self.pc = (self.pc + addr) & 0xfff
    elif state_type == StateType.JUMP:
      self.pc = addr
    else:
      raise NotImplementedError

    time.sleep(self.clock_speed)

  def get_opcode(self):
    return (self.memory[self.pc] << 8) | self.memory[self.pc + 1]

  def get_x(self):
    return (self.opcode & 0x0f00) >> 8

  def get_y(self):
    return (self.opcode & 0x00f0) >> 4

  def get_n(self):
    return (self.opcode & 0x000f)

  def get_kk(self):
    return (self.opcode & 0x00ff)

  def get_nnn(self):
    return (self.opcode & 0x0fff)

  def op_none(self):
    """
    Empty operation.
    """
    return State.NotImplemented()

  def op_00e_(self):
    """
    Handles 0x00e_ operations.
    """
    if self.get_n() == 0x0e:
      return self.op_00ee()
    return self.op_00e0()

  def op_00e0(self):
    """
    Clear the display.
    """
    self.frame_buffer = [0] * 4096
    return State.Next()

  def op_00ee(self):
    """
    Return from a subroutine.
    """
    self.sp -= 1
    return State.Jump(self.stack[self.sp])

  def op_1nnn(self):
    """
    Jump to location nnn.
    """
    return State.Jump(self.get_nnn())

  def op_2nnn(self):
    """
    Call subroutine at nnn.
    """
    self.stack[self.sp] = self.pc + 2
    self.sp += 1
    return State.Jump(self.get_nnn())

  def op_3xkk(self):
    """
    Skip next instruction if Vx = kk.
    """
    x = self.get_x()
    kk = self.get_kk()
    return State.SkipIf(self.V[x] == kk)

  def op_4xkk(self):
    """
    Skip next instruction if Vx != kk.
    """
    x = self.get_x()
    kk = self.get_kk()
    return State.SkipIf(self.V[x] != kk)

  def op_5xy0(self):
    """
    Skip next instruction if Vx = Vy.
    """
    x = self.get_x()
    y = self.get_y()
    return State.SkipIf(self.V[x] == self.V[y])

  def op_6xkk(self):
    """
    Set Vx = kk.
    """
    self.V[self.get_x()] = self.get_kk()
    return State.Next()

  def op_7xkk(self):
    """
    Set Vx = Vx + kk.
    """
    x = self.get_x()
    kk = self.get_kk()
    vx = self.V[x]
    self.V[x] = (vx + kk) & 0xff
    return State.Next()

  def op_8xy_(self):
    """
    Handles 0x8xy- operations.
    """
    return self.operations_8xy_[self.get_n()]()

  def op_8xy0(self):
    """
    Set Vx = Vy.
    """
    x = self.get_x()
    y = self.get_y()
    self.V[x] = self.V[y]
    return State.Next()

  def op_8xy1(self):
    """
    Set Vx = Vx OR Vy.
    """
    x = self.get_x()
    y = self.get_y()
    self.V[x] |= self.V[y]
    return State.Next()

  def op_8xy2(self):
    """
    Set Vx = Vx AND Vy.
    """
    x = self.get_x()
    y = self.get_y()
    self.V[x] &= self.V[y]
    return State.Next()

  def op_8xy3(self):
    """
    Set Vx = Vx XOR Vy.
    """
    x = self.get_x()
    y = self.get_y()
    self.V[x] ^= self.V[y]
    return State.Next()

  def op_8xy4(self):
    """
    Set Vx = Vx + Vy, set VF = carry.
    """
    x = self.get_x()
    y = self.get_y()
    result = self.V[x] + self.V[y]
    self.V[0xf] = 1 if result > 255 else 0
    self.V[x] = result & 0xff
    return State.Next()

  def op_8xy5(self):
    """
    Set Vx = Vx - Vy, set VF = NOT borrow.
    """
    x = self.get_x()
    y = self.get_y()
    result = self.V[x] - self.V[y]
    self.V[0xf] = 1 if result > 0 else 0
    self.V[x] = result if result > 0 else 0xff - abs(result)
    return State.Next()

  def op_8xy6(self):
    """
    Set Vx = Vx SHR 1.
    """
    x = self.get_x()
    self.V[0x0f] = self.V[x] & 1
    self.V[x] >>= 1
    return State.Next()

  def op_8xy7(self):
    """
    Set Vx = Vy - Vx, set VF = NOT borrow.
    """
    x = self.get_x()
    y = self.get_y()
    result = self.V[y] - self.V[x]
    self.V[0xf] = 1 if result > 0 else 0
    self.V[x] = result if result > 0 else 0xff - abs(result)
    return State.Next()

  def op_8xye(self):
    """
    Set Vx = Vx SHL 1.
    """
    x = self.get_x()
    Vx = self.V[x]
    self.V[0xf] = (Vx & 0b10000000) >> 7
    self.V[x] = (Vx << 1) & 0xff
    return State.Next()

  def op_9xy0(self):
    """
    Skip next instruction if Vx != Vy.
    """
    x = self.get_x()
    y = self.get_y()
    return State.SkipIf(self.V[x] != self.V[y])

  def op_annn(self):
    """
    Set I = nnn.
    """
    self.I = self.get_nnn()
    return State.Next()

  def op_bnnn(self):
    """
    Jump to location nnn + V0.
    """
    nnn = self.get_nnn()
    return State.Jump(nnn + self.V[0])

  def op_cxkk(self):
    """
    Set Vx = random byte AND kk.
    """
    x = self.get_x()
    kk = self.get_kk()
    self.V[x] = kk & randint(0, 255)
    return State.Next()

  def op_dxyn(self):
    """
    Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.
    """
    x = self.get_x()
    y = self.get_y()
    n = self.get_n()

    Vx = self.V[x]
    Vy = self.V[y]

    self.V[0xf] = 0

    for i in range(n):
      y = (Vy + i) & 31
      pixel = self.memory[self.I + i]

      for j in range(8):
        if pixel & (0x80 >> j) != 0:
          x = (Vx + j) & 63
          pos = x + (y << 6)

          if self.frame_buffer[pos] == 1:
            self.V[0xf] = 1
          self.frame_buffer[pos] ^= 1
    return State.Next()

  def op_ex__(self):
    """
    Handles 0xex-- operations.
    """
    if self.get_n() == 0x0e:
      return self.op_ex9e()
    return self.op_exa1()

  def op_ex9e(self):
    """
    Skip next instruction if key with the value of Vx is pressed.
    """
    x = self.get_x()
    return State.SkipIf(self.keys_pressed[self.V[x]])

  def op_exa1(self):
    """
    Skip next instruction if key with the value of Vx is not pressed.
    """
    x = self.get_x()
    return State.SkipIf(not self.keys_pressed[self.V[x]])

  def op_fx__(self):
    """
    Handles 0xfx__ operations.
    """
    return self.operations_fx__[self.get_y()]()

  def op_fx0_(self):
    """
    Handles 0x0fx0_ operations.
    """
    if self.get_n() == 0x07:
      return self.op_fx07()
    return self.op_fx0a()

  def op_fx07(self):
    """
    Set Vx = delay timer value.
    """
    x = self.get_x()
    self.V[x] = self.delay_timer
    return State.Next()

  def op_fx0a(self):
    """
    Wait for a key press, store the value of the key in Vx.
    """
    key_pressed = self.chip8.input.get_key()

    if key_pressed == None:
      return State.Block()

    x = self.get_x()
    self.V[x] = key_pressed
    return State.Next()

  def op_fx1_(self):
    """
    Handles 0xfx1_ operations.
    """
    n = self.get_n()

    if n == 0x05:
      return self.op_fx15()
    elif n == 0x08:
      return self.op_fx18()
    return self.op_fx1e()

  def op_fx15(self):
    """
    Set delay timer = Vx.
    """
    x = self.get_x()
    self.delay_timer = self.V[x]
    return State.Next()

  def op_fx18(self):
    """
    Set sound timer = Vx.
    """
    x = self.get_x()
    self.sound_timer = self.V[x]
    return State.Next()

  def op_fx1e(self):
    """
    Set I = I + Vx. Set Vf to 1 if it overflows.
    """
    x = self.get_x()
    Vx = self.V[x]
    self.V[0xf] = 1 if self.I + Vx > 0xfff else 0
    self.I = (self.I + Vx) & 0xfff
    return State.Next()

  def op_fx29(self):
    """
    Set I = location of sprite for digit Vx.
    """
    x = self.get_x()
    self.I = (self.V[x] * 0x5) & 0xfff
    return State.Next()

  def op_fx33(self):
    """
    Store BCD representation of Vx in memory locations I, I+1, and I+2.
    """
    x = self.get_x()
    Vx = self.V[x]
    self.memory[self.I] = Vx // 100
    self.memory[self.I + 1] = (Vx // 10) % 10
    self.memory[self.I + 2] = (Vx % 100) % 10
    return State.Next()

  def op_fx55(self):
    """
    Store registers V0 through Vx in memory starting at location I.
    """
    x = self.get_x()
    for i in range(x + 1):
      self.memory[self.I + i] = self.V[i]
    return State.Next()

  def op_fx65(self):
    """
    Read registers V0 through Vx from memory starting at location I.
    """
    x = self.get_x()
    for i in range(x + 1):
      self.V[i] = self.memory[self.I + i]
    return State.Next()
