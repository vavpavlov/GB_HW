#Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных
#(от кого, дата отправки, тема письма, текст письма полный)
#Логин тестового ящика: study.ai_172@mail.ru
#Пароль тестового ящика: NewPassword172

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome('/home/vadim/PycharmProjects/selenium/chromedriver', options=options)
driver.get('https://passport.yandex.ru/auth?from=mail&origin=hostroot_homer_auth_L_ru&retpath=https%3A%2F%2Fmail.yandex.ru%2F&backpath=https%3A%2F%2Fmail.yandex.ru%3Fnoretpath%3D1')

elem = driver.find_element_by_id('passp-field-login')
elem.send_keys('wix.555@yandex.ru')
elem.send_keys(Keys.RETURN)

elem = WebDriverWait(driver,10).until(
    EC.visibility_of_element_located((By.ID,'passp-field-passwd'))
)

elem.send_keys('Lancer2005')
elem.send_keys(Keys.RETURN)

result = []
pages_number = 2
i = 0

letters_first_page = WebDriverWait(driver,20).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME,'js-message-snippet'))
    )

while i < pages_number:
    button = driver.find_element_by_class_name('mail-MessagesPager-button')
    if button:
        button.click()
        i += 1
        time.sleep(3)
    else: break

letters_all_pages = WebDriverWait(driver,20).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME,'js-message-snippet'))
    )

for letter in letters_all_pages:
    letter_link = letter.get_attribute('href')

    print(letter_link)


#driver.quit()