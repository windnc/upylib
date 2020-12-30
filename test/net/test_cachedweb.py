from upylib.net.cachedweb import CachedWeb


def test_cachedweb1():
    c = CachedWeb(cache_dir="cachedweb-data")
    assert c


def test_cachedweb2():
    c = CachedWeb(cache_dir="cachedweb-data")
    r = c.delete("http://naver.com")
    r = c.search("http://naver.com")
    assert r is not False


def test_cachedweb3():
    c = CachedWeb(cache_dir="cachedweb-data")
    r = c.cached_search("http://naver.com")
    assert r is not False
    print(len(r))


def test_cachedweb4():
    c = CachedWeb(cache_dir="cachedweb-data")
    r = c.get_count()
    print(r)


def test_cachedweb5():
    c = CachedWeb(cache_dir="cachedweb-data")
    r = c.cached_search("http://google.com")
    r = c.cached_search("http://daum.net")
    for url, html in c.fetch_data():
        print(url, len(html))
