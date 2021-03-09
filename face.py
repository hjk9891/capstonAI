import requests
from io import BytesIO

from PIL import Image, ImageDraw
import cognitive_face as CF
import json
import requests
from bs4 import BeautifulSoup
from random import randint

#날씨 크롤링 테스트
location = "서울"
Finallocation = location + '날씨'
LocationInfo = ""
NowTemp = ""
CheckDust = []
url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + Finallocation
hdr = {'User-Agent': ('mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.70 safari/537.36')}
req = requests.get(url, headers=hdr)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

ErrorCheck = soup.find('span', {'class' : 'btn_select'})
if 'None' in str(ErrorCheck):
    print("Error! 지역 검색 오류!")
else:
    for i in soup.select('span[class=btn_select]'):
        LocationInfo = i.text
    WeatherCast = soup.find('p', {'class': 'cast_txt'}).text
WeatherCast1 = WeatherCast.split(",")
print("오늘의 날씨: " + WeatherCast1[0])


# 우울할 때 힘나는 노래 크롤링
if __name__ == "__main__":
    RANK = 50  # 몇개의 곡을 가져올 것인지.

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    req = requests.get('https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=402227162', headers=header)  ## 주간 차트를 크롤링 할 것임
    html = req.text
    parse = BeautifulSoup(html, 'html.parser')

    titles = parse.find_all("div", {"class": "ellipsis rank01"})
    singers = parse.find_all("div", {"class": "ellipsis rank02"})
    albums = parse.find_all("div", {"class": "ellipsis rank03"})

    title = []
    singer = []
    album = []

    sadsing = []

    for t in titles:
        title.append(t.find('a').text)

    for s in singers:
        singer.append(s.find('span', {"class": "checkEllipsis"}).text)

    for a in albums:
        album.append(a.find('a').text)

    for i in range(RANK):
        # print('%3d위: %s [ %s ] - %s' % (i + 1, title[i], album[i], singer[i]))
        sadsing.append(title[i] + " " + "[" + album[i] + "]" + " - " + singer[i])
    sad_song = sadsing[randint(0, 49)]
    print(sad_song)#우울할 때 듣는 노래 50개 크롤링 한 것 중에 랜덤으로 한 개 출력

# 대중적이고 신나는 노래 크롤링
if __name__ == "__main__":
    RANK = 50  # 몇개의 곡을 가져올 것인지.

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    req = requests.get('https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=427175003', headers=header)  ## 주간 차트를 크롤링 할 것임
    html = req.text
    parse = BeautifulSoup(html, 'html.parser')

    titles = parse.find_all("div", {"class": "ellipsis rank01"})
    singers = parse.find_all("div", {"class": "ellipsis rank02"})
    albums = parse.find_all("div", {"class": "ellipsis rank03"})

    title = []
    singer = []
    album = []
    
    sing = []

    for t in titles:
        title.append(t.find('a').text)

    for s in singers:
        singer.append(s.find('span', {"class": "checkEllipsis"}).text)

    for a in albums:
        album.append(a.find('a').text)

    for i in range(RANK):
        #print('%3d위: %s [ %s ] - %s' % (i + 1, title[i], album[i], singer[i]))
        sing.append(title[i] +" "+ "[" +album[i] +"]"+ " - " + singer[i])
    exciting_song = sing[randint(0, 49)]
    print(exciting_song)


KEY ='b65cf089d7784364abaf43d455312df2'# 자신의 Cognitive Services API KEY
CF.Key.set(KEY)

BASE_URL = 'https://koreacentral.api.cognitive.microsoft.com/face/v1.0/'# 자신의 지역에 해당하는 URL
CF.BaseUrl.set(BASE_URL)

img_url = '/Users/hjk2/PycharmProjects/pythonProject1/MSFACE/img1.jpg' # 이미지 파일의 경로
faces = CF.face.detect(img_url,True,False,'age,emotion') # 중요!
# detect 함수는 4가지의 매개변수를 갖는다.
# 첫 번째 인자 : 이미지파일
# 두 번째 인자 : face_id의 반환 여부
# 세 번째 인자 : landmarks(눈,코,입 등의 위치)의 반환 여부
# 네 번째 인자 : 반환할 속성(연령,성별 등)
recomend_song = ''
for face in faces:
    print(face['faceAttributes']) # 터미널 창에 속성값들을 출력
    emotions = {}
    emotions['anger'] = face['faceAttributes']['emotion']['anger']
    emotions['contempt'] = face['faceAttributes']['emotion']['contempt']
    emotions['disgust'] = face['faceAttributes']['emotion']['disgust']
    emotions['fear'] = face['faceAttributes']['emotion']['fear']
    emotions['happiness'] = face['faceAttributes']['emotion']['happiness']
    emotions['neutral'] = face['faceAttributes']['emotion']['neutral']
    emotions['sadness'] = face['faceAttributes']['emotion']['sadness']
    emotions['surprise'] = face['faceAttributes']['emotion']['surprise']
    bestemotion = max(zip(emotions.values(), emotions.keys()))[1]
    if bestemotion == 'anger' or 'neutral' or 'contempt':
        recomend_song = exciting_song
    else :
        recomend_song = sad_song
    doc = {
        'age': face['faceAttributes']['age'],
        'emotion': bestemotion,
        'Weather': WeatherCast1[0],
        'recomend_song': recomend_song
    }
print(bestemotion)
print(doc)
# 인식된 얼굴에 네모 박스 그리는 함수 작성
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

img = Image.open(img_url) # img 변수에 이미지 파일을 넣어준다.
draw = ImageDraw.Draw(img)
for face in faces:
    draw.rectangle(getRectangle(face), outline='red') # 인식된 얼굴들에 네모 박스 쳐주기

img.show() # 이미지 뷰어로 이미지 띄우기

file_path = "./sample.json"
with open(file_path, 'w',encoding='utf-8') as outfile:
    json.dump(doc, outfile,ensure_ascii=False)