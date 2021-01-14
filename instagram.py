import sqlite3
import requests
import json
import shutil
import os

'''
QueryID,Endpoint
17875800862117404,posts for tags
17874545323001329,user following
17851374694183129,user followers
17888483320059182,user posts
17864450716183058,likes on posts
17852405266163336,comments on posts
17842794232208280,posts on feed
17847560125201451,feed profile suggestions
17863787143139595,post suggestions
'''


class Instagram:
    def __init__(self):
        self.cookie = self.get_cookie()
        self.my_id = self.cookie['ds_user_id']
        self.header = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; motorola one Build/OPKS28.63-18-3; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 Instagram 72.0.0.21.98 Android (27/8.1.0; 320dpi; 720x1362; motorola; motorola one; deen_sprout; qcom; pt_BR; 132081645)',
            'Accept': '*/*'}

    # TODO: using login mechanism instead of cookie
    def get_cookie(self):
        if 'linux' in os.sys.platform:
            # For firefox browser
            try:
                dirs = os.listdir(os.getenv('HOME') + '/.mozilla/firefox/')
                for d in dirs:
                    if 'default-release' in d:
                        path = os.getenv('HOME') + '/.mozilla/firefox/' + d + '/cookies.sqlite'
                shutil.copy(path, './cookies.sqlite')
            except:
                print('Error: firefox cookie for instagram login not found')
                return 0
            db = sqlite3.connect("./cookies.sqlite")
            cur = db.cursor()
            query = "SELECT name, value FROM moz_cookies WHERE (host='.instagram.com');"
            cur.execute(query)
            cookie = dict(cur.fetchall())
            return cookie

    def get_user_info_by_id(self, user_id):
        url = 'https://i.instagram.com/api/v1/users/{}/info/'.format(user_id)
        res = requests.get(url, cookies=self.cookie, headers=self.header)
        return json.loads(res.content)

    def get_user_followings(self, user_id, number):
        if number > 100:
            print("user followings are more than 100, are you sure you want to proceed?[Y/N]: ", end=' ')
            if input() != 'Y':
                return []
        # query_id = '17874545323001329'
        res = requests.get(
            'https://www.instagram.com/graphql/query/?query_id=17874545323001329&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A{}%7D'.format(
                user_id, number), cookies=self.cookie, headers=self.header)

        following = json.loads(res.content)
        nodes = following['data']['user']['edge_follow']['edges']
        following_list = []
        for node in nodes:
            following_list.append((node['node']['id'], node['node']['username'], node['node']['full_name']))
        return following_list

    def get_user_followers(self, user_id, number):
        if number > 100:
            print("user  followers are more than 100, are you sure you want to proceed?[Y/N]: ", end=' ')
            if input() != 'Y\n':
                return []
        # query_id = '17851374694183129'
        res = requests.get(
            'https://www.instagram.com/graphql/query/?query_id=17851374694183129&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A{}%7D'.format(
                user_id, number), cookies=self.cookie, headers=self.header)
        following = json.loads(res.content)
        nodes = following['data']['user']['edge_followed_by']['edges']
        followers_list = []
        for node in nodes:
            followers_list.append((node['node']['id'], node['node']['username'], node['node']['full_name']))
        return followers_list

    def get_user_posts(self, user_id, number):
        # query_id = '17888483320059182'
        user_info = self.get_user_info_by_id(user_id)
        if user_info['user']['is_private'] == 'false':
            res = requests.get(
                'https://www.instagram.com/graphql/query/?query_id=17888483320059182&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A{}%7D'.format(
                    user_id, number), cookies=self.cookie, headers=self.header)
            with open('posts.json', 'w') as fd:
                fd.write(res.content)
        else:
            print("Error account is private")
