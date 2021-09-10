from z3 import *
 
import sys
import itertools
import random

n=0 # COLORS
k=0 # SIZE_SEQ
MOVE=[]

vs = [] # Variables
base_conditions = [] # Only one colour should be activated per sequence slot
obtained_conditions = []


def initialize(COLORS,SIZE_SEQ):
    global n,k,base_cons,vs,klist,nlist
    n=COLORS
    k=SIZE_SEQ

    vs = [[Bool ("e_{}_{}".format(i,j))  for j in range(n)] for i in range(k)]
    for i in range(k):
        base_conditions.append(sum_is_one(vs[i]))

def sum_is_one(ls):
    # Using the implementation shown in tutorial
    # Each slot should have one and only one colour
    cond = PbEq([(ls[i],1) for i in range(len(ls))], 1)
    return cond

def red_cond(ls, red):
    # Exactly 'red' number of colours are in correct positions!
    # That is 'red' number of these 'vs[i][ls[i]]' should be correct
    cond = PbEq([(vs[i][ls[i]],1) for i in range(k)], red)
    return cond

def white_cond(ls, white):
    # Atleast 'white' number of colours in the sequence 
    # will be correct at some different location
    l = []
    for i in range(len(ls)):
        some_diff_loc = False
        for j in range(k):
            # Encodes "at some different" location
            some_diff_loc = Or(some_diff_loc, vs[j][ls[i]])
        l.append(some_diff_loc)

    # Encodes "atleast"
    cond = PbGe([(l[i],1) for i in range(len(l))], white)
    return cond

def get_second_player_move():
    global MOVE,k,n,obtained_conditions,base_conditions
    if MOVE is None:
        return MOVE
    
    MOVE = random.sample(range(0, n), k)
    # if s.check() == sat:
    #     model = s.model()
    #     for i in range(k):
    #         for j in range(n):
    #             getany = model[vs[i][j]]
    #             if is_true(getany):
    #                 MOVE[i] = j
    #     # print("Next Step Selected: ",MOVE)
    #     return MOVE
    # else:
    #     # We need to backtrack here
    #     print("NO POSSIBLE MOVES FOUND ! Solver Resetting !")
    #     s = Solver()
    #     s.add(And(base_conditions))
    #     return MOVE

    if len(obtained_conditions) == 0:
        return MOVE

    s = Optimize()
    s.add(base_conditions)
    s.maximize(sum(obtained_conditions))
    s.check()
    # print(len(obtained_conditions))
    model = s.model()
    # print(model)
    # print(klist)
    # print(nlist)
    for i in range(k):
        for j in range(n):
            getany = model[vs[i][j]]
            if is_true(getany):
                MOVE[i] = j
                break
    return MOVE


def put_first_player_response(red,white):
    global obtained_conditions,MOVE, k
    # Get the conditions and add to the 
    # existing set of constraints
    cons = red_cond(MOVE,red)    
    guess_cons = white_cond(MOVE,white)
    # s.add(And(guess_cons,cons))
    obtained_conditions.append(IntSort().cast(cons))
    obtained_conditions.append(IntSort().cast(guess_cons))
    obtained_conditions.append(IntSort().cast(Or([Not(vs[i][MOVE[i]]) for i in range(k)])))