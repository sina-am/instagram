from instagram import Instagram
from fuzzywuzzy import fuzz


'''
A simple code for finding your following's following list

'''


# TODO search something in full name field
def search_in_list(self, search_name, user_list):
    match_users = []
    for user in user_list:
        if fuzz.partial_ratio(search_name, user[1]) > 70:
            match_users.append(user)
    return match_users


ig = Instagram()
my_profile = ig.get_user_info_by_id(ig.my_id)
my_followers = ig.get_user_followers(ig.my_id, my_profile['user']['follower_count'])

users_for_search = my_followers[:]

# search in your follower list to find their followers
for user in my_followers:
    user_profile = ig.get_user_info_by_id(user[0])
    users_for_search += ig.get_user_followers(user[0], user_profile['user']['follower_count'])

with open('users_list', 'w') as fd:
    for user in users_for_search:
        fd.write(str(user))
