import mastermind
import importlib
import numpy as np
import time
print("*******************Mastermind*******************")
print("Case 1: Reliable player")
marks = 0
tot_time = 0
moves_limit = 50
def get_reliable_response( move,k ):
    assert( len(move) == k )
    reds = 0
    for i in range(k):
        if move[i] == code[i]:
            reds += 1
    matched_idxs = []
    whites_and_reds = 0
    for i in range(k):
        c = move[i]
        for j in range(k):
            if j in matched_idxs:
                continue
            if c == code[j]:
                whites_and_reds += 1
                matched_idxs.append(j)
                break
    return reds, whites_and_reds-reds
n_list = [5,8,10,12,12]
k_list = [3,4,5,6,7]
for t in range(len(n_list)):
    np.random.seed(t)
    n = n_list[t]
    k = k_list[t]
    code = []
    importlib.reload(mastermind)
    for i in range(k):
        code.append( np.random.randint(0, n))
    t1 = time.time()
    mastermind.initialize(n,k)
    guess_list = []
    red = 0
    tot_moves = 0
    while red < k and tot_moves < moves_limit:
        tot_moves += 1
        move = mastermind.get_second_player_move()
        guess_list.append(move)
        red, white = get_reliable_response( move,k )
        mastermind.put_first_player_response( red, white )
    t2=time.time()
    tot_time += t2-t1
    if red == k:
        marks += 5
        print("Testcase {} passed with time = {} and moves = {}".format(t+1,t2-t1,tot_moves))
    else:
        print("Testcase {} took too many moves".format(t+1))
print("Marks for correctness = {}".format(marks),"/ 25 marks")
print("Total time (5 marks) = {}".format(tot_time))
