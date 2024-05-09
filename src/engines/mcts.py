import ctypes
import struct
from chess_implementationC.chess_board_wrapper import ChessBoard, chess_lib
import random
from math import log, sqrt, e, inf
import time


# a basic very slow implementation of the MCTS only usefull to understand how MCTS works 
class node():
    def __init__(self):
        self.state = ChessBoard()
        self.child = set()
        self.parent = None
        self.N = 0 #N- Number of times parent node has been visited
        self.n = 0 #n-Number of times current node has been visited
        self.v = 0 #v-Exploitation factor of current node

def ucb1(curr_node):
    ans = curr_node.v+2*(sqrt(log(curr_node.N+e+(10**-6))/(curr_node.n+(10**-10))))
    return ans


def monte_carlo_tree_search(board):

    moves = (ctypes.c_byte * 2024)()
    move_count = ctypes.c_short(0)
    chess_lib.find_all_moves(ctypes.byref(board), moves, ctypes.byref(move_count))
    
    sm = 0
    root = node()
    root.state = board
    matt = ctypes.c_float(0)
    chess_lib.printChessBoard(ctypes.byref(board))
    chess_lib.is_check_mate(ctypes.byref(board), ctypes.byref(matt))
    result = mcts_pred(root, matt.value != 0, 1)
    return result

def rollout(curr_node):
    matt = ctypes.c_float(0)
    chess_lib.is_check_mate(ctypes.byref(curr_node.state), ctypes.byref(matt))

    if matt.value != 0:
        if curr_node.state.color_to_move == 1:
            return (-matt.value, curr_node)
        else:
            return (matt.value, curr_node)
    moves = (ctypes.c_byte * 2024)()
    move_count = ctypes.c_short(0)
    chess_lib.find_all_moves(ctypes.byref(curr_node.state), moves, ctypes.byref(move_count))

    for i in range(move_count.value//5):

        tmp_state = ChessBoard()
        chess_lib.copyBoard(ctypes.byref(curr_node.state), ctypes.byref(tmp_state))
        chess_lib.make_move( ctypes.byref(tmp_state), moves[i*5], moves[i*5+1], moves[i*5+2], moves[i*5+3], moves[i*5+4])
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.child.add(child)

    rnd_state = random.choice(list(curr_node.child))
    return rollout(rnd_state)

def expand(curr_node, white):
    if len(curr_node.child) == 0:
        return curr_node
    if white:
        max_ucb = -inf
        sel_child = None
        for i in curr_node.child:
            tmp = ucb1(i)
            if tmp > max_ucb:
                max_ucb = tmp 
                sel_child = i 
        return expand(sel_child,0)
    else:
        min_ucb = inf 
        sel_child = None
        for i in curr_node.child:
            tmp = ucb1(i)
            if tmp < min_ucb:
                min_ucb = tmp
                sel_child = i 
        return expand(sel_child, 1)

def rollback(curr_node, reward):
    curr_node.n += 1
    curr_node.v += reward
    while curr_node.parent != None:
        curr_node.N += 1
        curr_node = curr_node.parent
    return curr_node

def mcts_pred(curr_node, over, white, iterations=500):
    if over:
        return -1
    
    moves = (ctypes.c_byte * 2024)()
    move_count = ctypes.c_short(0)
    chess_lib.find_all_moves(ctypes.byref(curr_node.state), moves, ctypes.byref(move_count))
    map_state_move = dict()

    for i in range(move_count.value//5):
        tmp_state = ChessBoard()
        chess_lib.copyBoard(ctypes.byref(curr_node.state), ctypes.byref(tmp_state))
        chess_lib.make_move( ctypes.byref(tmp_state), moves[i*5], moves[i*5+1], moves[i*5+2], moves[i*5+3], moves[i*5+4])
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.child.add(child)
        map_state_move[child] = i*5  

    while iterations > 0:
        start = time.time()
        if white:
            max_ucb = -inf
            sel_child = None
            for i in curr_node.child:
                tmp = ucb1(i)
                if tmp > max_ucb:
                    max_ucb = tmp
                    sel_child = i
            ex_child = expand(sel_child, 0)
            reward, state = rollout(ex_child)
            curr_node = rollback(state, reward)
            iterations -= 1
        else:
            min_ucb = inf
            sel_child = None
            for i in curr_node.child:
                tmp = ucb1(i)
                if tmp < min_ucb:
                    min_ucb = tmp
                    sel_child = i 
            ex_child = expand(sel_child, 1)
            reward, state = rollout(ex_child)
            curr_node = rollback(state, reward)
            iterations -=1
        end = time.time()

    if white:
        mx = -inf 
        selected_move = ''
        for i in curr_node.child:
            tmp = ucb1(i)
            if tmp > mx:
                mx = tmp
                selected_move = map_state_move[i]
        return selected_move
    else:
        mn = inf 
        selected_move = ''
        for i in curr_node.child:
            tmp = ucb1(i)
            if tmp < mn:
                mn = tmp
                selected_move = map_state_move[i]
        return selected_move

        




        
