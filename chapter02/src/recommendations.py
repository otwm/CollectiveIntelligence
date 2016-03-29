# -*- coding: utf-8 -*-

# A dictionary of movie critics and their ratings of a small
# 데이터
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}

from math import sqrt


def sim_distance(data, person1, person2):
    """
    선호도 계산(유클리디안)

    @type data: dict
    @param data: 데이터

    @type person1: 사람1
    @param person1: 사람1

    @type person2: 사람2
    @param person2: 사람2

    :return 선호도
    """
    si = {}
    for item in data[person1]:
        if item in data[person2]:
            si[item] = 1

    if len(si) == 0: return 0
    sum_of_squares = sum([pow(data[person1][item] - data[person2][item], 2)
                          for item in data[person1] if item in data[person2]])
    return 1 / (1 + sqrt(sum_of_squares))


def sim_peason(data, person1, person2):
    """
    선호도 계산(피어슨)

    @type data: dict
    @param data: 데이터

    @type person1: 사람1
    @param person1: 사람1

    @type person2: 사람2
    @param person2: 사람2

    :return 선호도
    """

    common = {}
    for item in data[person1]:
        if item in data[person2]: common[item] = 1

    n = len(common)

    if n == 0: return 0

    sum1 = sum([data[person1][it] for it in common])
    sum2 = sum([data[person2][it] for it in common])

    sum1Sq = sum([pow(data[person1][it], 2) for it in common])
    sum2Sq = sum([pow(data[person2][it], 2) for it in common])

    pSum = sum([data[person1][it] * data[person2][it] for it in common])

    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))

    if den == 0: return 0

    r = num / den

    return r


def topMatches(prefs, person, n=5, similarity=sim_peason):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


def getRecommendations(prefs, person, similarity=sim_peason):
    totals = {}
    simSums = {}

    for other in prefs:
        if other == person: continue
        sim = similarity(prefs, person, other)

        if sim <= 0: continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                simSums.setdefault(item, 0)
                simSums[item] += sim

    rankings = [(total / simSums[item], item) for item, total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings


def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]

    return result
