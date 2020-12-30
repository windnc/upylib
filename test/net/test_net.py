from upylib.net.url import read_url, urlenc


def test_url():
    url = "http://naver.com"
    r = read_url(url, retry=1)
    print(len(r))
    assert r


def test_urlenc():
    q = "한글 문자열"
    qenc = urlenc(q)
    print(qenc)
    assert qenc
