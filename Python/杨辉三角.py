# -*- coding: utf-8 -*-
def triangles()
    l1=[1]
    yield(l1)
    l2=[1,1]
    yield(l2)
    while True:
        L=[1]
        for x in range(0,len(l2)-1):
           L.append(l2[x]+l2[x+1])
        L.append(1)
        l2=L
        yield(l2)


n = 0
for t in triangles():
    print(t)
    n = n + 1
    if n == 10:
        break