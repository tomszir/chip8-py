import time
import random
import pygame as pg
import argparse

from src.chip8 import Chip8

pg.init()


def main():
  parser = argparse.ArgumentParser(description='A Chip8 interpreter.')
  parser.add_argument('--rom', help='Path to Chip8 ROM', default="roms/PONG")

  args = parser.parse_args()

  # Seed the random number generator
  random.seed(time.time() * 1000)

  # Initialize the interpreter
  chip8 = Chip8(args.rom)

  # Run the interpreter
  chip8.run()


if __name__ == "__main__":
  main()
