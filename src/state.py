from enum import Enum


class StateType(Enum):
  NEXT = 0
  SKIP = 1
  JUMP = 2
  BLOCK = 3
  NOT_IMPLEMENTED = 4


class State:
  @staticmethod
  def Next():
    return (StateType.NEXT, 2)

  @staticmethod
  def Skip():
    return (StateType.SKIP, 4)

  @staticmethod
  def SkipIf(condition: bool):
    if condition:
      return State.Skip()
    return State.Next()

  @staticmethod
  def Jump(addr: int):
    return (StateType.JUMP, addr)

  @staticmethod
  def Block():
    return (StateType.BLOCK, 0)

  @staticmethod
  def NotImplemented():
    return (StateType.NOT_IMPLEMENTED, -1)
