from bs4 import BeautifulSoup
from selenium import webdriver
from pytube import YouTube
import pandas as pd
import glob
import os.path


data = pd.read_csv('list.csv')


for i in range(len(data['Name'])):
    keyword = data['Name'][i]
    print(keyword)
    req = 'https://www.youtube.com/results?search_query={}'.format(keyword)
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome('./chromedriver.exe', options=options)
    driver.get(req)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    my_titles = soup.select('a#video-title')

    url = []
    url.append(my_titles[0].get('href'))

    #유튜브 mp4 다운
    # 유튜브 전용 인스턴스 생성
    link = 'https://www.youtube.com/watch?v=' + url[0].split('v=')[1]
    yt = YouTube(link)

    #특정영상 다운로드
    yt.streams.filter(only_audio=True).first().download()
    files = glob.glob("*.mp4")
    for x in files:
        if not os.path.isdir(x):
            filename = os.path.splitext(x)
            try:
                os.rename(x, filename[0] + '.wav')
            except:
                pass
    print('완료')
