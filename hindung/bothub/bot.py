# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)
import requests
from bs4 import BeautifulSoup
import random 

from bothub_client.bot import BaseBot
from bothub_client.decorators import channel
from bothub_client.messages import Message


class Bot(BaseBot):

    @channel()
    def default_handler(self, event, context):

        content = event['content']
    
        if content =='사용법':
          self.chatbot_text(event)
        

        elif content == '영화추천':    
          self.recmovie(event)

        elif content == '영화차트':
           self.movie(event)

        else:
          self.search_word(event)

    def movie(self, event):
      Tag = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol > li > div.box-contents > a > strong'
      URL= 'http://www.cgv.co.kr/movies/'

      req = requests.get(URL)
      html = req.text
      soup = BeautifulSoup(html, 'html.parser') 

      all_a = soup.select(Tag)
      movielist=[]
      num=["1위 : ", "2위 : ", "3위 : ", "4위 : ", "5위 : ", "6위 : ", "7위 : "]
      for title in all_a:
        movielist.append(title.text)

      for a in range(0, 7, 1):
        self.send_message(num[a]+movielist[a])

    def recmovie(self, event):
      TagTitle='#contents > div.wrap-movie-chart > div.sect-movie-chart > ol > li > div.box-contents > a > strong'

      URL = 'http://www.cgv.co.kr/movies/'

      req = requests.get(URL)
      html = req.text
      soup = BeautifulSoup(html, 'html.parser')

      all_title = soup.select(TagTitle)


      titleList = []


      for title in all_title:
        titleList.append(title.text)

      message = "인기 순위에 있는 [" + random.choice(titleList) + "]을 추천합니댱"
      self.send_message(message)


    def chatbot_text(self, event):
      message = "영화 추천을 입력하시면 영화를 추천, 영화차트를 입력하시면 영화 인기 순위를 보여줍니다."
      self.send_message(message)

    
