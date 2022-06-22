# coding: utf-8
# Your code here!

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    st = sum(a)
    tree = [st]
    for i in range(n):
        next_gen = []
        for i, k in enumerate(tree):
            if k in a:
                del a[a.index(k)]
            else:
                next_gen.append(round(k / 2 - 0.25))
                next_gen.append(round(k / 2 + 0.25))
        tree = next_gen.copy()
        if next_gen == [] and a==[]:
            print("yes")
            break
        if len(next_gen) > n or (next_gen == [] and a!=[]):
            print("no")
            break
