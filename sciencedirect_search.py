import pandas as pd
import random
import time,win32con,win32api

from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver import ActionChains





# -*- coding: UTF8 -*-
import json
from selenium import webdriver


def typename(name):
    globaldelay = 0.02
    dict_alphabet = {'A': 65, 'B': 66, 'C': 67, 'D': 68, 'E': 69, 'F': 70, 'G': 71, 'H': 72, 'I': 73, 'J': 74, 'K': 75, 'L': 76, 'M': 77, 'N': 78, 'O': 79, 'P': 80, 'Q': 81, 'R': 82, 'S': 83, 'T': 84, 'U': 85, 'V': 86, 'W': 87, 'X': 88, 'Y': 89, 'Z': 90, '-': 109,
                     'a': 65, 'b': 66, 'c': 67, 'd': 68, 'e': 69, 'f': 70, 'g': 71, 'h': 72, 'i': 73, 'j': 74, 'k': 75, 'l': 76, 'm': 77, 'n': 78, 'o': 79, 'p': 80, 'q': 81, 'r': 82, 's': 83, 't': 84, 'u': 85, 'v': 86, 'w': 87, 'x': 88, 'y': 89, 'z': 90, ' ': 32}
    for capi in name:
        if capi.isupper():  # 如果是大写字母
            win32api.keybd_event(20, 0, 0, 0) # 按下capslock
            win32api.keybd_event(20, 0, win32con.KEYEVENTF_KEYUP, 0) # 释放capslock
            win32api.keybd_event(dict_alphabet[capi], 0, 0, 0) # 按下字母
            time.sleep(globaldelay) # 模拟输入延迟
            win32api.keybd_event(dict_alphabet[capi], 0, win32con.KEYEVENTF_KEYUP, 0) # 释放字母
            time.sleep(globaldelay) # 模拟输入延迟
            win32api.keybd_event(20, 0, 0, 0) # 按下capslock--关闭大写
            win32api.keybd_event(20, 0, win32con.KEYEVENTF_KEYUP, 0) # 释放capslock--关闭大写
        elif capi.islower():   # 如果是小写字母
            win32api.keybd_event(dict_alphabet[capi], 0, 0, 0)
            time.sleep(globaldelay)
            win32api.keybd_event(dict_alphabet[capi], 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(globaldelay)
        else:   # 如果是其他字符，直接敲空格
            win32api.keybd_event(32, 0, 0, 0) # space
            win32api.keybd_event(32, 0, win32con.KEYEVENTF_KEYUP, 0) # space

def pagedown(num):
    for i in range(num):
        win32api.keybd_event(34, 0, 0, 0) # page down
        win32api.keybd_event(34, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.5)
def pageend(num):
    for i in range(num):
        win32api.keybd_event(35, 0, 0, 0) # end
        win32api.keybd_event(35, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.5)

def savepdf():
    win32api.keybd_event(17, 0, 0, 0) # ctrl
    win32api.keybd_event(83, 0, 0, 0) # s
    win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

def savebyprint():
    win32api.keybd_event(17, 0, 0, 0) # ctrl
    win32api.keybd_event(80, 0, 0, 0) # p
    win32api.keybd_event(80, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
def getDriver():
    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "isHeaderFooterEnabled": False,
        "isCssBackgroundEnabled": True,
        "mediaSize": {
            "height_microns": 297000,
            "name": "ISO_A4",
            "width_microns": 210000,
            "custom_display_name": "A4"
        },
    }
    options = webdriver.EdgeOptions()
    options.add_argument('--enable-print-browser')
    options.add_argument('--headless')  # headless模式下，浏览器窗口不可见，可提高效率
    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        'savefile.default_directory': 'C:\\Users\\admin\\Desktop'  # 此处填写你希望文件保存的路径,可填写your file path默认下载地址
    }

    options.add_argument('--kiosk-printing')  # 静默打印，无需用户点击打印页面的确定按钮
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option('prefs', prefs)
    edge_path = Service(r"msedgedriver.exe")  # 相对路径下
    driver = webdriver.Edge(service=edge_path)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
             Object.defineProperty(navigator, 'webdriver', {
                 get: () => undefined
             })
         """
    })
    driver.maximize_window()
    return driver


url = "https://www.sciencedirect.com/search?"
keywords = input('请输入关键词Please input your key words：').split(' ')
num = int(input('请输入想要下载的文章数量And the number of paper you want to download：'))
url += 'qs=' + keywords[0]
for i in range(1, len(keywords)):
    url += r'%20'+ keywords[i]

url += '&show=100'
print(url)

wd = getDriver()

dict_name_url = []

for i in range(num):

    wd.get(url)
    time.sleep(10)
    js1 = "window.scrollTo(0, document.body.scrollHeight)"
    wd.execute_script(js1)
    titles = wd.find_elements(By.XPATH, '//*[contains(@id, "title-")]/span/span')

    print(titles[i].text)
    title_temp = titles[i].text
    titles[i].click()   # 点击标题,打开文章页面
    dict_name_url.append([title_temp, wd.current_url])
    time.sleep(random.randint(5, 10)) # 等待页面加载
    button = wd.find_element(By.XPATH, '//*[@id="mathjax-container"]/div[1]/div/div[2]/ul/li[1]/a')
    button.click()   # 点击view
    try:
        time.sleep(10) # 等待页面加载
        savepdf()   # 打印  switch to savebyprint() if you want to save by print
        time.sleep(1)
        typename(title_temp)
        win32api.keybd_event(13, 0, 0, 0) # enter
        win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(random.randint(5, 10)) # 等待另存为完成
    except:
        print('下载失败 download failed')

time.sleep(20)
pd.DataFrame(dict_name_url).to_csv('name_url.csv', index=False, header=False)
wd.quit()


