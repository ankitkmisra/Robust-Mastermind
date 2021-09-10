import mastermind
import numpy as np
import time
import importlib
print("************************************************")
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
print("Case 2: Unreliable player")
marks = 0
tot_time = 0
moves_limit = 100
def get_unreliable_response( move, chance, k ):
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
    if np.random.random() < chance and reds != k and reds!=k-1:
        reds += 1
    return reds, whites_and_reds-reds
n_list = [5,8,10,12,12]
k_list = [3,4,5,6,7]
prob = [0.1,0.1,0.1,0.1,0.1]
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
    red_actual = 0
    tot_moves = 0
    while red_actual < k and tot_moves < moves_limit:
        tot_moves += 1
        move = mastermind.get_second_player_move()
        guess_list.append(move)
        if len(guess_list) > 1 and move != guess_list[-2]:
            red, white = get_unreliable_response( move, prob[t], k )
        elif len(guess_list) == 1:
            red, white = get_unreliable_response( move, prob[t], k )
        red_actual, white_actual = get_reliable_response(move,k)
        mastermind.put_first_player_response( red, white )
    t2=time.time()
    tot_time += t2-t1
    if red_actual == k:
        marks += 3
        print("Testcase {} passed with time = {} and moves = {}".format(t+1,t2-t1,tot_moves))
    else:
        print("Testcase {} took too many moves".format(t+1))
print("Marks for correctness = {}".format(marks),"/ 15 marks")
print("Total time (5 marks) = {}".format(tot_time))
