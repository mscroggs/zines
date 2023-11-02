from zines import find

for i, dims in enumerate([(2, 2), (4, 2), (4, 4), (8, 4), (8, 8), (16, 8)]):
    assert dims[0] * dims[1] == 2 ** (i + 2)
    res = find(*dims)
    print(i + 2, len(res))
