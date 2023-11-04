from zines import find
from time import time

assert len(find(2, 2)) == 1
assert len(find(4, 2)) == 1
assert len(find(4, 4)) == 1
assert len(find(8, 4)) == 3

with open("b367038.txt", "w") as f:
    pass
for i, dims in enumerate([(2, 2), (4, 2), (4, 4), (8, 4), (8, 8), (16, 8)]):
    assert dims[0] * dims[1] == 2 ** (i + 2)
    start = time()
    term = len(find(*dims))
    print(i + 2, term, f"(computed in {time() - start}s)")
    with open("b367038.txt", "a") as f:
        f.write(f"{i+2} {term}\n")
