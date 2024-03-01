import numpy as np

class MoveStack:

  def __init__(self):
    self.stack = np.empty(1000,dtype=int)
    self.head = 0