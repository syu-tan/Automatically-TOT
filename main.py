import argparse
import time

import yaml
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class TOTController(object):

    # chrome option
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu');
    options.add_argument('--disable-extensions');
    options.add_argument('--proxy-server="direct://"');
    options.add_argument('--proxy-bypass-list=*');
    options.add_argument('--start-maximized');
    options.add_argument('--kiosk') # 全画面

    def __init__(self,path_config, watch):
        
        # 設定ファイル読み込み
        with open(path_config) as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)

        self.DRIVER_PATH = str(cfg['chromedriver'])
        self.ID = cfg['ID']
        self.PASSWORD = cfg['PASSWORD']

        # 画面表示する場合の処理
        if not watch:
            self.options.add_argument('--headless') # 画面表示

        # ブラウザの起動
        self.driver = webdriver.Chrome(executable_path=self.DRIVER_PATH, options=self.options)

    def login(self):
        # Webページにアクセスする
        url = 'https://touchontime.com/independent/recorder/personal/'
        self.driver.get(url)

        selector = '#id'
        element = self.driver.find_element_by_css_selector(selector)

        # テキストを入力する
        element.send_keys(self.ID)


        selector = '#password'
        element = self.driver.find_element_by_css_selector(selector)
        # テキストを入力する
        element.send_keys(self.PASSWORD)


        # 要素をクリックする
        selector = '#modal_window > div > div > div.btn-control-outer.btn-control-outer-size-short.align-right > div > div'
        element = self.driver.find_element_by_css_selector(selector)
        element.click()

        # 位置情報や読み込みのため
        time.sleep(5)

    def go_to_work(self):
        # 出勤
        selector = '#record_qmXXCxw9WEWN3X\/YrkMWuQ\=\= > div'
        element = self.driver.find_element_by_css_selector(selector)
        element.click()

    def leave_work(self):
        # 退勤
        selector = '#record_j8ekmJaw6W3M4w3i6hlSIQ\=\= > div'
        element = self.driver.find_element_by_css_selector(selector)
        element.click()

    def finish(self):
        # ブラウザ終了
        self.driver.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='出勤と退勤や、ファイルの設定')
    parser.add_argument('-i', '--go_to_work', help='出勤する', action='store_true')
    parser.add_argument('-o', '--leave_work', help='退勤する', action='store_true')
    parser.add_argument('-w', '--watch_screen', help='画面を見る', action='store_true')
    parser.add_argument('-p', '--path_config', help='設定ファイルへのパス', type=str, default='config.yaml')
    args = parser.parse_args()

    # 基本処理
    totc = TOTController(args.path_config, args.watch_screen)
    totc.login()

    if args.go_to_work:
        totc.go_to_work()
        print('今日も一日がんばろお！')
    if args.leave_work:
        totc.leave_work()
        print('お疲れ様でした。')

    totc.finish()
    print('==>> done <<==')





