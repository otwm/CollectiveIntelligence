# -*- coding: utf-8 -*-
import feedparser
import re


def getWordCounts(url):
    """
    단어 숫자 세기

    @type url file_stream or string
    @param url url
    :returns 제목, data
    """

    try:
        print('parse url : ' + url)
        feedInfo = feedparser.parse(url)
        wc = {}

        for entry in feedInfo.entries:
            if 'summary' in entry:
                summary = entry.summary
            else:
                summary = entry.description

            words = getwords(entry.title + ' ' + summary)
            for word in words:
                wc.setdefault(word, 0)
                wc[word] += 1

        return feedInfo.feed.title, wc
    except Exception, e:
        print(e)


def getwords(html):
    """
    단어 분리

    @type html string
    @param html html
    :returns 단어 리스트(소문자)
    """
    txt = re.compile(r'<[^>]+>').sub('', html)
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    return [word.lower() for word in words if word != '']

    # text = bs4.BeautifulSoup(html, "html.parser").get_text().strip()
    # # 단어를 분리
    # words = text.split()
    # # 소문자로 변환함
    # return [word.lower() for word in words if word != '']