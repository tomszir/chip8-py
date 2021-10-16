import os


class ROM:
  def __init__(self, path: str, data: list[int]):
    self.name = os.path.basename(path)
    self.data = data

  @staticmethod
  def load_from_file(path: str):
    # Open file as bytes
    try:
      file = open(path, "rb")
    except:
      return print("ROM file could not be found.")

    # Read first 0xFFF (4096) bytes from file
    try:
      file_buffer = file.read(0xfff)
    except:
      return print("ROM data couuld not be read.")

    data = [file_buffer[i] for i in range(len(file_buffer))]

    return ROM(path, data)
