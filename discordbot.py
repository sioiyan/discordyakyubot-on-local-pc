#coding: utf-8

# 上記で取得したアプリのトークンを入力
BOT_TOKEN = "NDMwNTYwNjY5Njk2NTI0Mjk5.DaR-aw.sEUcdNZYHdej3RvLc9sfm7tADHA"

# パッケージのインポートとインスタンス作成
import discord
client = discord.Client()

import lxml.html
import datetime
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

def todayyakyuurl():
    today = datetime.date.today()
    url = "https://baseball.yahoo.co.jp/npb/schedule/?date=%d%02d%02d" % (today.year, today.month, today.day)

    # URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "lxml")

    # span要素全てを摘出する→全てのspan要素が配列に入ってかえされます→[<span class="m-wficon triDown"></span>, <span class="l-h...
    array = soup.find_all("td", class_="today")

    return array

def tomorrowyakyuurl():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    url = "https://baseball.yahoo.co.jp/npb/schedule/?date=%d%02d%02d" % (tomorrow.year, tomorrow.month, tomorrow.day)

    # URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "lxml")

    # span要素全てを摘出する→全てのspan要素が配列に入ってかえされます→[<span class="m-wficon triDown"></span>, <span class="l-h...
    array = soup.find_all("td", class_="today")
    return array

def returnsoup(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "lxml")
    return soup

def ljust_fixed(string,length):
    count_length = 0
    for char in string:
        if ord(char) <= 255:
            count_length += 1
        else:
            count_length += 2
    if length-count_length-1 < 0:
        paddingeq_len = 0
    else:
        paddingeq_len = length-count_length-1
    return string + paddingeq_len * '=' + '>'
# ログイン&準備が完了したら一度だけ実行される
@client.event
async def on_ready():
    # コンソールにBOTとしてログインした名前とUSER-IDを出力
    print('Logged in as')
    print('BOT-NAME :', client.user.name)
    print('BOT-ID   :', client.user.id)
    print('------')


# メッセージを受信するごとに実行される
@client.event
async def on_message(message):

    # BOTとメッセージの送り主が同じ人なら処理しない
    if client.user == message.author:
        return

    # メッセージの頭が "!hello" なら実行する
    if message.content.startswith('!hello'):
        # メッセージが送られてきたチャンネルに "Hello World..." を返す
        await client.send_message(message.channel, 'Hello World...')

    if message.content.startswith('!siai'):
        senddata=""
        siaiurl = "";
        base = "";
        attackteam = "";
        array = todayyakyuurl()
        try:
            for i in range(int(len(array)/6)):
                #試合中
                if array[6*i+3].text != "試合前" and array[6*i+3].text != "結果":
                    #試合のURLを取得
                    siaiurl = "https://baseball.yahoo.co.jp/live" + array[6*i+3].a.get("href") + "score"
                    siaihtml = urllib.request.urlopen(siaiurl)
                    soup = BeautifulSoup(siaihtml, "lxml")
                    siaiout = soup.select(".sbo .o b")
                    siaibase = soup.select("#dakyu")
                    hometeam = array[6*i].text
                    visteam = array[6*i+2].text

                    if "裏" in array[6*i+3].text:
                        hometeam = "__**" + hometeam + "**__"
                    else:
                        visteam =  "__**" + visteam + "**__"

                    try:
                        outcount = len(siaiout[0].text) + "アウト"
                    except:
                        outcount = "ノーアウト"
                    finally:
                        if siaibase[0].find_all("div", id="base1") and siaibase[0].find_all("div", id="base2") and siaibase[0].find_all("div", id="base3"):
                            base = "満塁"
                        elif siaibase[0].find_all("div", id="base2") and siaibase[0].find_all("div", id="base3"):
                            base = "2塁3塁"
                        elif siaibase[0].find_all("div", id="base1") and siaibase[0].find_all("div", id="base3"):
                            base = "1塁3塁"
                        elif siaibase[0].find_all("div", id="base1") and siaibase[0].find_all("div", id="base2"):
                            base = "1塁2塁"
                        elif siaibase[0].find_all("div", id="base3"):
                            base = "3塁"
                        elif siaibase[0].find_all("div", id="base2"):
                            base = "2塁"
                        elif siaibase[0].find_all("div", id="base1"):
                            base = "1塁"
                        else:
                            base = "ランナーなし"
                    senddata += hometeam + " " + array[6*i+1].text + " " + visteam + " " + array[6*i+3].text + " " + outcount + base + "\n"
                elif array[6*i+3].text == "結果":
                    senddata += array[6*i].text + array[6*i+1].text + " " + array[6*i+2].text + " " + " 終了\n"
                elif array[6*i+3].text == "試合前":
                    homep_url = "https://baseball.yahoo.co.jp" + array[6*i+5].find_all("a")[0].get("href")
                    visiterp_url = "https://baseball.yahoo.co.jp" + array[6*i+5].find_all("a")[1].get("href")

                    homesoup = returnsoup(homep_url)
                    visitersoup = returnsoup(visiterp_url)

                    homeera = homesoup.select(".yjM td")[0].text
                    visiterera = visitersoup.select(".yjM td")[0].text

                    senddata += array[6*i].text + " " + array[6*i+1].text + " " + array[6*i+2].text + " " + array[6*i+3].text + " " +  array[6*i+4].text + "\n（予）" + array[6*i+5].find_all("a")[0].text.replace(" ","　") + "\n　防御率:" + homeera + "\n（予）" + array[6*i+5].find_all("a")[1].text.replace(" ","　") + "\n　防御率:" + visiterera + "\n\n"
                else:
                    senddata += array[6*i].text + " " + array[6*i+1].text + " " + array[6*i+2].text + " " + array[6*i+3].text + " " +  array[6*i+4].text + "\n" + array[6*i+5].text.strip().replace("|テレビ放送","\n")
        except Exception as e:
            senddata = "今日は試合がないようです"
            print(e)
        await client.send_message(message.channel, senddata)

    if message.content.startswith('!asita'):
        senddata=""
        array = tomorrowyakyuurl()
        try:
            for i in range(int(len(array)/6)):
                    homep_url = "https://baseball.yahoo.co.jp" + array[6*i+5].find_all("a")[0].get("href")
                    visiterp_url = "https://baseball.yahoo.co.jp" + array[6*i+5].find_all("a")[1].get("href")

                    homesoup = returnsoup(homep_url)
                    visitersoup = returnsoup(visiterp_url)

                    homeera = homesoup.select(".yjM td")[0].text
                    visiterera = visitersoup.select(".yjM td")[0].text

                    #teamname = "**" + array[6*i+3].text + "**"

                    senddata += array[6*i].text + " " + array[6*i+1].text + " " + array[6*i+2].text + " " + array[6*i+3].text + " " +  array[6*i+4].text + "\n（予）" + array[6*i+5].find_all("a")[0].text.replace(" ","　") + "\n　防御率:" + homeera + "\n（予）" + array[6*i+5].find_all("a")[1].text.replace(" ","　") + "\n　防御率:" + visiterera + "\n\n"
        except Exception as e:
            senddata = "今日は試合がないようです。もしくはまだ予告先発が発表されていません。"
            print(e)
        await client.send_message(message.channel, senddata)
    #試合中の場合,試合状況をキャプチャしてdiscord上に投稿
    if message.content.startswith('!baystars') or message.content.startswith('!carp') or message.content.startswith('!tigers') or message.content.startswith('!giants') or message.content.startswith('!dragons') or message.content.startswith('!swallows')\
    or message.content.startswith('!lions') or message.content.startswith('!fighters') or message.content.startswith('!hawks') or message.content.startswith('!marines') or message.content.startswith('!buffaloes') or message.content.startswith('!eagles')\
    or message.content.startswith('!de') or message.content.startswith('!softbank') or message.content.startswith('!hanshin') or message.content.startswith('!tora') or message.content.startswith('!koi') or message.content.startswith('!yakult') or message.content.startswith('!hiroshima')\
    or message.content.startswith('!yokohama') or message.content.startswith('!dena') or message.content.startswith('!kyojin') or message.content.startswith('!chunichi') or message.content.startswith('!fukuoka') or message.content.startswith('!seibu') or message.content.startswith('!rakuten')\
    or message.content.startswith('!orix') or message.content.startswith('!ham') or message.content.startswith('!lotte'):
        #本日の野球速報URL
        array = todayyakyuurl()
        team = ""
        siaiurl = ""
        #チーム名指定
        if message.content.startswith('!carp') or message.content.startswith('!koi') or message.content.startswith('!hiroshima'):
            team = "広島"
        elif message.content.startswith('!tigers') or message.content.startswith('!hanshin') or message.content.startswith('!tora'):
            team = "阪神"
        elif message.content.startswith('!baystars') or message.content.startswith('!dena') or message.content.startswith('!yokohama'):
            team = "ＤｅＮＡ"
        elif message.content.startswith('!giants') or message.content.startswith('!kyojin'):
            team = "巨人"
        elif message.content.startswith('!dragons') or message.content.startswith('!chunichi'):
            team = "中日"
        elif message.content.startswith('!swallows') or message.content.startswith('!yakult'):
            team = "ヤクルト"
        elif message.content.startswith('!hawks') or message.content.startswith('!softbank') or message.content.startswith('!fukuoka'):
            team = "ソフトバンク"
        elif message.content.startswith('!lions') or message.content.startswith('!seibu'):
            team = "西武"
        elif message.content.startswith('!eagles') or message.content.startswith('!rakuten'):
            team = "楽天"
        elif message.content.startswith('!buffaloes') or message.content.startswith('!orix'):
            team = "オリックス"
        elif message.content.startswith('!fighters') or message.content.startswith('!ham'):
            team = "日本ハム"
        elif message.content.startswith('!marines') or message.content.startswith('!lotte'):
            team = "ロッテ"

        #試合URLを探す
        for i in range(int(len(array)/6)):
            if array[6*i].text == team or array[6*i+2].text == team:
                #チームが試合中の場合試合URLを取得（試合中でない場合はsiaiurlは空）
                if array[6*i+3].a.get("href"):
                    siaiurl = "https://baseball.yahoo.co.jp/live" + array[6*i+3].a.get("href") + "score"
                    break

        #画面キャプチャ用のおまじない
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Firefox(firefox_options=options)
        try:
            browser.get(siaiurl)
            png = browser.find_element_by_id('gm_ball').screenshot_as_png
            with open("./screenshot.png", "wb") as f:
                f.write(png)
            browser.close()
            await client.send_file(message.channel, 'screenshot.png')
        except:
            await client.send_message(message.channel, team + "は試合がありません")

    if message.content.startswith('!exit'):
        exit()
# APP(BOT)を実行
client.run(BOT_TOKEN)
