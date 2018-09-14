from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import xlrd

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

def get_info():
    workbook = xlrd.open_workbook('username.xlsx')
    sheet = workbook.sheet_by_index(0)
    cols = sheet.col_values(0)
    return cols


def input_info(browser,username):
    user_name = browser.find_element_by_id('loginName')
    password = browser.find_element_by_id('password')
    verify_code = browser.find_element_by_id('rand')
    button = browser.find_element_by_id('loginBtn')
    user_name.send_keys(username)
    password.send_keys('lhxq123456')
    code_input = input('verify_code:')
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


def exit(browser):
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
    for i in  info_list:
        input_info(browser,i)
        confirm_message(browser)
        exit(browser)

if __name__ == '__main__':
    main()

