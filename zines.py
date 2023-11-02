import math
import matplotlib.pylab as plt


def to_tikz(path, include_borders=True):
    n = max(i[0] for i in path) + 1
    m = max(i[1] for i in path) + 1

    out = "\\begin{tikzpicture}["
    if n > m:
        out += f"x={8 * math.sqrt(2)/n}cm,y={8/m}cm"
    else:
        out += f"x={8/n}cm,y={8 * math.sqrt(2)/m}cm"
    out += ",line width=1pt,line cap=round,line join=round]\n"
    if include_borders:
        out += f"\\draw (0,0) rectangle ({n},{m});\n"
        out += "\\draw[dashed,gray]"
        for i in range(1, n):
            out += f" ({i},0) -- ({i},{m})"
        for i in range(1, m):
            out += f" (0,{i}) -- ({n},{i})"
        out += ";\n"
    out += "\\draw[red]"
    for i, j in path:
        out += f" ({i}.5,{j}.5) --"
    out += " cycle;"

    out += "\\end{tikzpicture}"
    return out


def plot(path):
    plt.plot([i[0] for i in path], [i[1] for i in path], "r-")
    plt.show()


def connected_empty(n, m, path):
    if max(i[0] for i in path) < n-1 and max(i[1] for i in path) < m-1:
        return True
    empty = [(i, j) for i in range(n) for j in range(m) if (i,j) not in path]
    c = []
    l = -1
    while l != len(c):
        l = len(c)
        c += [i for i in empty if i not in c and ((i[0]+1, i[1]) in c or (i[0]-1, i[1]) in c or (i[0], i[1]+1) in c or (i[0], i[1]-1) in c)]
    return True


def diff1(a, b):
    if a[0] == b[0] and abs(a[1] - b[1]) == 1:
        return True
    if a[1] == b[1] and abs(a[0] - b[0]) == 1:
        return True
    return False


def find(n, m, done=None):
    if done is None:
        done = [(0,1), (0,0), (1,0)]
    if len(done) == n * m + 1:
        if done[-1] == done[0] and is_max(done):
            return [done]
        else:
            return []
    if (done[-1][0] == n - 1 or done[-1][1] == m - 1) and not connected_empty(n, m, done):
        return []
    if (1, 1) in done and (0, 2) in done:
        return []
    if done[0] in done[1:]:
        return []
    d = done[-1]
    out = []
    for n1 in [
        (d[0] + 1, d[1]),
        (d[0] - 1, d[1]),
        (d[0], d[1] - 1),
        (d[0], d[1] + 1),
    ]:
        if 0 <= n1[0] < n and 0 <= n1[1] < m and n1 not in done:
            for n2 in [
                (n1[0] - 1, n1[1]),
                (n1[0] + 1, n1[1]),
            ]:
                if 0 <= n2[0] < n and 0 <= n2[1] < m and n2 not in done[1:]:
                    out += find(n, m, done + [n1, n2])
    return out


def permutations(r):
    n = max(i[0] for i in r)
    m = max(i[1] for i in r)
    out = []
    for f in [
        lambda i, j: (i, j),
        lambda i, j: (i, m - j),
        lambda i, j: (n - i, j),
        lambda i, j: (n - i, m - j),
    ]:
        r2 = [f(*i) for i in r[:-1]]
        i = r2.index((0, 1))
        r2 = r2[i:] + r2[:i]
        if r2[1] != (0,0):
            r2 = [r2[0]] + r2[:0:-1]
        out.append(r2 + [r2[0]])
    return out


def is_max(r):
    for i in permutations(r):
        if i > r:
            return False
    return True
