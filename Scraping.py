# ※注意※
# 以下の利用規約を熟読した上で、本プログラムの利用は自己責任でお願いします。
# 利用規約　OpenWork（旧:Vorkers）
# https://www.vorkers.com/rule.php

import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# -------------------- 定数 -------------------- #
LOGIN_USER = "**********"
LOGIN_PASS = "**********"

company_ids = ["a0910000000G7Hz", "a0910000000GWbg", "a0C1000000s3emK", "a0910000000GW8O", "a0910000000GVqH"]
# https://www.vorkers.com/company_answer.php?m_id=xxxxxxxxxxxxxxx
#   a0910000000G7Hz グーグル合同会社
#   a0910000000GWbg アマゾンジャパン合同会社
#   a0C1000000s3emK Facebook Japan株式会社
#   a0910000000GW8O Apple Japan合同会社
#   a0910000000GVqH 日本マイクロソフト株式会社

kuchikomi_ids = [1, 2, 3, 4, 5, 6, 8, 9, 10]
# https://www.vorkers.com/company_answer.php?m_id=xxxxxxxxxxxxxxx&q_no=y
#   1   組織体制・企業文化
#   2   年収・給与制度
#   3   入社理由と入社後ギャップ
#   4   働きがい・成長
#   5   女性の働きやすさ
#   6   ワーク・ライフ・バランス
#   7   -
#   8   退職検討理由
#   9   企業分析［強み・弱み・展望］
#   10  経営者への提言

now = datetime.datetime.now()
# OUTPUT_CSV_FILEPATH = now.strftime("./%Y%m%d-%H%M.csv")
OUTPUT_CSV_FILEPATH = "./scraping.csv"

DRIVER_PATH = './chromedriver'
BASE_URL = "https://www.vorkers.com/"

SLEEP_TIME = 5
# --------------------------------------------- #

# top page * headless mode ではありません
driver = webdriver.Chrome(executable_path = DRIVER_PATH)
driver.get(BASE_URL)
time.sleep(SLEEP_TIME)

# login page
driver.find_element_by_xpath('//*[@id="headerMenu"]/li[2]/a').click()
time.sleep(SLEEP_TIME)

# login
user_box = driver.find_element_by_xpath('//*[@id="_username"]')
pass_box = driver.find_element_by_xpath('//*[@id="_password"]')
user_box.send_keys(LOGIN_USER)
pass_box.send_keys(LOGIN_PASS)
driver.find_element_by_xpath('//*[@id="log_in"]').click()
time.sleep(SLEEP_TIME)

# scraping
for company_id in company_ids:
    for kuchikomi_id in kuchikomi_ids:
        kuchikomi_start_url = BASE_URL + "company_answer.php?m_id=" + company_id + "&q_no=" + str(kuchikomi_id)

        page = 1
        while True:
            kuchikomi_now_url = kuchikomi_start_url + "&next_page=" + str(page)
            driver.get(kuchikomi_now_url)
            time.sleep(SLEEP_TIME)

            ######### エラー処理 #########
            # 最終ページ＋1ページ目は1ページ目に戻ってくる
            if driver.current_url == kuchikomi_start_url and page != 1:
                break

            # 1ページしかない場合は、2ページ目はエラー
            elif driver.title == "404エラー　File not found　OpenWork":
                break
            ###########################

            ##### スクレイピング処理 #####
            print("[---------- " + driver.title + " ----------]")
            # articleは1ページ最大25件
            for i in range(1, 26):
                print("[ article " + str(i) + " ]")

                # 1. 回答日（2018年05月17日）
                answer_time_xpath  = '//*[@id="anchor01"]/article[' + str(i) + ']/div[1]/p/time'
                # 2. 回答者属性（SE、在籍3年未満、現職（回答時）、新卒入社、男性、xxx）
                answer_type_xpath  = '//*[@id="anchor01"]/article[' + str(i) + ']/div[2]/dl/dt/a'
                # 3. 点数（2.4）
                answer_score_xpath = '//*[@id="anchor01"]/article[' + str(i) + ']/div[2]/dl/dt/span[2]/span[6]'
                # 4. 本文
                answer_body_xpath  = '//*[@id="anchor01"]/article[' + str(i) + ']/div[2]/dl/dd'

                try:
                    answer_time_text  = driver.find_element_by_xpath(answer_time_xpath).text
                    answer_type_text  = driver.find_element_by_xpath(answer_type_xpath).text
                    answer_score_text = driver.find_element_by_xpath(answer_score_xpath).text
                    answer_body_text  = driver.find_element_by_xpath(answer_body_xpath).text
                # articleが25件未満
                except Exception:
                # except selenium.common.exceptions.NoSuchElementException:
                    break

                tmp_str = company_id             + "\t"  \
                        + str(kuchikomi_id)      + "\t"  \
                        + answer_time_text       + "\t"  \
                        + answer_type_text       + "\t"  \
                        + str(answer_score_text) + '\t"' \
                        + answer_body_text       + '"\n'
                with open(OUTPUT_CSV_FILEPATH, mode='a') as f:
                    f.write(tmp_str)
            ###########################

            page += 1
driver.quit()
