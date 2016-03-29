# -*- coding: utf-8 -*-

import recommendations

reload(recommendations)

info = recommendations.calculate_similar_items(recommendations.critics)

# print info

print recommendations.get_recommended_items(recommendations.critics, info, 'Jack Matthews')
