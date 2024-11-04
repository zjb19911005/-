from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 手动指定 chromedriver 路径
chrome_driver_path = 'C:\Program Files (x86)\chromedriver-win64/chromedriver.exe'  # 将路径替换为你自己的 chromedriver 路径
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)


# 登录京东账户
def login_jd():
    driver.get('https://passport.jd.com/new/login.aspx')

    # 等待用户手动扫码登录
    print("请手动扫码登录京东账号...")
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, 'nickname')))
    print("登录成功！")


# 搜索商品并添加到购物车
def search_and_add_to_cart(product_name):
    # 搜索商品
    search_box = driver.find_element(By.ID, 'key')
    search_box.send_keys(product_name)
    search_box.submit()

    # 等待搜索结果加载
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'gl-item')))

    # 点击第一个商品的购买链接
    first_product = driver.find_element(By.CSS_SELECTOR, 'li.gl-item div.p-name a')
    first_product.click()

    # 切换到新标签页
    driver.switch_to.window(driver.window_handles[-1])

    # 点击添加到购物车按钮
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'InitCartUrl')))
    add_to_cart_btn = driver.find_element(By.ID, 'InitCartUrl')
    add_to_cart_btn.click()

    print(f"商品 {product_name} 已加入购物车")


# 批量添加收货地址
def add_shipping_address(address_list):
    for address in address_list:
        # 打开购物车
        driver.get('https://cart.jd.com/cart')

        # 点击去结算
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.common-submit-btn')))
        checkout_btn = driver.find_element(By.CSS_SELECTOR, '.common-submit-btn')
        checkout_btn.click()

        # 选择收货地址并输入地址信息
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, '新增收货地址')))
        add_address_btn = driver.find_element(By.LINK_TEXT, '新增收货地址')
        add_address_btn.click()

        # 输入地址信息
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'consigneeName')))
        driver.find_element(By.ID, 'consigneeName').send_keys(address['name'])
        driver.find_element(By.ID, 'consigneeAddress').send_keys(address['address'])
        driver.find_element(By.ID, 'consigneeMobile').send_keys(address['phone'])
        # 其他地址字段的填写

        # 保存地址
        driver.find_element(By.CLASS_NAME, 'saveConsigneeBtn').click()

        print(f"已添加地址：{address['name']}, {address['address']}, {address['phone']}")


# 选择对公转账作为付款方式
def choose_payment_method():
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'payment-method')))
    payment_methods = driver.find_elements(By.CLASS_NAME, 'payment-method')

    for method in payment_methods:
        if '对公转账' in method.text:
            method.click()
            print("已选择对公转账")
            break


# 提交订单
def submit_order():
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'checkout-submit')))
    submit_btn = driver.find_element(By.CLASS_NAME, 'checkout-submit')
    submit_btn.click()
    print("订单已提交")


# 运行批量下单工具
def run_batch_order(product_name, address_list):
    login_jd()
    search_and_add_to_cart(product_name)
    add_shipping_address(address_list)
    choose_payment_method()
    submit_order()


# 示例地址列表
address_list = [
    {'name': '张三', 'address': '北京市海淀区中关村1号', 'phone': '13800000001'},
    {'name': '李四', 'address': '上海市浦东新区陆家嘴2号', 'phone': '13800000002'},
    {'name': '王五', 'address': '广州市天河区3号', 'phone': '13800000003'}
]

# 执行批量下单操作
product_name = "iPhone 14 Pro"  # 你要购买的商品
run_batch_order(product_name, address_list)

# 关闭浏览器
driver.quit()
