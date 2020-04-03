#-*- coding : utf-8 -*-

import json
import requests
import logging
import time
import os
import configparser

'''
接口校验（异常情况处理）
检查点校验

'''
class print_log:

    # 配置文件获取(日志目录，日志文件名称)
    curpath = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(curpath, "config.ini")

    config = configparser.ConfigParser()
    config.read(cfgpath, encoding="utf-8")
    logpath = config['log']['logpath']
    logname = config['log']['logname']


    sessions = requests.session()


    def __init__(self,data,check_point,sessions,url,ways,cookies,path = logpath,logname = logname):
        '''
        :param data: 检查数据
        :param check_point: 检查点
        :param sessions: session
        :param url: activity完整url
        :param ways: 请求方式
        :param cookies: cookie
        :param logpath: 日志路径(默认为当前执行文件路径)
        :param logname: 日志名字(默认为当前执行文件路径下新建test.log)
        '''
        self.data = data
        self.check_point = check_point
        self.sessions = sessions
        self.url = url
        self.ways = ways
        self.cookies = cookies
        self.path = path
        self.logname = logname



    #异常结果判断
    def printlog(self,ways,url,datas,sessions=None,headers=None,cookies=None):
        '''

        :param ways: 请求方式
        :param url: activity完整url
        :param datas: 请求体
        :param sessions: session
        :param headers: 请求头
        :param cookies: cookie

        '''
        if sessions != None:
            sessions.get(url)
        else:
            sessions=requests
            requests.get(url)
        logging.basicConfig(level=logging.WARNING,
                            format="%(levelname)s %(message)s",
                            datefmt='%Y-%m-%d %H:%M:%S %a',  # 注意月份和天数不要搞乱了，这里的格式化符与time模块相同
                            filename='{0}\\{1}.log'.format(self.logpath, self.logname),
                            filemode='w'
                            )
        try:
            if ways == 'GET':
                a = sessions.get(url, params=datas)
                if a.status_code == 200:
                    if self.DY(self, json.loads(a.text, encoding='utf-8'), '000000') is False:
                        rsp = json.loads(a.text, encoding='utf-8')
                        log = "接口未成功，报错为:" + str(rsp)
                        logging.error(log)
                        return log
                    else:
                        return a
                else:
                    rsp = json.loads(a.text, encoding='utf-8')
                    log = "报错接口：" + str(url) + "接口信息异常，报错为:" + str(rsp) + "\n"
                    logging.error(log)
                    return log
            elif ways == 'POST':
                a = sessions.post(url=url, data=json.dumps(datas), headers=headers, cookies=cookies)
                if a.status_code == 200:
                    if self.DY(self, json.loads(a.text, encoding='utf-8'), '000000') is False:
                        rsp = json.loads(a.text, encoding='utf-8')
                        log = "接口未成功，报错为:" + str(rsp)
                        logging.error(log)
                        return log
                    else:

                        return a
                else:
                    rsp = json.loads(a.text, encoding='utf-8')
                    log = "报错接口：" + str(url) + "接口信息异常，报错为:" + str(rsp) + "\n"
                    logging.error(log)
                    return log
            else:
                log = '输入请求方式有误，只支持：GET、POST'
                logging.error(log)
        except AttributeError as e:
            log = "未知错误,接口名称为:" + str(url)
            logging.warning(log)
            return log

    # 断言检查
    def DY(self,data,check_point):
        '''

        :param data: 检查对象
        :param check_point:  检查点

        '''
        a = str(data)
        check = str(check_point)
        if a.find(check) != -1:
            return True
        else:
            log = "断言错误，未找到此数据：" + check_point
            logging.warning(log)
            return False



