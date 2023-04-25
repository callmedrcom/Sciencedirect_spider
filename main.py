import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from download_url import download_url
from sciencedirect_search import savepdf, savebyprint, typename
import time,win32con,win32api
import pandas as pd
import json

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
    options.add_argument('headless')
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

option = input('Please select your option: \n 1. Searching papers with key words \n 2. Downloading papers with '
               'key words')
keywords = input('Please input your key words: ').split(' ')
url = "https://www.sciencedirect.com/search?"
url += 'qs=' + keywords[0]
for i in range(1, len(keywords)):
    url += r'%20'+ keywords[i]

url += '&show=100'
print('opening url:',url)
wd = getDriver()
if option == '1':
    dict_name_url = []
    num = int(input('And the number of paper you want to download information：'))
    time.sleep(5)
    for i in range(num):
        wd.get(url)
        time.sleep(2)
        js1 = "window.scrollTo(0, document.body.scrollHeight)"
        wd.execute_script(js1)
        titles = wd.find_elements(By.XPATH, '//*[contains(@id, "title-")]/span/span')
        print(titles[i].text)
        title_temp = titles[i].text
        titles[i].click()  # 点击标题,打开文章页面
        dict_name_url.append(download_url(wd.current_url)) # 保存文章标题和url
        pd.DataFrame(dict_name_url).to_csv('dict_name_url.csv', index=False)

elif option =='2':
    num = int(input('And the number of paper you want to download：'))
    wd.get(url)
    time.sleep(10)
    js1 = "window.scrollTo(0, document.body.scrollHeight)"
    wd.execute_script(js1)
    titles = wd.find_elements(By.XPATH, '//*[contains(@id, "title-")]/span/span')

    print(titles[i].text)
    title_temp = titles[i].text
    titles[i].click()   # 点击标题,打开文章页面
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
