#-*- coding : utf-8 -*-

import time
from hbncAPI import api_all,get_parm
import configparser
import os

#配置文件获取
curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, "config.ini")


config = configparser.ConfigParser()
config.read(cfgpath,encoding="utf-8")

activity_url = config['url']['activity_url']
appId=config['url']['appId']

address=config['url']['address']

headers_all = {"Content-Type": "application/json; charset=UTF-8"}


parms = get_parm(activity_url,appId,address,headers_all)

print(activity_url)
test01 = api_all(parms.parm())

#第一天
def run_one():
    # 初始化接口
    test01.user()
    # 收果实
    for i in range(0, 3):
        o = test01.user()
        test01.pick(o['data']['land'][0]['fruit']['id'])
        time.sleep(3)
    print("收取萝卜三次")

    # 修改金币
    test01.update_UserCash()
    test01.user()
    print("金币修改完毕，当前余额为" + str(test01.user()['data']['user']['cash']))

    # 解锁南瓜
    test01.unlockLand(o['data']['land'][1]['landId'])
    print("已解锁土地2--南瓜")

    # 灌溉升级5次
    # for water_times in range(0, 5):
    #     test01.water_Update()
    #     time.sleep(1)
    # print("灌溉升级5次")

    # 果实升级
    # for fruit_Update_times in range(0, 3):
    #     test01.fruit_Update()
    #     time.sleep(1)
    # print("果实南瓜升级3次")

    # 小游戏
    for game_Times_num in range(0, 3):
        test01.game(2)
        time.sleep(1)
    print("小游戏次数3次")

    # 随机事件--宝箱

    appearedTimes = int(test01.user()['data']['randomEvent'][0]['appearedTimes'])
    appearTimes = int(test01.user()['data']['randomEvent'][0]['appearTimes'])
    random_box_times = appearTimes - appearedTimes
    if random_box_times != 0:
        for random_Event_box_num in range(0, random_box_times):
            test01.baoxiang()
            time.sleep(1)
        print("随机事件" + str(appearTimes) + "次抽完")
    else:
        print("宝箱获取次数已用完")

    # 解锁升级设施
    for farm_update_num in range(1, 8):
        for facilityType_num in range(0, 2):
            time.sleep(1)
            test01.farm_update(farm_update_num)
    print("解锁升级设施12次")

    # for landId in range(1, 7):
    #     o = test01.user()
    #     test01.unlockLand(o['data']['land'][landId]['landId'])
    #     time.sleep(1)
    #     test01.user()
    # print('解锁3-7块土地,依次为菠萝,玉米,甘蔗,草莓,西瓜')


    # 完成任务
    mission = test01.user()
    for missions in mission['data']['mission']:
        if missions['status'] == 1:
            test01.finish(missions['id'])

    #风车收取红包
    for l in range(0, 1):
        test01.fengche()
        time.sleep(35)
        test01.receiveReward()
    print("已收取风车红包两个")
    print("用户余额：" + str(test01.user()['data']['user']['cash']) + "红包余额；" + str(
        test01.user()['data']['user']['redPacket']))
    print("------------------------------------------------")
#第二天及以后普通天
def run_two():
    # 初始化接口

    test01.user()
    # 收果实
    # for i in range(0, 3):
    #     o = test01.user()
    #     test01.pick(o['data']['land'][0]['fruit']['id'])
    #     time.sleep(3)
    # print("收取萝卜三次")


    # 累计金币
    test01.update_UserCash()
    test01.user()
    print("金币修改完毕，当前余额为" + str(test01.user()['data']['user']['cash']))

    # 小游戏
    for game_Times_num in range(0, 3):
        test01.game(2)
        time.sleep(1)
    print("小游戏次数3次")

    # 随机事件--宝箱
    appearedTimes = int(test01.user()['data']['randomEvent'][0]['appearedTimes'])
    appearTimes = int(test01.user()['data']['randomEvent'][0]['appearTimes'])
    random_box_times = appearTimes - appearedTimes
    if random_box_times != 0:
        for random_Event_box_num in range(0, random_box_times):
            test01.baoxiang()
            time.sleep(1)
        print("随机事件" + str(appearTimes) + "次抽完")
    else:
        print("宝箱获取次数已用完")

    # 完成任务
    mission = test01.user()
    for missions in mission['data']['mission']:
        if missions['status'] == 1:
            test01.finish(missions['id'])


    #风车收取红包
    for l in range(0, 1):
        test01.fengche()
        time.sleep(35)
        test01.receiveReward()
    print("已收取风车红包两个")
    print("用户余额：" + str(test01.user()['data']['user']['cash']) + "红包余额；" + str(
        test01.user()['data']['user']['redPacket']))
    print("------------------------------------------------")


if __name__ =='__main__':

    #获取提现门槛
    withdrawThreshold = int(test01.user()['data']['conversion'][0]['withdrawThreshold'])

    #红包余额
    user_redPacket = int(test01.redPacket())

    while user_redPacket < withdrawThreshold:
        days = test01.signDays()
        if days == 1:
            print("当前第" + str(days) + "天")
            #新手礼包
            # fetchGift(days)
            # 第一天操作
            run_one()
            user_redPacket = int(test01.redPacket())
        else:
            print("当前第" + str(days) + "天")
            #新手礼包
            # fetchGift(days)
            #第二天及以后
            run_two()
            user_redPacket = int(test01.redPacket())
        print(str(user_redPacket))
        if int(test01.redPacket()) > withdrawThreshold:
            break
        #换天
        test01.nextday()
        test01.chongzhibaoxiang()
        test01.chongzhijieti()


    print("用户红包余额：" + str(user_redPacket) + "个，运行结束")




