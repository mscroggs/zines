from zines import find

with open("diagrams.tex", "w") as f:
    for dims in [(2, 2), (4, 2), (4, 4), (8, 4), (8, 8), (16, 8)]:
        res = find(*dims)
        print(dims[0] * dims[1], len(res))
