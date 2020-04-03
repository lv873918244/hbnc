#coding = utf-8

import time
import json
import requests
import re

appId='61536'#媒体Id

address = 'https://activity.tuiapre.cn'
activity_url = "https://activity.tuiapre.cn/activity/index?id=19353&slotId=310172&login=normal&appKey=kEzAJT4iRMMag29Z7yWcJGfcVgG&deviceId=b3324f-8e14-446f-bd4d-83041f432e33&dsm=1.310172.0.0&dsm2=1.310172.2.19353&tenter=SOW&subActivityWay=1&tck_rid_6c8=0ad04810k74kmh7v-1081&tck_loc_c5d=tactivity-19353&dcm=401.310172.0.0&&tenter=SOW&visType=0&specialType=0&sourcePage=19353&isTestActivityType=0&userType=1&ep=CTT6X1yzqawAuq19AFfahv9JFoSwBfF_42-0NtOogt-yM3YC4PSgvuiqbmMqNJEy8bVia0zr4z8k2QIzz8s92g=="
# activity_url = "https://activity.tuiapre.cn/activity/index?id=19152&slotId=327666&deviceId=188b933bbc8379134409d9282874f49d&login=normal&appKey=2yncSxukc1p7QMgqw5MiCDfq6NU5&sourceId=19152&sourceType=3&subActivityWay=1&sourcePage=19113&tck_rid_6c8=0acc645fk6uhyp32-10561367&imei=188b933bbc8379134409d9282874f49d&ep=OVmZHBXSTMxZbtXc4YHRMhlIampoMzTxCTCRy8JdNrc5Mw9lNBU_GeUahiTn_5xzAdlOFD0hi4QomjMGqDA4cQ==&activityPage=19113&dpm=69640.66.2.1&dcm=701.19152.0.19113&dsm=1.327666.1.19113&dsm2=1.327666.2.19113"
print(activity_url)
res = requests.get(activity_url)
cookies = requests.utils.dict_from_cookiejar(res.cookies)

facilityType=2#风车
headers_all = {
    "Content-Type": "application/json; charset=UTF-8"
}




#获取cookie，headers
sessions = requests.session()
sessions.get(activity_url)


#断言
def DY(data,check_point):
    #断言检查
    a = str(data)
    check = str(check_point)
    if a.find(check) != -1:
        return True
    else:
        print("未找到此数据：" + check)
        return False


#异常结果判断
def printlog(ways,url,datas):
    try:
        if ways=='GET':
            a = sessions.get(url,params =datas)
            if a.status_code==200:
                if DY(json.loads(a.text, encoding='utf-8'),'000000') is False:
                    rsp = json.loads(a.text, encoding='utf-8')
                    log = "接口未成功，报错为:" + str(rsp)
                    print(log)
                    return log
                else:
                    return a
            else:
                rsp = json.loads(a.text, encoding='utf-8')
                log = "接口信息异常，报错为:" + str(rsp)
                print(log)
                return log
        elif ways=='POST':
            a =sessions.post(url=url,data=json.dumps(datas),headers=headers_all,cookies = cookies)
            if a.status_code==200:
                if DY(json.loads(a.text, encoding='utf-8'),'000000') is False:
                    rsp = json.loads(a.text, encoding='utf-8')
                    log = "接口未成功，报错为:" + str(rsp)
                    print(log)
                    return log
                else:
                    return a
            else:
                rsp = json.loads(a.text, encoding='utf-8')
                log = "接口信息异常，报错为:" + str(rsp)
                print(log)
                return log
    except AttributeError as e:
        log = "未知错误,接口名称为:" + str(url)
        print(log)
        return log


#引用url
def url_get(activity_url):
    global deviceId
    global activityId
    global slotId
    url = activity_url
    deviceId = re.search(r'(?<=&deviceId=).*?(?=&)', url, re.M).group()
    activityId = re.search(r'(?<=index\?id=).*?(?=&)', url, re.M).group()
    slotId = re.search(r'(?<=&slotId=).*?(?=&)', url, re.M).group()

    get_url = {
        'deviceId': deviceId,
        'activityId': activityId,
        'slotId' : slotId
    }
    return get_url



#获取当前用户详情
def user():
    url = address + '/commercialloanv/farm/initialize'
    data = {

        "slotId": slotId,
        "activityId": activityId,
    }
    a = printlog('GET', url, data)
    rsp = json.loads(a.text, encoding='utf-8')
    return rsp


#收获果实
def pick(seedID):
    url = address + '/commercialloanv/farm/pickFruit'
    data = {
        "slotId":slotId,
        "activityId":activityId,
        "fruitIds":[seedID]
    }
    a = printlog('POST', url, data)

def update_UserCash():
    #添加用户金币余额
    url = address + "/commercialloanv/farm/test/updateBalance"
    data = {
        "appId": appId,
        "deviceId": deviceId,
        "redPacket": 0,
        "cash":100000000
    }
    a = printlog("GET", url, data)




#刷新果实成熟时间
def updateTime(fruitid):
    url = address + '/commercialloanv/farm/test/updateFruitRipeTime'
    data = {
        "fruitId": fruitid,
    }
    a = printlog('GET', url, data)

def water_Update():
    #灌溉升级
    url = address + "/commercialloanv/farm/prop/waterUpgrade"

    data = {
        "slotId": slotId,
        "activityId": activityId
    }
    a = printlog("POST", url, data)


#灌溉
def water():
    url = address + '/commercialloanv/farm/prop/water'
    data = {
        "clickAmount": 1,
        "activityId": activityId,
        "slotId": slotId,
    }
    a =printlog('POST', url, data)

def fruit_Update():
    #果实升级
    url = address + "/commercialloanv/farm/upgradeFruit"
    data = {
        "slotId": slotId,
        "activityId": activityId,
        "fruitType": 2
    }
    a = printlog("POST", url, data)

def farm_update(facilityType):
    #农场升级
    url = address + "/commercialloanv/farm/farmUpgrade"
    data = {
        "slotId": slotId,
        "activityId": activityId,
        "facilityType": facilityType
    }
    a = printlog("POST", url, data)

#解锁3-7块土地
def unlockLand(landId):
    url = address + '/commercialloanv/farm/unlockLand'
    data = {
        "activityId": activityId,
        "slotId": slotId,
        "landId":landId,
    }
    a = printlog('GET', url, data)


#小游戏
def game(i):
    url = address + '/commercialloanv/farm/reportActivity'
    data = {
        "activityId": activityId,
        'type': i,#活动类型 1、激励互动 2、侧边栏小游戏
        'slotId':slotId,
    }
    a = printlog('POST', url, data)

#完成任务
def finish(missionId):
    url = address + '/commercialloanv/farm/finishMission'
    data = {
        "activityId": activityId,
        'missionId': missionId,  #任务Id
        'slotId': slotId,
    }
    a = printlog('POST', url, data)

#收取宝箱
def baoxiang():
    url = address + '/commercialloanv/farm/randomEvent'
    data = {
        'type':1,#1-宝箱    2 - 打地鼠  3-神秘访客
        'detailType':0, #其他的默认传0 神秘访客时传 1、A金币 2、B金币 3、C金币
        'landId':1,#表示几号土地
        'resultType':1,#触发随机事件的方式 0表示到事件消失 1表示触发了
    }
    a = printlog('POST', url, data)


#收取风车红包
def receiveReward():
    url = address + '/commercialloanv/farm/finance/receiveReward'
    data = {
        'slotId': slotId,
        "activityId": activityId,
        "type":2,  #1.离线收益 2.设施奖励
        "subType":2 #若为设施类型 2.风车 5.仓库 6.推车 离线收益0
    }
    a = printlog('GET', url, data)


#校验红包个数
def packnum():
    url = address + '/commercialloanv/farm/finance/redPacketDetail'
    data = {
        "activityId": activityId,
        'slotId': slotId,
        'start': 0,  #开始
        'size': 1,  #每页个数
    }
    a = printlog('GET', url, data)

#重置签到信息
def signin():
    url = address + '/commercialloanv/farm/test/resetSignInfo'
    data = {
        'deviceId': deviceId,
        'appId': appId,
        'signDays':[1,2,3,4,5,6],  # 周期内哪几天签到
        'todaySign':7, #指定今天是第几天
        'signStage':1, #第几周期的签到
    }
    a = printlog('POST', url, data)

#领取签到奖励
def ReceivesignIn():
    url = address + '/commercialloanv/farm/signIn'
    data = {
        'activityId': activityId,
        'appId': appId,
    }
    a = printlog('POST', url, data)


#普通换天接口
def nextday():
    url = address + '/commercialloanv/farm/test/resetForTest'
    data = {
        'deviceId': deviceId,
        'appId': appId,
    }
    a = printlog('GET', url, data)

#重置风车时间接口
def fengche():
    url = address + '/commercialloanv/farm/test/resetFacilityFinishTime'
    data = {
        'deviceId': deviceId,
        'appId': appId,
        'facilityType': facilityType,
    }
    a = printlog('GET', url, data)

#重置宝箱次数接口
def chongzhibaoxiang():
    url = address + '/commercialloanv/deletefKey'
    data = {
        'str': str(appId) + '-' + str(cookies['userId']),
    }
    a = printlog('GET', url, data)

#重置阶梯开始接口
def chongzhijieti():
    url = address + '/commercialloanv/farm/test/updateStageStartTime'
    data = {
        'deviceId': deviceId,
        'appId':appId,
    }
    a = printlog('GET', url, data)


#用户登陆天数
def signDays():
    user()
    # 获取用户登陆天数
    c = int(user()['data']['user']['signDays'])
    return c

#用户当前红包余额
def redPacket():
    user()
    c = int(user()['data']['user']['redPacket'])
    return c





#新手礼包领取
def fetchGift(days):

    if days < 4:
        url = address + '/commercialloanv/farm/fetchGift'
        data = {
            "skinVersion":2,
            "slotId":slotId,
            "isNewUser":True
        }
        printlog('POST', url, data)
        print("新手礼包领取完毕")
    else:
        print('超过三天没有新手礼包')

#第一天
def run_one():
    # 初始化接口
    url_get(activity_url)
    user()
    # 收果实
    for i in range(0, 3):
        o = user()
        pick(o['data']['land'][0]['fruit']['id'])
        time.sleep(3)
    print("收取萝卜三次")

    # 修改金币
    update_UserCash()
    user()
    print("金币修改完毕，当前余额为" + str(user()['data']['user']['cash']))

    # 解锁南瓜
    unlockLand(o['data']['land'][1]['landId'])
    print("已解锁土地2--南瓜")

    # 灌溉升级5次
    for water_times in range(0, 5):
        water_Update()
        time.sleep(1)
    print("灌溉升级5次")

    # 果实升级
    for fruit_Update_times in range(0, 3):
        fruit_Update()
        time.sleep(1)
    print("果实南瓜升级3次")

    # 小游戏
    for game_Times_num in range(0, 3):
        game(2)
        time.sleep(1)
    print("小游戏次数3次")

    # 随机事件--宝箱

    appearedTimes = int(user()['data']['randomEvent'][0]['appearedTimes'])
    appearTimes = int(user()['data']['randomEvent'][0]['appearTimes'])
    random_box_times = appearTimes - appearedTimes
    if random_box_times != 0:
        for random_Event_box_num in range(0, random_box_times):
            baoxiang()
            time.sleep(1)
        print("随机事件" + str(appearedTimes) + "次抽完")
    else:
        print("宝箱获取次数已用完")

    # 解锁升级设施
    for farm_update_num in range(1, 8):
        for facilityType_num in range(0, 2):
            time.sleep(1)
            farm_update(farm_update_num)
    print("解锁升级设施12次")

    for landId in range(1, 7):
        o = user()
        unlockLand(o['data']['land'][landId]['landId'])
        time.sleep(1)
        user()
    print('解锁3-7块土地,依次为菠萝,玉米,甘蔗,草莓,西瓜')


    # 完成任务
    mission = user()
    for missions in mission['data']['mission']:
        if missions['status'] == 1:
            finish(missions['id'])

    #风车收取红包
    for l in range(0, 2):
        fengche()
        time.sleep(35)
        receiveReward()
    print("已收取风车红包两个")
    print("用户余额：" + str(user()['data']['user']['cash']) + "红包余额；" + str(
        user()['data']['user']['redPacket']))
    print("------------------------------------------------")
#第二天及以后普通天
def run_two():
    # 初始化接口

    user()
    # 收果实
    for i in range(0, 3):
        o = user()
        pick(o['data']['land'][0]['fruit']['id'])
        time.sleep(3)
    print("收取萝卜三次")


    # 累计金币
    update_UserCash()
    user()
    print("金币修改完毕，当前余额为" + str(user()['data']['user']['cash']))

    # 小游戏
    for game_Times_num in range(0, 3):
        game(2)
        time.sleep(1)
    print("小游戏次数3次")

    # 随机事件--宝箱
    appearedTimes = int(user()['data']['randomEvent'][0]['appearedTimes'])
    appearTimes = int(user()['data']['randomEvent'][0]['appearTimes'])
    random_box_times = appearTimes - appearedTimes
    if random_box_times != 0:
        for random_Event_box_num in range(0, random_box_times):
            baoxiang()
            time.sleep(1)
        print("随机事件" + str(appearedTimes) + "次抽完")
    else:
        print("宝箱获取次数已用完")

    # 完成任务
    mission = user()
    for missions in mission['data']['mission']:
        if missions['status'] == 1:
            finish(missions['id'])


    #风车收取红包
    for l in range(0, 2):
        fengche()
        time.sleep(35)
        receiveReward()
    print("已收取风车红包两个")
    print("用户余额：" + str(user()['data']['user']['cash']) + "红包余额；" + str(
        user()['data']['user']['redPacket']))
    print("------------------------------------------------")


#获取配置项参数
#初始化接口
url_get(activity_url)

#获取提现门槛
withdrawThreshold = int(user()['data']['conversion'][0]['withdrawThreshold'])

#红包余额
user_redPacket = int(redPacket())

while user_redPacket < withdrawThreshold:
    days = signDays()
    if days == 1:
        print("当前第" + str(days) + "天")
        #新手礼包
        # fetchGift(days)
        # 第一天操作
        run_one()
        user_redPacket = int(redPacket())
    else:
        print("当前第" + str(days) + "天")
        #新手礼包
        # fetchGift(days)
        #第二天及以后
        run_two()
        user_redPacket = int(redPacket())
    print(str(user_redPacket))
    if int(redPacket()) > withdrawThreshold:
        break
    #换天
    nextday()
    chongzhibaoxiang()
    chongzhijieti()


print("用户红包余额：" + str(user_redPacket) + "个，运行结束")



















