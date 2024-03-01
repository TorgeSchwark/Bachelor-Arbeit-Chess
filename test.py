import numpy as np
from move_stack import MoveStack

stack = MoveStack()

def test(num: MoveStack):
  num.head += 5
  #print(num)

test(stack)

print(stack.head)