import matplotlib.pylab as plt
import zines
from time import time

maps = [
    lambda x, y, w, h: (x, y),
    lambda x, y, w, h: (w-1-x, y),
    lambda x, y, w, h: (w-1-x, h-1-y),
    lambda x, y, w, h: (x, h-1-y),
]


def isvalid(a, w, h):
    vertex = (1, 0)
    n = 0
    while True:
        for e in a:
            if vertex in e:
                vertex = [v for v in e if v != vertex][0]
                n += 1
                break
        else:
            return True
        if vertex == (0, 0):
            break
        if vertex[0] % 2 == 0:
            vertex = (vertex[0] + 1, vertex[1])
        else:
            vertex = (vertex[0] - 1, vertex[1])

    return n == len(a)


def ismax(a, w, h):
    return a == max(
        sorted([tuple(sorted((map(*v, w, h) for v in vs))) for vs in a])
        for map in maps)


total = 0


def find_all(n, m, edges=None, remaining_vertices=None, next=None):
    global total
    if remaining_vertices is None:
        remaining_vertices = [(i, j) for i in range(n) for j in range(m)]
        edges = []
        next = (0, 0)

    if not isvalid(edges, n, m):
        return 0

    if len(remaining_vertices) == 0:
        if ismax(edges, n, m):
            total += 1
            print(total)
            return 1
        else:
            return 0

    if next not in remaining_vertices:
        return 0
    remaining_vertices.remove(next)

    if next[0] % 2 == 0:
        allowed = [
            (next[0] - 1, next[1]),
            (next[0], next[1] + 1),
            (next[0], next[1] - 1),
        ]
    else:
        allowed = [
            (next[0] + 1, next[1]),
            (next[0], next[1] + 1),
            (next[0], next[1] - 1),
        ]

    if next[0] in [0, n - 1]:
        above = (next[0], next[1] + 1)
        below = (next[0], next[1] - 1)
        if below in remaining_vertices and above in remaining_vertices:
            return 0

    if next[1] in [0, m - 1]:
        left = (next[0] - 1, next[1])
        right = (next[0] + 1, next[1])
        if left in remaining_vertices and right in remaining_vertices:
            return 0

    if next == (n - 1, m - 1):
        if len([p for p in remaining_vertices if p == n - 1]) > 0 and len([p for p in remaining_vertices if p == 0]) > 0:
            return 0

    out = 0
    for v2 in allowed:
        if v2 in remaining_vertices:
            if v2[0] % 2 == 0:
                nx = (v2[0] + 1, v2[1])
            else:
                nx = (v2[0] - 1, v2[1])
            e = (min(next, v2), max(next, v2))
            out += find_all(n, m, sorted(edges + [e]), [i for i in remaining_vertices if i != v2], nx)
    return out


def find(n, m):
    global total
    total = 0
    return find_all(n, m)


def plot(w, h, a):
    plt.plot([0, w, w, 0, 0], [0, 0, h, h, 0], "r-")
    for x in range(1, w):
        plt.plot([x, x], [0, h], "r--")
    for y in range(1, h):
        plt.plot([0, w], [y, y], "r--")
    for i in range(0, w, 2):
        for j in range(h):
            plt.plot([i+0.5, i+1.5], [j+0.5, j+0.5], "k-")
    for e in a:
        plt.plot([e[0][0]+0.5, e[1][0]+0.5], [e[0][1]+0.5, e[1][1]+0.5], "ko-")
    plt.show()
    plt.clf()


for w, h, n in [
    (2, 2, 1),
    (4, 2, 1),
    (4, 4, 1),
    (8, 4, 3),
    (8, 8, 31),
]:
    f = find(w, h)
    print(w, h, f, n)
    assert f == n
    assert len(zines.find(w, h)) == n

with open("b367038.txt", "w") as f:
    pass
for i, dims in enumerate([(2, 2), (4, 2), (4, 4), (8, 4), (8, 8), (16, 8)]):
    assert dims[0] * dims[1] == 2 ** (i + 2)
    start = time()
    term = find(*dims)
    print(i + 2, term, f"(computed in {time() - start}s)")
    with open("b367038.txt", "a") as f:
        f.write(f"{i+2} {term}\n")
