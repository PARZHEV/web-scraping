import json
import re

import scrapy
from scrapy import item
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from instaparser.items import InstaparserItem
from copy import deepcopy


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = "https://www.instagram.com/accounts/login/ajax/"
    inst_login_name = 'tobi.poter2022'
    inst_login_pwd = '#PWD_INSTAGRAM_BROWSER:10:1642503257:AbhQAN6B9dVcQ6UhIwSakFvlA49tdmcUDmNZaWA1Kh1/loB4fp8JcV+PTB60Z9QrJnMbQNEfIndnMNPqlujsjWPbKzN9+zRELBsrhAz8reCJs5uCS72uJ3Ed5tsta1M3FUoR+J3IPlpYiwCMkvFGSg=='
    parse_user = 'pavel_arzhevitov'
    parse_id_user = '1416701525'
    api_url = 'https://i.instagram.com/api/v1/friendships'
    # https: // i.instagram.com / api / v1 / friendships / 1416701525 / followers /?'


    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login_name, 'enc_password': self.inst_login_pwd},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):

        j_body = response.json()
        if j_body.get('authenticated'):

            yield response.follow(f'/{self.parse_user}',
                                  callback=self.user_data_parse,
                                  cb_kwargs={'username': self.parse_user}
                                  )

    def user_data_parse(self, response: HtmlResponse, username):
        # print()
        # user_id = '1416701525'

        variables = {'count': 12, 'max_id':12, 'search_surface':'follow_list_page'}
        url_posts = f'{self.api_url}/{self.parse_id_user}/followers/?&{urlencode(variables)}'
        yield response.follow(url_posts,
                              callback=self.user_followers_parse,
                              cb_kwargs={'username': username, 'variables':variables},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def user_followers_parse(self, response: HtmlResponse, username, variables):
        # print()
        j_data = response.json()
        page_info = j_data.get('next_max_id')
        if int(page_info) > 0:
            variables['max_id'] = variables['max_id'] + 12

            url_followers = f'{self.api_url}/{self.parse_id_user}/followers/?&{urlencode(variables)}'
            yield response.follow(url_followers,
                                  callback=self.user_followers_parse,
                                  cb_kwargs={'username': username, 'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'}
                                  )

        followers = j_data.get('users')
        for follower in followers:
            item = InstaparserItem(
                followerid = follower.get('pk'),
                followername = follower.get('username'),
                followerphoto = follower.get('profile_pic_url'),

            )
            yield item

    def user_followings_parse(self, response: HtmlResponse, username, variables):
        # print()
        j_data = response.json()
        page_info = j_data.get('next_max_id')
        if int(page_info) > 0:
            variables['max_id'] = variables['max_id'] + 12

            url_followers = f'{self.api_url}/{self.parse_id_user}/followers/?&{urlencode(variables)}'
            yield response.follow(url_followers,
                                  callback=self.user_followings_parse,
                                  cb_kwargs={'username': username, 'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'}
                                  )

        followings = j_data.get('users')
        for following in followings:
            item = InstaparserItem(
                followingid = following.get('pk'),
                followingname = following.get('username'),
                followingphoto = following.get('profile_pic_url'),

            )
            yield item

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # def fetch_user_id(self, text, username):
    #     try:
    #         matched = re.search(
    #             '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
    #         ).group()
    #         return json.loads(matched).get('id')
    #     except:
    #         return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]
