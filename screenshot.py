from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import time
import os.path
 
# 配置驱动路径
DRIVER_PATH = '/your/chromedriver/path'
 
if __name__ == "__main__":
    # 设置浏览器
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # 无头参数
    options.add_argument('--disable-gpu')
    # 启动浏览器
    driver = Chrome(executable_path=DRIVER_PATH, options=options)
    driver.maximize_window()
 
    try:
        # 配置你的和风天气H5界面的url
        url = 'https://your/hefeng/weather/url'
        driver.get(url)
        time.sleep(3)
 
        # 设置截屏整个网页的宽度以及高度
        scroll_width = 300
        scroll_height = 700
        driver.set_window_size(scroll_width, scroll_height)
 
        # 保存图片，自定义图片命名和路径，注意：发送邮件时需要用到
        img_name = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取今天的日期
        img = '/user/weather/' + img_name + '.png'
        driver.get_screenshot_as_file(img)
 
        # 关闭浏览器
        driver.close()
        driver.quit()
 
    except Exception as e:
        print(e)
