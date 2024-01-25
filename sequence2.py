import matplotlib.pylab as plt
from time import time

maps = [
    lambda x, y, w, h: (x, y),
    lambda x, y, w, h: (w-1-x, y),
    lambda x, y, w, h: (w-1-x, h-1-y),
    lambda x, y, w, h: (x, h-1-y),
]

def ismax(a, w, h):
    return a == max(
        sorted([tuple(sorted((map(*v, w, h) for v in vs))) for vs in a])
        for map in maps)

def finished(n, m, vertices, edges):
    w = n//2 - 1
    h = m//2
    for i in range(0, w, 2):
        for j in range(0, h):
            if (i, j) not in vertices:
                return False
    for i in range(1, w, 2):
        for j in range(0, h):
            if (i, j) not in vertices and ((i-1, j) not in vertices or (i+1, j) not in vertices):
                pass # return False
    return True


def find_all(n, m, vertices=None, edges=None, allowed_edges=None):
    w = n // 2 - 1
    h = m // 2

    if vertices is None:
        vertices = [(0,0)] if max(h, w) > 0 else []
        edges = []
        allowed_edges = []
        if w > 1:
            allowed_edges.append(((0, 0), (1, 0)))
        if h > 1:
            allowed_edges.append(((0, 0), (0, 1)))

    if finished(n, m, vertices, edges):
        if ismax(edges, w, h):
            return [edges]
        else:
            return []

    v = vertices[-1]

    if v[0] % 2 == 1:
        found = False
        for v2 in [
            (v[0] + 1, v[1]),
            (v[0] - 1, v[1]),
        ]:
            e = (min(v, v2), max(v, v2))
            if e not in edges:
                found = True
                if v2 in vertices:
                    return []
                vertices.append(v2)
                edges.append(e)
                allowed_edges += [(min(v2, v3), max(v2, v3)) for v3 in [
                    (v2[0] + 1, v2[1]), (v2[0], v2[1] + 1),
                    (v2[0] - 1, v2[1]), (v2[0], v2[1] - 1)
                ] if 0 <= v3[0] < w and 0 <= v3[1] < h and v3 not in vertices]
        if found:
            return find_all(n, m, vertices, sorted(edges), allowed_edges)

    out = []
    while len(allowed_edges) > 0:
        edge = allowed_edges[0]
        allowed_edges = allowed_edges[1:]
        assert edge[0] != edge[1]
        if edge[0] not in vertices or not edge[1] in vertices:
            if edge[0][0] == edge[1][0]:
                if tuple((a - 1, b) for a, b in edge) in edges:
                    continue
                if tuple((a + 1, b) for a, b in edge) in edges:
                    continue
            v = [v for v in edge if v not in vertices][0]
            out += find_all(n, m, vertices + [v],
                            sorted(edges + [edge]), allowed_edges + [
                                (min(v, v2), max(v, v2)) for v2 in [
                                    (v[0] + 1, v[1]), (v[0], v[1] + 1),
                                    (v[0] - 1, v[1]), (v[0], v[1] - 1)
                                ] if 0 <= v2[0] < w and 0 <= v2[1] < h and v2 not in vertices])
    return out


def find(n, m, remove_symmetric=True):
    return find_all(n, m)


def plot(a):
    plt.plot([0, w, w, 0, 0], [0, 0, h, h, 0], "r-")
    for x in range(1, w):
        plt.plot([x, x], [0, h], "r--")
    for y in range(1, h):
        plt.plot([0, w], [y, y], "r--")
    for e in a:
        plt.plot([2 + 2*e[0][0], 2 + 2*e[1][0]], [1 + 2*e[0][1], 1 + 2*e[1][1]], "ko-")
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
    print(w, h, len(f), n)
    assert len(f) == n

with open("b367038.txt", "w") as f:
    pass
for i, dims in enumerate([(2, 2), (4, 2), (4, 4), (8, 4), (8, 8), (16, 8)]):
    assert dims[0] * dims[1] == 2 ** (i + 2)
    start = time()
    term = len(find(*dims))
    print(i + 2, term, f"(computed in {time() - start}s)")
    with open("b367038.txt", "a") as f:
        f.write(f"{i+2} {term}\n")
