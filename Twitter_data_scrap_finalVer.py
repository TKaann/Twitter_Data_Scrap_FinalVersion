from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from matplotlib import pyplot as plt
import time
import os
import openpyxl



from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

from selenium.webdriver.common.by import By


def twitter_data():
    # Sayfamizda kac scroll asagi inecegimizi belirliyoruz.
    scroll = int(input("Scroll Number: "))
    # Selenium tarayıcısını başlat
    driver = webdriver.Chrome()

    # Twitter giriş sayfasını aç
    driver.get("https://twitter.com/login")

    time.sleep(5)
    box = ".r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-1dz5y72.r-fdjqy7.r-13qz1uu"
    # Kullanıcı adı giriş alanı
    username_input = driver.find_element(By.CSS_SELECTOR, box)

    # Kullanıcı adı giriş alanına tıklamak için
    username_input.click()
    username_input.send_keys("EMAIL")
    username_input.send_keys(Keys.ENTER)
    # Tiwtter kullanici adimizin girisi
    time.sleep(3)
    acc_input = driver.find_element(By.CSS_SELECTOR, box)
    acc_input.click()
    acc_input.send_keys("USERNAME")
    acc_input.send_keys(Keys.ENTER)
    # Sifre Girisi
    time.sleep(3)
    password_input = driver.find_element(By.CSS_SELECTOR, box)
    password_input.click()
    password_input.send_keys("PASSWORD")
    password_input.send_keys(Keys.ENTER)

    time.sleep(5)
    # Target Account
    url = 'https://twitter.com/AltayCemMeric'
    driver.get(url)
    time.sleep(8)

    # Cektigimiz Verileri csv dosyasina kaydediyoruz.
    file = open("tweet.csv", "w", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["UDate", "Tweet", "Reply", "Retweet", "Like", "View"])

    #

    a = 0
    while a < scroll:
        # Sayfanin kaynagini aliyoruz ve beautifulsoup'da html.parser ile parcaliyoruz.
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        tweets = soup.find_all("article", attrs={"data-testid": "tweet"})
            # User-Date, Tweet, Reply Sayisi, Retweet Sayisi, Like Sayisi, Toplam Goruntulenme verilerini cekiyoruz.
        for bod in tweets:
            udate_div = bod.find("div", attrs={"class": "css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t"})
            if udate_div:
                udate = udate_div.text
            tweet_div = bod.find("div", attrs={"data-testid": "tweetText"})
            if tweet_div:
                tweet = tweet_div.text
            reply_div = bod.find("div", attrs={"data-testid": "reply"})
            if reply_div:
                reply = reply_div.text
            retweet_div = bod.find("div", attrs={"data-testid": "retweet"})
            if retweet_div:
                retweet = retweet_div.text
            like_div = bod.find("div", attrs={"data-testid": "like"})
            if like_div:
                like = like_div.text
            view_a = bod.find("a", attrs={
                "class": "css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1777fci r-bt1l66 r-1ny4l3l r-bztko3 r-lrvibr"})
            if view_a:
                view = view_a.text

            # Yazma islemini yapiyoruz.
            writer.writerow([udate, tweet, reply, retweet, like, view])
        # time.sleep(5)

        a = a + 1

        # Scroll islemi
        lastHeight = driver.execute_script("return document.body.scrollHeight")
        i = 0
        while i < 1:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            newHeight = driver.execute_script("return document.body.scrollHeight")
            time.sleep(6)
            if newHeight == lastHeight:
                break
            else:
                lastHeight = newHeight
            i = i + 1


twitter_data()


df = pd.read_csv("tweet.csv")
data = pd.read_csv("tweet.csv")
data.to_excel("tweet_excel.xlsx")

print(df)


