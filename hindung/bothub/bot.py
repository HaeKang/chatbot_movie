# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)
import requests
from bs4 import BeautifulSoup
import random 

from bothub_client.bot import BaseBot
from bothub_client.decorators import channel
from bothub_client.messages import Message

ListBack =  [
              '불안정, 한판승부 내기의 실패, 무책임, 계획성이 없다. 길을 잘못들다. 경솔한사랑, 불 같은 성질, 불안한 사랑의 시작',
              '우유뷰단, 다재다능하나 실속없어 성공하지 못함. 사기 당할 위험이 있다. 기술부족, 너무 소극적 센스가 없다. 창조력이 없다. 애정은 진전이 없다. 플레이보이를 조심하라. 연애의 계기를 잡지 못한다.',
              '무지, 무식, 연구부족, 자신의 껍질 속에 틀어 박힘, 결벽증, 제 멋대로, 정신세계에 너무 집착하는, 정신세계에 너무 집착하는, 여자끼리 트러블, 냉대받음, 독신주의, 불임, 성적 매력 부족, 짝사랑으로 끝남.',
              '성취 못함, 동요, 주저, 태만, 허영심이 자멸을 부름, 주제 넘는 제멋대로 행동, 낭비와 손실, 과보호, 권태기, 질투, 원치 않던 임신',
              '미숙, 의지박약, 빛 좋은 개살구, 허세, 자격 없이 권위만 내세우는, 현실인식이 약함, 실무능력 부족, 거만함이 반감을 삼, 업무과다, 독선적 태도, 도둑맞음, 경제적 기반 없음, 쓰디쓴 사랑 결말',
              '신용을 잃음, 원조자가 없음, 고립, 그릇된 충고, 편견, 전통적인 것에 집착, 고마우나 오히려 난처함, 사적인 정 때문에 실패, 동의를 얻지 못함, 조언이나 협력에 매이지 말 것, 인연이 없는 한 쌍',
              '이별, 혼란, 대립, 유혹, 잘못된 선택, 비협력적인 태도, 변심, 불만족스런 성과, 방해가 부딪힌다, 식어가는 사랑, 배신, 사랑 도피행각',
              '패배, 전의상실, 제자리걸음, 좌절, 성급함이 패인, 능률저하, 공허, 벅찬 라이벌 등장, 사랑의 도피는 나쁜 결과로, 소극적이고 진행되지 않는 사랑',
              '겁쟁이, 체념, 실력부족, 강경책으로 반발을 사다, 인내력 부족, 위험한 내기, 우유부단, 유혹에 지다, 체력부족, 무기력',
              '침묵을 깨다. 비밀이 누설된다. 남의 의견을 듣지 않는 편협함, 불순한 동기, 고립, 쓸데없는 한탄과 비꼼으로 미움을 산다. 경박한 사랑',
              '하강기, 시기사조, 예상을 벗어나는 일이 많다, 때를 잘못 만난다, 재수 없을, 불리한 입장, 궁핍함, 악화, 계획을 다시 짜서 때를 기다려야, 실연, 잠깐의 사랑, 어긋남이 많아짐',
              '불공평, 불균형, 불리한 조건, 편파, 선입관, 편견과 독단, 분쟁이나 소송이 일어남, 꺼림직한 행동, 성격의 불일치,도덕을 무시하는 사랑, 편애',
              '열매 맺지 않는 희생, 포기, 둔감함, 도로아미타불, 불리한 입장이 된다, 제멋대로, 필요한 노력을 하지 않는다, 더 이상 참지 못한다, 욕심에 사로잡힌 이기주의자, 벌을 받는다, 이루어지지 않을 사랑',
              '회생의 찬스, 슬럼프 탈출, 이미지체인지, 다시 시작, 기적적인 회생, 포기했던 것이 되돌아온다. 사랑을 버리고 다시 시작한다.',
              '소모하다, 절제 없음이 악영향을 미친다, 인내가 모자람, 쓸데없는 일이 많다, 끝낼 수 없음, 잘 들어맞지 않는다. 애정의 조절이 서로 어설프다, 대립, 불일치, 내성적인 성격이 오해를 부른다',
              '구속에서 도망친다. 오랜 고뇌에서 해방된다, 나쁜 인연에서 해방, 징크스를 깨뜨린다. 나쁜 유혹을 뿌리친다. 욕심을 버림, 병이 나음, 헤어질 기회',
              '긴박한 상황, 험악한 분위기, 복잡한 상황, 내분, 불운의 상황, 형사 문제에 주의, 궁지에 물린 상태, 애정의 위기, 이별의 예감',
              '걸림, 이상이 너무 높다, 안이한 발상, 소망이 이뤄지지 않음, 실망, 좋아하지 않는 일을 하게 됨, 바램이 높음, 기대 밖의 상대, 사랑 없는 생활, 겉모습 중시',
              '직감, 위기를 모면하다, 조금씩 상황호조, 오해가 풀리다, 결심하게 된다, 시간이 해결한다, 긴 안목으로 본다, 정관하고 기다린다, 조기발견, 사전에 위험을 안다, 거짓사랑임을 알아차린다.',
              '부진, 생산력 저하, 화근이 되다. 의기소침하다, 생활불안, 사랑의 파국, 결혼까지 가지 않는 사랑, 이혼, 유산',
              '나쁜 소식, 재기불능, 부활까지 시간이 걸림, 불리한 결정, 연기, 헤어짐, 후회, 미련',
              '미완성, 부조화, 준비부족으로 실패, 도중하차, 슬럼프에 빠지다, 포화상태, 정신이 없음, 미숙함으로 좌절하는 사랑, 애매하나 태도'
            ]

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

    
