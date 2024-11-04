from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 手动指定 chromedriver 路径
chrome_driver_path = 'C:\Program Files (x86)\chromedriver-win64/chromedriver.exe'  # 将路径替换为你自己的 chromedriver 路径
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# 测试打开一个页面
driver.get('https://www.jd.com')
