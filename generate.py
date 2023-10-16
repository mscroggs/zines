import math
import matplotlib.pylab as plt
from zines import to_tikz, find


next = ["\n\\hspace{5mm}\n", "\n\n\\vspace{5mm}\n\n"]

with open("diagrams.tex", "w") as f:
    for dims in [(4, 2), (4, 4), (8, 4), (8, 8), (16, 8)]:
        print(dims)
        res = find(*dims)
        print(len(res))
        for i, r in enumerate(res):
            f.write(to_tikz(r))
            f.write(next[i % len(next)])

        f.write("\\newpage")
