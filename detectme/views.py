import os

from requests import request
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from email.mime import image
from sre_constants import ANY
from tkinter import Frame
from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from student_management_app.models import Subjects, subject_atten, Subjecttostudent

# https://blog.miguelgrinberg.com/post/video-streaming-with-flask/page/8
import time
from re import X
from tkinter import Y
from scipy.spatial.distance import cosine
import mtcnn
from keras.models import load_model
import pickle

from sklearn.model_selection import train_test_split
from detectme.utils import *
from certifi import contents
from django.forms import NullBooleanField, NullBooleanSelect
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from matplotlib.style import context



class FaceDetector(object):
    def recognize(img,
              detector,
              encoder,
              encoding_dict,
              recognition_t=0.3,
              confidence_t=0.99,
              required_size=(100, 100), ):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = detector.detect_faces(img_rgb)
        
        for res in results:
      ####만약 인식된 얼굴이 있으면 지속
            if 0.75<res['confidence'] < confidence_t:
                continue
            face, pt_1, pt_2 = get_face(img_rgb, res['box'])
            encode = get_encode(encoder, face, required_size)
            encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
            name = 'unknown'
            
            ##만약 인식된 얼굴이() 0.58보다 높고 등록된 사진보다 작으면 
            distance = float("inf")
            for db_name, db_encode in encoding_dict.items():
                dist = cosine(db_encode, encode)
                #if dist < recognition_t and dist < distance:
                if dist < recognition_t and dist < 0.58:
                    name = db_name
                    distance = dist
                
            
            
#인식된 얼굴이 없으면 unknown 이 뜸
            #if name == 'unknown':
            if name =='unknown' :
                cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
                cv2.putText(img, 'unknown', pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
               # cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
            else:
                cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
#                cv2.putText(img, name , (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
#                        (0, 200, 200), 2)
#####확률 나오는거 
#                cv2.putText(img, name + f'__{distance:.2f}', (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,  (0, 200, 200), 2)

                cv2.putText(img, name , (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,  (0, 200, 200), 2)



                
                    
        return img

####메인 출력 
    if __name__ == '__main__':
        encoder_model = 'C:/djangostudent/detectme/facenet_keras.h5'
        encodings_path = 'C:/djangostudent/data_folder/admin/encodings.pkl'

        face_detector = mtcnn.MTCNN()
        face_encoder = load_model(encoder_model)
        encoding_dict = load_pickle(encodings_path)
        
        

        vc = cv2.VideoCapture(0)
        while vc.isOpened():
            ret, image = vc.read()

            if not ret:
                print("no frame")
                break
           
            frame = recognize(image, face_detector, face_encoder, encoding_dict)
            cv2.imshow('frame', image)

            if cv2.waitKey(0.5)>0:
                break



def detectme(request):
    context = {}
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(VideoCamera.gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")

    return render(request, "hod_check.html", context)

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        self.frame = cv2.flip(self.frame, 1)
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        frame = self.frame
        try:
             image = FaceDetector.recognize(frame,
              detector= mtcnn.MTCNN(),
              encoder= load_model('C:/djangostudent/detectme/facenet_keras.h5'),
              encoding_dict= load_pickle('C:/djangostudent/data_folder/encodings.pkl'))
        except TypeError:
            pass
        _, jpeg = cv2.imencode('.jpg',image)
        
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


    def gen(camera):
        while True:
        # frame = fe.recognize(image,
        #       detector= mtcnn.MTCNN(),
        #       encoder= load_model('C:/djangostudent/detectme/facenet_keras.h5'),
        #       encoding_dict= load_pickle('C:/Users/admin/encodings.pkl'))
            frame = camera.get_frame()
            yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
              


# @gzip.gzip_page
# def detectme(request):
#     try:
#         cam = VideoCamera()
#         return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
#     except:  # This is bad! replace it with proper handling
#         print("에러입니다...")
#         pass

