from selenium import  webdriver
import time,datetime,sys,requests
from PIL import Image
import threading
web=webdriver.Firefox()
web.maximize_window()
web.get('http://zqb.red.xunlei.com/html/grabcode.html')#http://zqb.red.xunlei.com/html/grabcode.html
# time.sleep(100)
web.find_element_by_class_name("input").send_keys("17865667221")#input input-short    input-send
web.find_element_by_class_name("input-send").click()


web.save_screenshot('aa.png')
rangle=(int(1016),int(480),int(1163),int(545))
i=Image.open("aa.png")
frame4=i.crop(rangle)
frame4.save('frame4.png')

web.find_element_by_class_name("input-box2").find_element_by_tag_name("input").send_keys(input("图片验证码："))
time.sleep(2)
web.find_element_by_link_text("确定").click()
web.find_element_by_class_name("input-short").send_keys(input("验证码："))
time.sleep(1)
try:
    web.find_element_by_link_text("立即预约").click()
except Exception as e:
    web.find_element_by_link_text("立即登录").click()
def click_but():
    while True:
        print("------")
        web.refresh()
        web.find_element_by_link_text("立即抢码").click()
def now_time():
    hour =datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    seconds= datetime.datetime.now().second
    if  hour == 10 and  minute==40 and seconds == 0:
        return True
    return  True
while True:
    if now_time():
        #print("True")
        threads = []
        while True :
            print(len(threads))
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)
            while len(threads) < 3 :
                thread = threading.Thread(target=click_but)
                thread.setDaemon(True)
                thread.start()
                threads.append(thread)
        # while True:
        #     click_but()
        #     # try:
        #     #     if web.find_element_by_link_text("立即抢码"):
        #     #         web.find_element_by_link_text("立即抢码").click()
        #     # except Exception as e:
        #     #     sys.exit()
    time.sleep(0.5)
