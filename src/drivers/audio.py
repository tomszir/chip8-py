import winsound

from ..processor import Processor


class AudioDriver:
  def __init__(self):
    pass

  def process_audio(self, processor: Processor):
    if processor.sound_timer > 0:
      winsound.Beep(2500, 10)
