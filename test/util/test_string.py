from upylib.util.string import substr


def test_substr():
    s = "aabb1234ss"

    before, match, end = substr(s, "b", "s", contain_patt=True)
    print(before, match, end)

    before, match, end = substr(s, "b", "s", contain_patt=False)
    print(before, match, end)
