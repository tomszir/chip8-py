# chip8-py

A Chip8 interpreter created in Python.

> CHIP-8 is an interpreted programming language, developed by Joseph Weisbecker. It was initially used on the COSMAC VIP and Telmac 1800 8-bit microcomputers in the mid-1970s.

## Motivation

The main motivation for this project was to learn the basics of emulation and lower-level programming concepts.

## Screenshots

![TETRIS.gif](/.assets/tetris.gif?raw=true)
![PONG.gif](/.assets/pong.gif?raw=true)

## Running

> Tested and made with [Python 3.9.5](https://www.python.org/downloads/)

```bash
# Install required packages
pip install -r reqs.txt

# Run the interpreter
py main.py --rom roms/PONG
```

## Keyboard Layout

|              |              |              |              |
| ------------ | ------------ | ------------ | ------------ |
| <kbd>1</kbd> | <kbd>2</kbd> | <kbd>3</kbd> | <kbd>4</kbd> |
| <kbd>Q</kbd> | <kbd>W</kbd> | <kbd>E</kbd> | <kbd>R</kbd> |
| <kbd>A</kbd> | <kbd>S</kbd> | <kbd>D</kbd> | <kbd>F</kbd> |
| <kbd>Z</kbd> | <kbd>X</kbd> | <kbd>C</kbd> | <kbd>V</kbd> |

- <kbd>F1</kbd> - Change the color scheme
- <kbd>F2</kbd> - Reload the current ROM

## Reference & Sources

- [Chip8 Wikipedia](https://en.wikipedia.org/wiki/CHIP-8)
- [Cowgod's Chip-8 Technical Reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM), made by Thomas P. Greene
- [Guide to making a CHIP-8 emulator](https://tobiasvl.github.io/blog/write-a-chip-8-emulator/), made by Tobias V. Langhoff

## License

This project is under the [MIT](https://choosealicense.com/licenses/mit/) license
