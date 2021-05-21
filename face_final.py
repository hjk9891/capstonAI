
from PIL import Image, ImageDraw
import cognitive_face as CF
import json
import cv2



class FaceClass:
    def clickPhoto(self):
        # create a VideoCapture object and a window "Captured Image"
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("Captured Frame")

        while True:
            if (cam.isOpened()):
                # Read frame from camera
                flag, frame = cam.read()
                cv2.imshow("Captured Frame", frame)

            if not flag:
                break
            k = cv2.waitKey(1)

            if k % 256 == 27:
                # ESC pressed ----- Break
                print("!!Escape Hit!!, Closing.....")
                return 0
            elif k % 256 == 32:
                # SPACE pressed ---  Save Image
                img_name = "Image_0.jpg"
                cv2.imwrite(img_name, frame)
                print("..........{} Written!!.........".format(img_name))
                print("..........Loading Captured Image........")
                # Release cam object and close all image windows
                cam.release()
                cv2.destroyWindow("Captured Frame")
                return 1

    def __init__(self):
        self.exciting_song = '롤린'
        self.sad_song = '우리둘만아는'
        KEY = '62a13cd4bdd94056b6fd4a9643a96644'  # Cognitive Services API KEY 키값이 있어야 api 호출이 가능
        CF.Key.set(KEY)
        BASE_URL = 'https://koreacentral.api.cognitive.microsoft.com/face/v1.0/'  # 자신의 지역에 해당하는 URL //
        CF.BaseUrl.set(BASE_URL)
        self.img_url = '/Users/hjk2/PycharmProjects/pythonProject1/MSFACE/Image_0.jpg'  # 이미지 파일의 경로
        self.faces = CF.face.detect(self.img_url, True, False, 'age,emotion')  # 중요!
        # detect 함수는 4가지의 매개변수를 갖는다.
        # 첫 번째 인자 : 이미지파일
        # 두 번째 인자 : face_id의 반환 여부
        # 세 번째 인자 : landmarks(눈,코,입 등의 위치)의 반환 여부
        # 네 번째 인자 : 반환할 속성(연령,성별 등)
        self.recomend_song = ''
        self.song_url = ''
    def face(self):
        for face in self.faces:

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
                self.recomend_song = self.exciting_song
                self.song_url = 'https://music.youtube.com/search?q=' + self.recomend_song
            else :
                self.recomend_song = self.sad_song
                self.song_url = 'https://music.youtube.com/search?q=' + self.recomend_song
            doc = {
                'age': face['faceAttributes']['age'],
                'emotion': bestemotion,
                'recomend_song': self.recomend_song,
                'song_url' : self.song_url
            } # json으로 출력되는 부분
        print(doc)
        # 인식된 얼굴에 네모 박스 그리는 함수 작성
        def getRectangle(faceDictionary):
            rect = faceDictionary['faceRectangle']
            left = rect['left']
            top = rect['top']
            bottom = left + rect['height']
            right = top + rect['width']
            return ((left, top), (bottom, right))

        img = Image.open(self.img_url) # img 변수에 이미지 파일을 넣어준다.
        draw = ImageDraw.Draw(img)
        for face in self.faces:
            draw.rectangle(getRectangle(face), outline='red') # 인식된 얼굴들에 네모 박스 쳐주기
        img = img.convert("RGB")
        print(img)
        img.save('./test.jpg')
        img.show() # 이미지 뷰어로 이미지 띄우기

        file_path = "./sample.json"
        with open(file_path, 'w',encoding='utf-8') as outfile:
            json.dump(doc, outfile,ensure_ascii=False)

