# -*- coding: utf-8 -*-

import recommendations

reload(recommendations)

# from deliciousrec import *
# delusers = initialize_user_dict('programing')
# fill_items(delusers)
#
# print delusers

data = recommendations.load_movie_lens()

print '==================== 사용자 ===================='
print data['87']

print '==================== 추천 ===================='
print recommendations.getRecommendations(data, '87')[0:30]

print '==================== 항목 기반 ===================='
item_sim = recommendations.calculate_similar_items(data, rank=50)
print recommendations.get_recommended_items(data, item_sim, '87')[0:30]
