import requests
import bs4
import re
import pprint
'''
The MIT License (MIT)

Copyright (c) 2015 Jun-Wei Lin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# modify from ptt-web-crawler on github: https://github.com/jwlin/ptt-web-crawler
def parse(link):
    resp = requests.get(url=link, cookies={'over18': '1'}, verify=True, timeout=3)
    if resp.status_code != 200:
        return 'invalid url:' + resp.url

    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    main_content = soup.find(id="main-content")
    metas = main_content.select('div.article-metaline')

    temp = main_content.select('div.article-metaline-right')
    board = temp[0].select('span.article-meta-value')[0].string

    author = metas[0].select('span.article-meta-value')[0].string
    title = metas[1].select('span.article-meta-value')[0].string
    date = metas[2].select('span.article-meta-value')[0].string

    # remove meta nodes
    for meta in metas:
        meta.extract()
    for meta in main_content.select('div.article-metaline-right'):
        meta.extract()

    # remove and keep push nodes
    pushes = main_content.find_all('div', class_='push')
    for push in pushes:
        push.extract()

    # 移除 '※ 發信站:' (starts with u'\u203b'), '◆ From:' (starts with u'\u25c6'), 空行及多餘空白
    # 保留英數字, 中文及中文標點, 網址, 部分特殊符號
    filtered = [v for v in main_content.stripped_strings if v[0] not in [u'※', u'◆'] and v[:2] not in [u'--']]
    expr = re.compile(r'[^\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\s\w:/-_.?~%()]')
    for i in range(len(filtered)):
        filtered[i] = re.sub(expr, '', filtered[i])

    filtered = [_f for _f in filtered if _f]  # remove empty strings
    content = ' '.join(filtered)
    content = re.sub(r'(\s)+', ' ', content)

    data = {
        'author': author,
        'board': board,
        'title': title,
        'date': date,
        'content': content
    }

    pprint.pprint(data)


if __name__ == '__main__':
    parse('https://www.ptt.cc/bbs/WomenTalk/M.1547552622.A.299.html')
    parse('https://www.ptt.cc/bbs/Gossiping/M.1547691603.A.2BE.html')
