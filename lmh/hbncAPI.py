#-*- coding : utf-8 -*-
# coding: unicode_escape


import time
import json
import requests
from common import print_log
import re

#红包农场参数获取：字典格式输出
class get_parm:

    dict_get = {}

    def __init__(self,url,appId,address,headers_all,dictget= dict_get):
        self.appId = appId
        self.address = address
        self.headers_all = headers_all
        self.dict_get = dictget
        self.url = url

    def parm(self) -> dict:


        deviceId = re.search(r'(?<=&deviceId=).*?(?=&)', self.url, re.M).group()
        activityId = re.search(r'(?<=index\?id=).*?(?=&)', self.url, re.M).group()
        slotId = re.search(r'(?<=&slotId=).*?(?=&)', self.url, re.M).group()

        res = requests.get(self.url)
        cookies = requests.utils.dict_from_cookiejar(res.cookies)
        sessions = requests.session()
        sessions.get(self.url)

        dict_get = {
            'url': self.url,
            'deviceId': deviceId,
            'activityId': activityId,
            'slotId': slotId,
            'appId': self.appId,
            'address': self.address,
            'cookies': cookies,
            'sessions': sessions,
            'headers_all': self.headers_all

        }
        return dict_get



#红包农场接口汇总
class api_all:


    headers_all= None
    cookies = None

    def __init__(self,dic: dict):
        '''

        :param dic: 参数字典
        '''
        self.address = dic['address']
        self.activity_url = dic['url']
        self.headers_all = dic['headers_all']
        self.cookies = dic['cookies']
        self.appId = dic['appId']
        self.sessions = dic['sessions']
        self.slotId = dic['slotId']
        self.activityId = dic['activityId']
        self.deviceId = dic['deviceId']

    def user(self):

        url = self.address + '/commercialloanv/farm/initialize'
        data = {

            "slotId": self.slotId,
            "activityId": self.activityId
        }
        a = print_log.printlog(print_log,'GET',url,data,self.sessions)
        rsp = json.loads(a.text, encoding='utf-8')
        return rsp


    #收获果实
    def pick(self,seedID):
        url = self.address + '/commercialloanv/farm/pickFruit'
        data = {
            "slotId":self.slotId,
            "activityId":self.activityId,
            "fruitIds":[seedID]
        }
        print_log.printlog(print_log,'POST', url, data,self.sessions,headers=self.headers_all,cookies=self.cookies)

    def update_UserCash(self):
        # 添加用户金币余额
        url = self.address + "/commercialloanv/farm/test/updateBalance"
        data = {
            "appId": self.appId,
            "deviceId": self.deviceId,
            "redPacket": 0,
            "cash": 100000000
        }
        print_log.printlog(print_log,"GET", url, data)

    # 刷新果实成熟时间
    def updateTime(self,fruitid):
        url = self.address + '/commercialloanv/farm/test/updateFruitRipeTime'
        data = {
            "fruitId": fruitid,
        }
        print_log.printlog(print_log, "GET", url, data, self.sessions)

    def water_Update(self):
        # 灌溉升级
        url = self.address + "/commercialloanv/farm/prop/waterUpgrade"

        data = {
            "slotId": self.slotId,
            "activityId": self.activityId
        }
        print_log.printlog(print_log, 'POST', url, data, self.sessions, headers=self.headers_all, cookies=self.cookies)

    # 灌溉
    def water(self):
        url = self.address + '/commercialloanv/farm/prop/water'
        data = {
            "clickAmount": 1,
            "activityId": self.activityId,
            "slotId": self.slotId,
        }
        print_log.printlog(print_log, 'POST', url, data, self.sessions, headers=self.headers_all, cookies=self.cookies)

    def fruit_Update(self):
        # 果实升级
        url = self.address + "/commercialloanv/farm/upgradeFruit"
        data = {
            "slotId": self.slotId,
            "activityId": self.activityId,
            "fruitType": 2 #facilityType = 2 风车
        }
        print_log.printlog(print_log, 'POST', url, data, self.sessions, headers=self.headers_all, cookies=self.cookies)

    def farm_update(self,facilityType):
        # 农场升级
        url = self.address + "/commercialloanv/farm/farmUpgrade"
        data = {
            "slotId": self.slotId,
            "activityId": self.activityId,
            "facilityType": facilityType
        }
        print_log.printlog(print_log, 'POST', url, data, self.sessions, headers=self.headers_all, cookies=self.cookies)

    # 解锁3-7块土地
    def unlockLand(self,landId):
        url = self.address + '/commercialloanv/farm/unlockLand'
        data = {
            "activityId": self.activityId,
            "slotId": self.slotId,
            "landId": landId,
        }
        print_log.printlog(print_log, "GET", url, data, self.sessions)

    # 小游戏
    def game(self,i):
        url = self.address + '/commercialloanv/farm/reportActivity'
        data = {
            "activityId": self.activityId,
            'type': i,  # 活动类型 1、激励互动 2、侧边栏小游戏
            'slotId': self.slotId,
        }
        print_log.printlog(print_log, 'POST', url, data, self.sessions, headers=self.headers_all, cookies=self.cookies)

    # 完成任务
    def finish(self,missionId):
        url = self.address + '/commercialloanv/farm/finishMission'
        data = {
            "activityId": self.activityId,
            'missionId': missionId,  # 任务Id
            'slotId': self.slotId,
        }
        print_log.printlog(print_log, 'POST', url, data, self.sessions, headers=self.headers_all, cookies=self.cookies)

    # 收取宝箱
    def baoxiang(self):
        url = self.address + '/commercialloanv/farm/randomEvent'
        data = {
            'type': 1,  # 1-宝箱    2 - 打地鼠  3-神秘访客
            'detailType': 0,  # 其他的默认传0 神秘访客时传 1、A金币 2、B金币 3、C金币
            'landId': 1,  # 表示几号土地
            'resultType': 1,  # 触发随机事件的方式 0表示到事件消失 1表示触发了
        }
        print_log.printlog(print_log, 'POST', url, data, self.sessions, headers=self.headers_all, cookies=self.cookies)

    # 收取风车红包
    def receiveReward(self):
        url = self.address + '/commercialloanv/farm/finance/receiveReward'
        data = {
            'slotId': self.slotId,
            "activityId": self.activityId,
            "type": 2,  # 1.离线收益 2.设施奖励
            "subType": 2  # 若为设施类型 2.风车 5.仓库 6.推车 离线收益0
        }
        print_log.printlog(print_log, "GET", url, data, self.sessions)

    # 校验红包个数
    def packnum(self):
        url = self.address + '/commercialloanv/farm/finance/redPacketDetail'
        data = {
            "activityId": self.activityId,
            'slotId': self.slotId,
            'start': 0,  # 开始
            'size': 1,  # 每页个数
        }
        print_log.printlog(print_log, "GET", url, data, self.sessions)

    # 重置签到信息
    # def signin(self):
    #     url = self.address + '/commercialloanv/farm/test/resetSignInfo'
    #     data = {
    #         'deviceId': self.deviceId,
    #         'appId': self.appId,
    #         'signDays': [1, 2, 3, 4, 5, 6],  # 周期内哪几天签到
    #         'todaySign': 7,  # 指定今天是第几天
    #         'signStage': 1,  # 第几周期的签到
    #     }
    #     print_log.printlog(print_log, 'POST', url, data, self.sessions, headers=self.headers_all, cookies=self.cookies)
    #
    # 领取签到奖励
    # def ReceivesignIn(self):
    #     url = self.address + '/commercialloanv/farm/signIn'
    #     data = {
    #         'activityId': self.activityId,
    #         'appId': self.appId,
    #     }
    #     print_log.printlog(print_log, 'POST', url, data, self.sessions, headers=self.headers_all, cookies=self.cookies)

    # 普通换天接口
    def nextday(self):
        url = self.address + '/commercialloanv/farm/test/resetForTest'
        data = {
            'deviceId': self.deviceId,
            'appId': self.appId,
        }
        print_log.printlog(print_log, "GET", url, data)

    # 重置风车时间接口
    def fengche(self):
        url = self.address + '/commercialloanv/farm/test/resetFacilityFinishTime'
        data = {
            'deviceId': self.deviceId,
            'appId': self.appId,
            'facilityType': 2,
        }
        print_log.printlog(print_log, "GET", url, data)

    # 重置宝箱次数接口
    def chongzhibaoxiang(self):
        url = self.address + '/commercialloanv/deletefKey'
        data = {
            'str': str(self.appId) + '-' + str(self.cookies['userId']),
        }
        print_log.printlog(print_log, "GET", url, data)

    # 重置阶梯开始接口
    def chongzhijieti(self):
        url = self.address + '/commercialloanv/farm/test/updateStageStartTime'
        data = {
            'deviceId': self.deviceId,
            'appId': self.appId,
        }
        print_log.printlog(print_log, "GET", url, data)

    # 用户登陆天数
    def signDays(self):
        self.user()
        # 获取用户登陆天数
        c = int(self.user()['data']['user']['signDays'])
        return c

    # 用户当前红包余额
    def redPacket(self):
        self.user()
        c = int(self.user()['data']['user']['redPacket'])
        return c

    # 新手礼包领取
    def fetchGift(self,days):

        if days < 4:
            url = self.address + '/commercialloanv/farm/fetchGift'
            data = {
                "skinVersion": 2,
                "slotId": self.slotId,
                "isNewUser": True
            }
            print_log.printlog(self, 'POST', url, data, self.sessions, headers=self.headers_all, cookies=self.cookies)
            print("新手礼包领取完毕")
        else:
            print('超过三天没有新手礼包')
