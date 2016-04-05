# -*- coding: utf-8 -*-
import generatefeedvector

apcount = {}
wordcounts = {}
feedlist = []

for feedurl in file('feedlist.txt'):
    try:
        feedlist.append(feedurl)
        title, wc = generatefeedvector.getWordCounts(feedurl)
        wordcounts[title] = wc

        for word, count in wc.items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[word] += 1
    except Exception, e:
        print e

# print apcount
# print wordcounts
# print feedlist

wordlist = []
for w, bc in apcount.items():
    frac = float(bc) / len(feedlist)
    if frac > 0.1 and frac < 0.5:
        wordlist.append(w)

out = file('blogdata.txt', 'w')
out.write('Blog')

for word in wordlist:
    try:
        out.write('\t%s' % word)
    except Exception, e:
        print e

out.write('\n')

for blog, wc in wordcounts.items():
    try:
        out.write(blog)
        for word in wordlist:
            if word in wc:
                out.write('\t%d' % wc[word])
            else:
                out.write('\t0')
        out.write('\n')
    except Exception, e:
        print e
