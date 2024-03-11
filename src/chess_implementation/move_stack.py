import numpy as np
from numba import jit 


class MoveStack:

  def __init__(self):
    self.stack = np.empty(1000,dtype=int)
    self.head = 0

  def show(self):
    for ind in range(self.head):
      print("(",self.stack[ind*5],",",self.stack[ind*5+1],")", "->","(",self.stack[ind*5+2],",",self.stack[ind*5+3],") ",self.stack[ind*5+4],"\n" )