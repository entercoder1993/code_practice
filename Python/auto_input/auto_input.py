import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import xlrd
from PIL import Image
from aip import AipOcr

'''
用途：自动填写账号密码，并进行一定操作
使用库：selenium，xlrd，Pillow，baidu-aip
流程：使用xlrd读取xlsx文件中的账号，并自动填写账号密码，截取浏览器窗口，
     截取窗口中的验证码图片，并进行识别填写，然后进行自动化操作。
'''

# 填写你的 APPID AK SK
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


# 使用百度识别验证码
def recognize2(imageName):
    with open(imageName,'rb') as f:
        image = f.read()
        result = client.numbers(image)
        return result['words_result'][0]['words']


def get_info():
    # 打开excel文件
    workbook = xlrd.open_workbook('username.xls')
    # 读取sheet1表格
    sheet = workbook.sheet_by_index(0)
    # 读取表格中的第一列数据
    cols = sheet.col_values(0)
    # 将该数据以列表形式返回
    return cols


def input_info(browser, username):
    # 截取当前网页
    browser.save_screenshot('screen.png')
    # image = browser.find_element_by_id('authimage')
    # 通过image.size和image.location获取数据height:20,width:60 {'x': 822, 'y': 265}
    # rangle = (x,y,x+width,y+height)
    rangle = (822, 265, 882, 285)
    # 打开截取的网页
    i = Image.open('screen.png')
    # 使用Image的crop函数，从截图中再次截取我们需要的区域
    result = i.crop(rangle)
    # 将文件保存为image.gif文件
    result.save('image.png')
    # 使用recognize进行识别
    code_input = recognize2('image.png')
    user_name = browser.find_element_by_id('loginName')
    password = browser.find_element_by_id('password')
    verify_code = browser.find_element_by_id('rand')
    button = browser.find_element_by_id('loginBtn')
    user_name.send_keys(username)
    password.send_keys('123456')
    # code_input = input('verify_code:')
    verify_code.send_keys(code_input)
    button.click()
    wait = WebDriverWait(browser, 1000)
    wait.until(EC.presence_of_element_located((By.ID, 'menu_index')))


# 点击确认
def confirm_message(browser):
    # 等待sj1加载完成，否则可能会出错
    time.sleep(0.5)
    confirm_btn = browser.find_element_by_class_name('sj1')
    confirm_btn.click()
    a = browser.switch_to_alert()
    # 确认
    # a.accept()
    # 取消
    a.dismiss()


# 退出登陆
def exit_browser(browser):
    exit_btn = browser.find_element_by_class_name('tc1')
    exit_btn.click()


def main():
    # 使用
    # option = webdriver.ChromeOptions()
    # option.add_argument('--headless')
    # browser = webdriver.Chrome(options=option)
    browser = webdriver.Chrome()
    browser.get('http://mis.cbern.com.cn/base/login.jsp')
    # 用户名列表
    info_list = get_info()
    for i in info_list:
        input_info(browser, i)
        confirm_message(browser)
        exit_browser(browser)


if __name__ == '__main__':
    main()
