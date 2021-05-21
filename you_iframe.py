import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from pytube import YouTube
import pandas as pd

data = pd.read_csv('Fun.csv')
Name = []
ifram =[]

for i in range(len(data['Name'])):
    if i > 101:
        keyword = data['Name'][i]
        Emotion = data['Emotion']
        req = 'https://www.youtube.com/results?search_query={}'.format(keyword)
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome('./chromedriver.exe', options=options)
        driver.get(req)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        my_titles = soup.select('a#video-title')

        title = []
        url = []
        url.append(my_titles[0].get('href'))


        iframe = 'https://www.youtube.com/embed/' + url[0].split('v=')[1]

        Name.append(keyword)
        ifram.append(iframe)
        df = pd.DataFrame(Name, columns=['Name'])
        df['Emotion'] = Emotion
        df['iframe'] = ifram

        print(df)
        df.to_csv('sample3.csv', encoding='utf-8-sig')
driver.close()
df = pd.DataFrame(Name, columns=['Name'])
df['iframe'] = ifram
print(df)
df.to_csv('sample2.csv',encoding='utf-8-sig')
#유튜브 mp4 다운
#유튜브 전용 인스턴스 생성
#link = 'https://www.youtube.com/watch?v=' + url[0].split('v=')[1]
#yt = YouTube(link)

# 특정영상 다운로드
#yt.streams.filter(only_audio=True).first().download()

#print('완료')