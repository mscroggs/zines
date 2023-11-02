from zines import find, to_tikz

for i, dims in enumerate([(2, 2), (4, 2), (4, 4), (8, 4), (8, 8)]):
    print("Starting", i)
    fname = f"output/routes{i+1}.tex"
    with open(fname, "w") as f:
        f.write("\\documentclass{standalone}\n")
        f.write("\\usepackage{tikz}\n")
        f.write("\\begin{document}\n")
    assert dims[0] * dims[1] == 2 ** (i + 2)
    for path in find(*dims):
        with open(fname, "a") as f:
            f.write(to_tikz(path))
    with open(fname, "a") as f:
        f.write("\\end{document}\n")
    print("Finished", i)
