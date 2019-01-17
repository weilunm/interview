import os
import posixpath
from urllib.parse import urlsplit, unquote


def url2filename(url):
    urlpath = urlsplit(url).path
    basename = posixpath.basename(unquote(urlpath))
    if os.path.basename(basename) != basename or unquote(posixpath.basename(urlpath)) != basename:
        raise ValueError  # reject '%2f' or 'dir%5Cbasename.ext' on Windows
    return basename


if __name__ == "__main__":
    urls = [
        "http://www.google.com/a.txt",
        "http://www.google.com.tw/a.txt",
        "http://www.google.com/download/c.jpg",
        "http://www.google.co.jp/a.txt",
        "http://www.google.com/b.txt",
        "https://facebook.com/movie/b.txt",
        "http://yahoo.com/123/000/c.jpg",
        "http://gliacloud.com/haha.png",
    ]
    urlsCnt = {}
    for url in urls:
        url = url2filename(url)
        urlsCnt[url] = urlsCnt.get(url, 0) + 1

    for url in list(urlsCnt)[:3]:
        print(url, '\t', urlsCnt[url])
