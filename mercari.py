from os import curdir
from unicodedata import name
from selenium import webdriver
import chromedriver_binary
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

#キーワード入力
# search_word = input("検索キーワード＝")
search_word = "iphone"

# メルカリ
url =  'https://jp.mercari.com/search?keyword=' + search_word
print(url)

# WebDriver のオプションを設定する
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome()

# 画面サイズ設定
driver.set_window_size(1920,1080)

# 起動
driver.get(url)

time.sleep(5)


def unsold():
    # 販売状況をクリック
    path = '/html/body/div/div[1]/div/div/div/main/div/div[1]/aside/div/div/ul/li[9]'
    driver.find_element_by_xpath(path).click()

    # 販売中のみを選択
    path = '/html/body/div/div[1]/div/div/div/main/div/div[1]/aside/div/div/ul/li[9]/mer-accordion/mer-checkbox-group/mer-checkbox-label[2]/mer-checkbox/input'
    driver.find_element_by_xpath(path).click()

def soldout():
    # 販売状況をクリック
    path = '/html/body/div/div[1]/div/div/div/main/div/div[1]/aside/div/div/ul/li[9]'
    driver.find_element_by_xpath(path).click()

    # 売り切れのみを選択
    path = '/html/body/div/div[1]/div/div/div/main/div/div[1]/aside/div/div/ul/li[9]/mer-accordion/mer-checkbox-group/mer-checkbox-label[3]/mer-checkbox/input'
    driver.find_element_by_xpath(path).click()

soldout()

time.sleep(5)

# カウンタ(表示用)
no = 0
# 外ループ：メルカリの次へボタンが無くなるまで。
while True :

    sellItems = driver.find_elements_by_tag_name("mer-item-thumbnail")
    # 内ループ：ページ内のアイテム情報を取得しきるまで。
    for item in sellItems :
        no += 1
        name = item.get_attribute("item-name")
        price = item.get_attribute("price")
        print(name)
        # print(str(no) + ' : ' + name + ' : \\' + price)

    # 「次へ」ボタンを探して、見つかればクリック
    try:
        # 自動でページ遷移すると画面読み込み時の初期処理に割り込まれてボタン押下が出来ないので、execute_scriptで対策する。
        buttonClick = driver.find_element_by_xpath("//mer-button[@data-testid='pagination-next-button']")
        driver.execute_script("arguments[0].click();",buttonClick)
        time.sleep(3)

    # 「次へ」ボタンが無ければループを抜ける
    except NoSuchElementException:
        break
# 終了処理(ヘッドレスブラウザを閉じる)
driver.quit()