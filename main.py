import time
import random
import pygame as pg
import numpy as np

from src.chip8 import Chip8

pg.init()


def main():
  # Seed the random number generator
  random.seed(time.time() * 1000)

  # Initialize the interpreter
  chip8 = Chip8("roms/INVADERS")

  # Run the interpreter
  chip8.run()


if __name__ == "__main__":
  main()
