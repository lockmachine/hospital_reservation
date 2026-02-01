#! /usr/bin/env python3
#-*- coding: utf-8 -*-
import os
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import schedule
import time
import datetime
import sys

# "person_data.env" を指定する
env_path = Path(__file__).parent / 'person_data.env'

# 同じフォルダにある.envファイルから環境変数を読み込む
load_dotenv(dotenv_path=env_path)

# 環境変数から設定を取得
HOSPITAL_URL = os.getenv("HOSPITAL_URL")
E_ID = os.getenv("E_ID")
E_BIRTH = os.getenv("E_BIRTH")
E_NAME = os.getenv("E_NAME")  # 名前を環境変数から取得
T_ID = os.getenv("T_ID")
T_BIRTH = os.getenv("T_BIRTH")
T_NAME = os.getenv("T_NAME")  # 名前を環境変数から取得

def hospital_reservation(driver, id1, birth1, id2, birth2, num_of_patients):
    driver.refresh()
    try:
        accept_button = driver.find_element(By.LINK_TEXT, "受付する")
        accept_button.click()
    except NoSuchElementException:
        print(f"受付前 : {datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
        return True
    
    print("受付中！！！！！")

    # 1人目の入力
    driver.find_element(By.ID, "id1").send_keys(id1)
    driver.find_element(By.ID, "birth1").send_keys(birth1)
    
    select_element = driver.find_element(By.NAME, "dnum")
    Select(select_element).select_by_value(str(num_of_patients))
    driver.find_element(By.NAME, "submit1").click()
    
    # 2人目の入力
    if num_of_patients == 2:
        driver.find_element(By.ID, "id2").send_keys(id2)
        driver.find_element(By.ID, "birth2").send_keys(birth2)
        driver.find_element(By.NAME, "submit1").click()

    # 確認画面
    driver.find_element(By.LINK_TEXT, "はい").click()

    # 「その他」チェック
    other_checkbox = driver.find_element(By.XPATH, "//input[@id='kid1_19']")
    driver.execute_script("arguments[0].click();", other_checkbox)
    
    if num_of_patients == 2:
        other_checkbox2 = driver.find_element(By.XPATH, "//input[@id='kid2_19']")
        driver.execute_script("arguments[0].click();", other_checkbox2)

    driver.find_element(By.NAME, "submit1").click()
 
    print("予約完了！！！！")
    time.sleep(10)
    driver.quit()
    return False

def job(id1, birth1, id2, birth2, num_of_patients):
    options = webdriver.ChromeOptions()
    # バージョン互換性の設定
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.page_load_strategy = 'normal'
    
    try:
        # webdriver-managerでchromedriverを自動ダウンロード・管理
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Chromeドライバーのエラー: {e}")
        return
    driver.get(HOSPITAL_URL)

    ret_val = True
    while ret_val:
        ret_val = hospital_reservation(driver, id1, birth1, id2, birth2, num_of_patients)
        time.sleep(0.01)

if __name__ == "__main__":
    # 1. 予約対象の選択
    id1, birth1, id2, birth2 = "", "", "", ""
    num_of_patients = 0

    while True:
        print(f"{E_NAME}:e  {T_NAME}:t  両方:2")
        val = input("対象を選択してください: ").strip().lower()

        if val == "e":
            id1, birth1, num_of_patients = E_ID, E_BIRTH, 1
            break
        elif val == "t":
            id1, birth1, num_of_patients = T_ID, T_BIRTH, 1
            break
        elif val == "2":
            id1, birth1, id2, birth2, num_of_patients = E_ID, E_BIRTH, T_ID, T_BIRTH, 2
            break
        else:
            print("無効な入力です。")

    # 2. 実行時間の入力
    while True:
        time_input = input("開始時間を入力してください (例 07:29:40): ").strip()
        try:
            # 入力された時間が正しい形式かチェック
            datetime.datetime.strptime(time_input, "%H:%M:%S")
            break
        except ValueError:
            print("時刻の形式が正しくありません。HH:MM:SS 形式で入力してください。")

    # 現在の日時を取得
    now = datetime.datetime.now()
    
    # 指定された時刻を今日の日付で作成
    scheduled_time = datetime.datetime.strptime(time_input, "%H:%M:%S").time()
    today_scheduled = datetime.datetime.combine(now.date(), scheduled_time)
    
    # 指定時刻が過ぎている場合は翌日に設定
    if today_scheduled <= now:
        scheduled_date = (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        scheduled_date = now.strftime("%Y-%m-%d")
    
    scheduled_datetime = f"{scheduled_date} {time_input}"

    # スケジュール登録
    schedule.every().day.at(time_input).do(
        job, id1=id1, birth1=birth1, id2=id2, birth2=birth2, num_of_patients=num_of_patients
    )

    print(f"\n予約待機中... ({scheduled_datetime} に開始します)")
    while True:
        schedule.run_pending()
        print(f"\r現在時刻: {datetime.datetime.now().strftime('%H:%M:%S')} | 開始予定: {time_input}", end='')
        time.sleep(0.1)
