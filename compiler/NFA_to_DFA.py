# let a n*n martix represent a NFA with n states
# -1--epsilon, 0--a, 1--b, 3--no path

# nfa = [
#     [-1,-1,3,3,3,3,3,-1,3],
#     [3,-1,-1,3,-1,3,3,3,3],
#     [3,3,-1,0,3,3,3,3,3],
#     [3,3,3,-1,3,3,-1,3,3],
#     [3,3,3,3,-1,1,3,3,3],
#     [3,3,3,3,3,-1,-1,3,3],
#     [3,-1,3,3,3,3,-1,-1,3],
#     [3,3,3,3,3,3,3,-1,1],
#     [3,3,3,3,3,3,3,3,-1]
# ]

# nfa = [
#     [-1,-1,3,-1,3,3,3,3,3,3,3,3,3,3,3,3],
#     [3,-1,0,3,3,3,3,3,3,3,3,3,3,3,3,3],
#     [3,-1,-1,-1,3,3,3,3,3,3,3,3,3,3,3,3],
#     [3,3,3,-1,1,3,3,3,3,3,3,3,3,3,3,3],
#     [3,3,3,3,-1,-1,3,-1,3,3,3,3,3,3,3,3],
#     [3,3,3,3,3,-1,0,3,3,3,3,3,3,3,3,3],
#     [3,3,3,3,3,-1,-1,-1,3,3,3,3,3,3,3,3],
#     [3,3,3,3,3,3,3,-1,1,3,3,3,3,3,3,3],
#     [3,3,3,3,3,3,3,3,-1,-1,3,-1,3,3,3,3],
#     [3,3,3,3,3,3,3,3,3,-1,0,3,3,3,3,3],
#     [3,3,3,3,3,3,3,3,3,-1,-1,-1,3,3,3,3],
#     [3,3,3,3,3,3,3,3,3,3,3,-1,1,3,3,3],
#     [3,3,3,3,3,3,3,3,3,3,3,3,-1,-1,3,-1],
#     [3,3,3,3,3,3,3,3,3,3,3,3,3,-1,0,3],
#     [3,3,3,3,3,3,3,3,3,3,3,3,3,-1,-1,-1],
#     [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,-1]      
# ]

nfa = [    
    [-1, -1, 3, 3, 3, 3, 3, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],# 0
    [3, -1, -1, 3, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],# 1
    [3, 3, -1, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],# 2
    [3, 3, 3, -1, 3, 3, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],# 3
    [3, 3, 3, 3, -1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],# 4
    [3, 3, 3, 3, 3, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],# 5
    [3, -1, 3, 3, 3, 3, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],# 6
    [3, 3, 3, 3, 3, 3, 3, -1, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],# 7
    [3, 3, 3, 3, 3, 3, 3, 3, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],# 8
    [3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, 3, -1, 3, 3, 3, 3, 3, 3, 3, 3],# 9
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3],# 10
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, 3, 3, -1, 3, 3, 3, 3, 3, 3],# 11
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, 1, 3, 3, 3, 3, 3, 3, 3],# 12
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, 3, 3, 3, 3, 3, 3],# 13
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, 3, 3, 3, 3, 3],# 14
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, 3, -1, 3, 3],# 15
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, 0, 3, 3, 3],# 16
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, 3, 3, -1],# 17
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, 1, 3],# 18
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1],# 19
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1],# 20
]

# input a set
def closure(state_set):
    if len(state_set) <= 0:
        return {}
    
    nfa_stack = []
    for i in state_set:
        nfa_stack.append(i)
        
    while len(nfa_stack) > 0:
        state = nfa_stack.pop()
        for i in range(len(nfa[state])):
            if nfa[state][i] == -1:
                if i not in state_set:
                    state_set.add(i)
                    nfa_stack.append(i)
                    
    return state_set

# input a set
def move(from_set, lable):
    to_set = set()
    for i in from_set:
        for j in range(len(nfa[i])):
            if nfa[i][j] == lable:
                to_set.add(j)

    return to_set

class DFA:
    def __init__(self):
        # dfa states
        self.state_list = [0]
        # 0-unmarked, 1-marked
        self.record_state = [0]
        # what nfa states it contains
        self.contain_nfa_states = [{0},]
        # dfa transition function
        self.tran = [[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]
    
    # state_from is a string, state_to is a set    
    def add_state(self, state_from, state_to, lable):
        if len(state_to) > 0:
            rec = 0
            already_state = -1
            for states in self.contain_nfa_states:
                if state_to == states:
                    rec = 1
                    already_state = self.contain_nfa_states.index(states)
                    break
            if rec == 0:
                self.contain_nfa_states.append(state_to)
                self.state_list.append(self.contain_nfa_states.index(state_to))
                self.tran[state_from][lable] = self.contain_nfa_states.index(state_to)
                self.record_state.append(0)
            else:
                self.tran[state_from][lable] = already_state
    
    def main(self):
        closure0 = closure(self.contain_nfa_states[0])
        self.contain_nfa_states[0] = closure0
        for state in self.state_list:
            print(f"{state}:{self.contain_nfa_states[state]}")
            if self.record_state[state] == 0:
                self.record_state[state] = 1
                for lable in range(2):
                    move_set = move(self.contain_nfa_states[state], lable)
                    new_state = closure(move_set)
                    print(f"Dtran[{state},{lable}]={new_state}")
                    self.add_state(state, new_state, lable)
        
        return self.tran

if __name__ == "__main__":
    
    test = DFA()
    ans = test.main()
    for row in ans:
        count = 0
        for element in row:
            print(element, end=" ")
            if element == -1:
                count += 1
        print()
        if count == len(row):
            break
        
    