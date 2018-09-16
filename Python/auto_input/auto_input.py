from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import xlrd
from PIL import Image
import pytesseract
import requests
import re

'''
用途：自动填写账号密码，并进行一定操作
使用库：selenium，xlrd，Pillow，pytesseract
流程：使用xlrd读取xlsx文件中的账号，并自动填写账号密码，截取浏览器窗口，
     截取窗口中的验证码图片，并进行识别填写，然后进行自动化操作。
'''

# browser = webdriver.Chrome()
# browser.get('http://mis.cbern.com.cn/base/login.jsp')
#
# user_name = browser.find_element_by_id('loginName')
# password = browser.find_element_by_id('password')
# verify_code = browser.find_element_by_id('rand')
# button = browser.find_element_by_id('loginBtn')
# user_name.send_keys('9440306364258')
# password.send_keys('lhxq123456')
# code_input = input('verify_code:')
# verify_code.send_keys(code_input)
# button.click()
# wait = WebDriverWait(browser,1000)
# wait.until(EC.presence_of_element_located((By.ID,'menu_index')))
#
# confirm_btn = browser.find_element_by_class_name('sj1')
# confirm_btn.click()
# a = browser.switch_to_alert()
# print(a)
# # a.accept()
# a.dismiss()
# exit_btn = browser.find_element_by_class_name('tc1')
# exit_btn.click()


# 识别验证码
def recognize(imgName):
    im = Image.open(imgName)

    # im = Image.open(io.BytesIO(b))
    # 转化到灰度图
    imgry = im.convert('L')
    # 保存图像
    imgry.save('gray-' + imgName)
    # 二值化，采用阈值分割法，threshold为分割点
    threshold = 140
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    out.save('b' + imgName)
    # 识别
    text = pytesseract.image_to_string(out)
    # print("识别结果："+text)
    return text


# def get_image():
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
#     }
#     r = requests.get('http://mis.cbern.com.cn/base/login.jsp', headers=headers)
#     html = r.text
#     pattern = re.compile('<tr>.*?src="(.*?)" onclick.*?</tr>', re.S)
#     src = re.findall(pattern, html)
#     image_url = 'http://mis.cbern.com.cn' + src[0]
#     r = requests.get(image_url, headers=headers)
#     with open('image.gif', 'wb') as f:
#         f.write(r.content)


def get_info():
    # 打开excel文件
    workbook = xlrd.open_workbook('username.xlsx')
    # 读取sheet1表格
    sheet = workbook.sheet_by_index(0)
    # 读取表格中的第一列数据
    cols = sheet.col_values(0)
    # 将该数据以列表形式返回
    return cols


# def save_image(image_url):
#     r = requests.get(image_url)
#     with open('image.gif', 'wb') as f:
#         f.write(r.content)


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
    result.save('image.gif')
    # 使用recognize进行识别
    code_input = recognize('image.gif')
    user_name = browser.find_element_by_id('loginName')
    password = browser.find_element_by_id('password')
    verify_code = browser.find_element_by_id('rand')
    button = browser.find_element_by_id('loginBtn')
    user_name.send_keys(username)
    password.send_keys('lhxq123456')
    # code_input = input('verify_code:')
    verify_code.send_keys(code_input)
    button.click()
    wait = WebDriverWait(browser, 1000)
    wait.until(EC.presence_of_element_located((By.ID, 'menu_index')))


def confirm_message(browser):
    confirm_btn = browser.find_element_by_class_name('sj1')
    confirm_btn.click()
    a = browser.switch_to_alert()
    # 确认
    # a.accept()
    # 取消
    a.dismiss()


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
