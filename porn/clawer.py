import shutil
import threading
import time
import urllib

import requests as requests
from seleniumwire import webdriver
# from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

save_path = "G:\hammer\Pictures\Download"


def get_img_path_from_url(url: str):
    # url 转 path
    # 按/拆分取最后
    arr = url.split('/')
    img_name = arr[len(arr) - 1]
    print(f"图片名:{img_name}")
    return f'{save_path}\{img_name}'


def response_interceptor(request, response):
    t = response.headers['Content-Type']
    print(request.host)
    print(t)
    if t is None:
        return
    if 'image' in t or 'image/jpeg' in t or 'image/png' in t:
        with open(get_img_path_from_url(request.url), 'wb') as f:
            f.write(response.body)


if __name__ == '__main__':
    """
    如何保存图片路径
    """
    __metamask_path = "F:\chrome\metamask-chrome-10.17.0"
    __chromedriver_path = "F:\chrome\chromedriver.exe"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.page_load_strategy = 'eager'
    # chrome_options.add_argument('--headless')  # 设置无头浏览器请求模式
    chrome_options.add_argument("--disable-gpu")
    # 不加载图片, 提升速度
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--proxy-server=http://127.0.0.1:10809") # 设置代理，请求头等，以列表的形式传入多个参数
    # seleniumwire 配置二级代理
    wire_option = {
        'proxy': {
            'http': 'http://127.0.0.1:10809',
            'https': 'https://127.0.0.1:10809',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }
    chrome_driver = webdriver.Chrome(seleniumwire_options=wire_option,
                                     executable_path=__chromedriver_path,
                                     options=chrome_options)
    chrome_driver.response_interceptor = response_interceptor
    url = "https://t1222.91p01.app/viewthread.php?tid=534431"
    url = "https://99zipai.com/selfies/202302/152407.html"
    chrome_driver.get(url)

    # src = chrome_driver.find_element_by_tag_name('img').get_attribute('src')
    # img_path = get_img_path_from_url(src)
    # print(img_path)
    time.sleep(5)
    # imgs = chrome_driver.find_elements(by=By.XPATH, value='//img')
    # for i in imgs:
    #     if i.get_attribute("src"):
    #         # print(i.get_attribute("src"))
    #         url = i.get_attribute("src")
    #         arr = url.split('/')
    #         img_name = arr[len(arr) - 1]
    #         if len(img_name.split(".")[0] ) < 20:
    #             continue
    #         print(f"图片名:{img_name}")
    #         file =  f'{save_path}\{img_name}'
    #         r = requests.get(url, stream=True)
    #         if r.status_code == 200:
    #             with open(file, 'wb') as f:
    #                 r.raw.decode_content = True
    #                 shutil.copyfileobj(r.raw, f)
