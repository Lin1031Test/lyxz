import datetime
import os
import time

import requests

# 全局变量
students = []
api_key = "API_KEY"
api_url = "https://sctapi.ftqq.com/"

# 如果检测到程序在 github actions 内运行，那么读取环境变量中的登录信息
if os.environ.get('GITHUB_RUN_ID', None):
    try:
        if not students:
            tmp_students = os.environ.get('students', '').split('\n')
            if "".join(tmp_students) == '':
                students = []
            else:
                students = tmp_students
            del tmp_students
    except:
        print('err: environment config error')


def message(key, title, content, stuID):
    """
    微信通知打卡结果
    """
    long_content = "%s<br>Time: %s<br>SchoolNumber: %s<br>" % (
        content, datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f UTC'), stuID)
    msg_url = "%s%s.send?text=%s&desp=%s" % (api_url, key, title, long_content)
    requests.get(msg_url)


# 实例化session
session = requests.session()


# 登录
def login(stuID, password):
    url = 'https://apii.lynu.edu.cn/v1/accounts/login/'
    data = {
        "username": stuID,
        "password": password,
        "type": ""
    }
    res = session.post(url=url, data=data)
    token = res.json().get('token')
    return token


# 打卡
def report(stuID, password):
    token = login(stuID, password)
    url = 'https://apii.lynu.edu.cn/v1/noons/'
    headers = {
        "Authorization": "JWT " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat"
    }
    data = {
        "condition": "A",
        "value": "36",
    }
    res = session.post(url=url, data=data, headers=headers)
    if res.json():
        return True

def main():
    print('共有 ' + str(len(students)) + ' 人等待打卡')
    for i in range(len(students)):
        list_temp = students[i].split(' ')
        stuID = list_temp[0]
        password = list_temp[1]
        report(stuID, password)
        print(stuID[-3:]+"打卡完成！")
        del (stuID)
        time.sleep(2)
    print("打卡任务全部完成！")


if __name__ == '__main__':
    main()
