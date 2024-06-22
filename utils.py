import random

def start_point_generate(n, m):

    if random.choice([True, False]): 
        if random.choice([True, False]):  
            start = (0, random.randint(0, m - 1))
        else:
            start = (n - 1, random.randint(0, m - 1))
    else: 
        if random.choice([True, False]):  
            start = (random.randint(0, n - 1), 0)
        else:
            start = (random.randint(0, n - 1), m - 1)
    return start

def finish_point_generate(start, n, m):
    return n - 1 - start[0], m - 1 - start[1]

def transition_choice(x, y, rm):
    choice_list = []
    if x > 0 and not rm[x - 1][y]:
        choice_list.append((x - 1, y))
    if x < len(rm) - 1 and not rm[x + 1][y]: 
        choice_list.append((x + 1, y))
    if y > 0 and not rm[x][y - 1]:  
        choice_list.append((x, y - 1))
    if y < len(rm[0]) - 1 and not rm[x][y + 1]: 
        choice_list.append((x, y + 1))

    if choice_list:
        nx, ny = random.choice(choice_list)
        if x == nx: 
            tx, ty = x * 2, ny * 2 - 1 if ny > y else ny * 2 + 1
        else:  
            tx, ty = nx * 2 - 1 if nx > x else nx * 2 + 1, y * 2
        return nx, ny, tx, ty
    else:
        return -1, -1, -1, -1
    
