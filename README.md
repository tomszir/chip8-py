# chip8-py

A Chip8 interpreter created in Python.

> CHIP-8 is an interpreted programming language, developed by Joseph Weisbecker. It was initially used on the COSMAC VIP and Telmac 1800 8-bit microcomputers in the mid-1970s.


## Table of Contents

- [Motivation](#motivation)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [ROMs](#roms)
- [Keyboard Layout](#keyboard-layout)
- [Reference](#reference)
- [License](#license)

## Motivation

The main motivation for this project was to learn the basics of emulation and lower-level programming concepts.

## Screenshots

> roms/TETRIS

![TETRIS.gif](/.assets/tetris.gif?raw=true)

> roms/PONG

![PONG.gif](/.assets/pong.gif?raw=true)


## Installation
> Assumes you already have [Python 3.9.5](https://www.python.org/downloads/)

```bash
git clone https://github.com/tomszir/chip8-py.git
cd chip8-py
pip install -r reqs.txt
```

## Usage

```bash
py main.py --rom roms/PONG
```

## ROMs

> A pack of simple yet amusing games, in the public domain, for any Chip-8 Interpreter. They are: 15 Puzzle, Blinky, Blitz, Brix, Connect 4, Guess, Hidden, Invaders, Kaleid, Maze, Merun, Missle, Pong, Pong 2, Puzzle, Syzgy, Tank, Tetris, TicTac, UFO, Vbrix and Wipeoff.

All roms were taken from [Chip-8 Public Domain ROMs](https://www.zophar.net/pdroms/chip8.html)

## Keyboard Layout

|              |              |              |              |
| ------------ | ------------ | ------------ | ------------ |
| <kbd>1</kbd> | <kbd>2</kbd> | <kbd>3</kbd> | <kbd>4</kbd> |
| <kbd>Q</kbd> | <kbd>W</kbd> | <kbd>E</kbd> | <kbd>R</kbd> |
| <kbd>A</kbd> | <kbd>S</kbd> | <kbd>D</kbd> | <kbd>F</kbd> |
| <kbd>Z</kbd> | <kbd>X</kbd> | <kbd>C</kbd> | <kbd>V</kbd> |

- <kbd>F1</kbd> - Change the color scheme
- <kbd>F2</kbd> - Reload the current ROM

## Reference

- [Chip8 Wikipedia](https://en.wikipedia.org/wiki/CHIP-8)
- [Cowgod's Chip-8 Technical Reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM), made by Thomas P. Greene
- [Guide to making a CHIP-8 emulator](https://tobiasvl.github.io/blog/write-a-chip-8-emulator/), made by Tobias V. Langhoff

## License

This project is under the [MIT](https://choosealicense.com/licenses/mit/) license
