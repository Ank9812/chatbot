# coding=utf-8


import time
# import json
import platform
import os
# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import itchat
from itchat.content import (
    TEXT
)

from everyday_wechat.utils.data_collection import (
    get_weather_info,
    get_dictum_info,
    get_diff_time,
    get_calendar_info,
    get_constellation_info
)
from everyday_wechat.control.airquality.air_quality_aqicn import (
    get_air_quality
)
from everyday_wechat.utils import config
from everyday_wechat.utils.itchat_helper import (
    init_wechat_config,
    set_system_notice,
)
from everyday_wechat.utils.group_helper import (
    handle_group_helper
)
from everyday_wechat.utils.friend_helper import (
    handle_friend
)

__all__ = ['run', 'delete_cache']


def run():
   
    print('run')
    if not is_online(auto_login=True):
        print('is online.')
        return


def is_online(auto_login=False):
   

    def _online():
        
        try:
            if itchat.search_friends():
                return True
        except IndexError:
            return False
        return True

    if _online(): return True  
    if not auto_login:  
        print('hai .')
        return False

    # hotReload = not
    loginCallback = init_data
    exitCallback = exit_msg
    try:
        for _ in range(2):  # 尝试登录 2 次。
            if platform.system() in ('Windows', 'Darwin'):
                itchat.auto_login(hotReload=hotReload,
                                  loginCallback=loginCallback, exitCallback=exitCallback)
                itchat.run(blockThread=True)
            else:
                # 命令行显示登录二维码。
                itchat.auto_login(enableCmdQR=2, hotReload=hotReload, loginCallback=loginCallback,
                                  exitCallback=exitCallback)
                itchat.run(blockThread=True)
            if _online():
                print('sahi h')
                return True
    except Exception as exception: 
        sex = str(exception)
        if sex == "'User'":
            print('ye nhi ho paya')
        else:
            print(sex)

    delete_cache()  
    print('deleted。')
    return False


def delete_cache():
    
    file_names = ('QR.png', 'itchat.pkl')
    for file_name in file_names:
        if os.path.exists(file_name):
            os.remove(file_name)


def init_data():
    
    set_system_notice('notice')
    itchat.get_friends(update=True)  
    itchat.get_chatrooms(update=True) 

    init_wechat_config()

   
    alarm_dict = config.get('alarm_info').get('alarm_dict')
    if alarm_dict:
        init_alarm(alarm_dict)
        print('ye yhaa h na。')


def init_alarm(alarm_dict):
    """
    
    scheduler = BackgroundScheduler()
    for key, value in alarm_dict.items():
        scheduler.add_job(send_alarm_msg, 'cron', [key], hour=value['hour'],
                          minute=value['minute'], id=key, misfire_grace_time=600, jitter=value.get("alarm_jitter",0))
    scheduler.start()


def send_alarm_msg(key):
    
    print('\n alaem')
    conf = config.get('alarm_info').get('alarm_dict')

    gf = conf.get(key)
    # print(gf)air_quality_city
    is_tomorrow = gf.get('is_tomorrow', False)
    calendar_info = get_calendar_info(gf.get('calendar'), is_tomorrow)
    weather = get_weather_info(gf.get('city_name'), is_tomorrow)
    horoscope = get_constellation_info(gf.get("horescope"), is_tomorrow)
    dictum = get_dictum_info(gf.get('dictum_channel'))
    diff_time = get_diff_time(gf.get('start_date'), gf.get('start_date_msg'))
    air_quality = get_air_quality(gf.get('air_quality_city'))

    sweet_words = gf.get('sweet_words')
    send_msg = '\n'.join(
        x for x in [calendar_info, weather, air_quality, horoscope, dictum, diff_time, sweet_words] if x)
    # print('\n' + send_msg + '\n')
    if not send_msg or not is_online(): return
    uuid_list = gf.get('uuid_list')
    for uuid in uuid_list:
        time.sleep(1)
        itchat.send(send_msg, toUserName=uuid)
    print('hey tehte\n\n'.format(send_msg))
    print('kaise ho aap.\n')


@itchat.msg_register([TEXT])
def text_reply(msg):
    
    handle_friend(msg)
   

@itchat.msg_register([TEXT], isGroupChat=True)
def text_group(msg):
    
    handle_group_helper(msg)


def exit_msg():
    
    print('bye')


if __name__ == '__main__':
    # run()
    pass
    # config.init()
    # init_wechat()
