# -*- coding: utf-8 -*-

import random
from deliciousrec import *
from recommendations import *

users = initialize_user_dict('programing')
fill_items(users)

# print users
user = users.keys()[random.randint(0, len(users) - 1)]

print "================== 유사도 랭크 ==================\n"
print "user :" + user + "\n"

print "1. 피어슨 \n"
print top_matches(users, user, similarity=sim_peason)
print "2. 유클리디안 \n"
print top_matches(users, user, similarity=sim_distance)

print "================== 추천 ==================\n"
print getRecommendations(users, user)[0: 10]

print "================== 유사링크 ==================\n"
url = getRecommendations(users, user)[0][1]
print top_matches(transform_prefs(users), url)
