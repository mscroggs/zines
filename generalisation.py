import math
import matplotlib.pylab as plt
from zines import to_tikz, find, valid, diff1, plot

with open("diagrams2.tex", "w") as f:
    for p in range(2, 7):
        for dims in [(2**p, 2**(p-1)), (2**p, 2**p)]:
            print(dims)
            path = [(i, 0) for i in range(dims[0])]
            for i in range(dims[0]-1,0,-4):
                for j in range(0, dims[1]-2, 2):
                    path += [(i, j+1), (i-1, j+1), (i-1, j+2), (i,j+2)]
                path += [(i, dims[1]-1), (i-1, dims[1]-1), (i-2, dims[1]-1), (i-3, dims[1]-1)]
                for j in range(dims[1]-1, 2, -2):
                    path += [(i-3, j-1), (i-2, j-1), (i-2, j-2), (i-3, j-2)]
            path += [(0,0)]

            for i, j in zip(path[:-1], path[1:]):
                assert diff1(i, j)
            assert len(path) == dims[0] * dims[1] + 1
            assert valid(path)

            f.write(to_tikz(path, False))
            f.write("\n\n\\vspace{5mm}\n\n")
