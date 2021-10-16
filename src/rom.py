from .font import Font


class ROM:
  def __init__(self, name: str, data: list[int], font: Font = Font.Default()):
    self.name = name
    self.data = data
    self.font = font

    # Load font into memory
    for i in range(0x200):
      self.data[i] = self.font.data[i]

  @staticmethod
  def load_from_file(path: str, font: Font = Font.Default()):
    # Open file as bytes
    try:
      file = open(path, "rb")
    except:
      return print("ROM file could not be found.")

    # Read first 0xFFF (4096) bytes from file
    try:
      file_data = file.read(0xfff)
    except:
      return print("ROM data couuld not be read.")

    rom_data = [0] * 0xfff

    # Load ROM file data into ROM memory
    for i in range(len(file_data)):
      rom_data[i + 0x200] = file_data[i]

    return ROM(path, rom_data, font)
