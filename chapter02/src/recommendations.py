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


def transform_data(data):
    """
     데이터를 아이템 기준으로 변경한다.
     @type data: dict
     @param data: 데이터
    """
    result = {}
    for person in data:
        for item in data[person]:
            result.setdefault(item, {})
            result[item][person] = data[person][item]

    return result


def calculate_similar_items(data, rank=10):
    """
     아이템 별로 랭크를 구한다.

     @type data: dict
     @param data: 데이터

     @type rank: int
     @param rank: 랭크
    """
    result = {}
    data_by_item = transform_data(data)

    c = 0
    for item in data_by_item:
        c += 1
        if c % 100 == 0:
            print "%d / %d " % (c, len(data_by_item))
        scores = topMatches(data_by_item, item, n=rank, similarity=sim_distance)
        result[item] = scores
    return result


def get_recommended_items(data, item_match, user):
    """
     아이템을 추천한다.

     @type data: dict
     @param data: 데이터

     @type item_match: dict
     @param item_match: 통계된 정보

     @type user: string
     @param user: 사용자
    """
    user_ratings = data[user]
    scores = {}
    total_sim = {}

    for (item, rating) in user_ratings.items():
        for (similarity, item2) in item_match[item]:

            # 사용자가 이미 평가 했다면, 패스 한다.
            # 왜냐고? 이미 봤으니까!
            if item2 in user_ratings:
                continue

            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            # 도데체 왜?? 이런식으로 구해야 하나?? =ㅅ=?? 알듯 말 듯?
            total_sim.setdefault(item2, 0)
            total_sim[item2] += similarity * rating

            total_sim.setdefault(item2, 0)
            total_sim[item2] += similarity

    result = [(score / total_sim[item], item) for item, score in scores.items()]

    result.sort()
    result.reverse()
    return result


def load_movie_lens(path='/home/kdo/dev/PycharmProjects/CollectiveIntelligence/chapter02/resources'):
    """
     영화 정보를 로드

     @type path: string
     @param path: 데이터 경로
    """
    movies = {}

    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    data = {}

    for line in open(path + '/u.data'):
        (user, movie_id, rating, ts) = line.split('\t')
        data.setdefault(user, {})
        data[user][movies[movie_id]] = float(rating)

    return data
