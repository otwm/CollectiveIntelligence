# -*- coding: utf-8 -*-

import time
from pydelicious import get_popular, get_userposts, get_urlposts


def initialize_user_dict(tag, count=5):
    """
    사용자 정보 초기화
    특정 키워드에 관심 있는 여러 사용자들의 정보를 가지고 오나부다.

    @type tag: string
    @param tag: 검색 태그

    @type count: int
    @type count: 검색 수

    :return 사용자들 정보
    """
    user_dict = {}
    try:
        for p1 in get_popular(tag=tag)[0:count]:
            for p2 in get_urlposts(str(p1['url'])):
                user = str(p2['user'])
                user_dict[user] = {}
    except Exception, e:
        # 404 등 에러 처리
        print("========================================")
        print e
        print("========================================")

    return user_dict


def fill_items(user_dict):
    """
    사용자 정보를 채운다.
    사용자의 포스트 정보를 채운다.
    포스트를 본 적(?)이 있다면 1.0이 될 것이다.

    @type user_dict: dict
    @param user_dict: 사용자 정보

    :return 모든 정보
    """
    all_items = {}

    for user in user_dict:
        for i in range(3):
            try:
                posts = get_userposts(user)
                break
            except Exception, e:
                print e
                print "failed user " + user + ", tetrying"
                time.sleep(4)

        for post in posts:
            url = str(post['url'])
            user_dict[user][url] = 1.0
            # 모든 아이템을 수집한다.
            all_items[url] = 1

    for ratings in user_dict.values():
        for item in all_items:
            if item not in ratings:
                ratings[item] = 0.0

    return all_items
