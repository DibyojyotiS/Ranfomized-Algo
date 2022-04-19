from itertools import permutations

s = set()
for x in permutations([*range(8)]):
    l = [frozenset(x[i*3:i*3+3]) for i in range(2)]
    f = frozenset(l)
    if f in s: pass
    else:
        s.add(f)
        print(f)
print(len(s))

s = set()
for x in permutations([*range(9)]):
    l = [frozenset(x[max(0,i*3 -1):max(3,i*3+3-1)]) for i in range(2)]
    f = frozenset(l)
    if f in s: pass
    else:
        s.add(f)
        print(f)
print(len(s))

x= 5; l=100
sum([l-i for i in range(x,l)]) 