from re import X
from tkinter import Y
from scipy.spatial.distance import cosine
import mtcnn
from keras.models import load_model
import pickle

from sklearn.model_selection import train_test_split
from detectme.utils import *


##얼굴인식 클래스

# def recognize(img,
#               detector,
#               encoder,
#               encoding_dict,
#               recognition_t=0.3,
#               confidence_t=0.99,
#               required_size=(X, Y), ):
#         img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = detector.detect_faces(img_rgb)
#         for res in results:
#       ####만약 인식된 얼굴이 있으면 지속
#             if 0.75<res['confidence'] < confidence_t:
#                 continue
#             face, pt_1, pt_2 = get_face(img_rgb, res['box'])
#             encode = get_encode(encoder, face, required_size)
#             encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
#             name = 'unknown'
            
#             ##만약 인식된 얼굴이() 0.58보다 높고 등록된 사진보다 작으면 
#             distance = float("inf")
#             for db_name, db_encode in encoding_dict.items():
#                 dist = cosine(db_encode, encode)
#                 if dist < recognition_t and dist < distance:
#                 #if and dist <recognition_t:
#                     name = db_name
#                     distance = dist
                
            
            
# #인식된 얼굴이 없으면 unknown 이 뜸
#             #if name == 'unknown':
#             if name =='unknown' :
#                 cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
#                 cv2.putText(img, 'unknown', pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
#                # cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
#             else:
#                 cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
# #                cv2.putText(img, name , (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
# #                        (0, 200, 200), 2)
#                 cv2.putText(img, name + f'__{distance:.2f}', (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,  (0, 200, 200), 2)
#  #               cv2.putText(img, name , (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
# #                        (0, 200, 200), 2)
#         return img


# ####메인 출력 
# if __name__ == '__main__':
#         encoder_model = 'C:/Users/admin/facenet_keras.h5'
#         encodings_path = 'C:/Users/admin/encodings.pkl'

#         face_detector = mtcnn.MTCNN()
#         face_encoder = load_model(encoder_model)
#         encoding_dict = load_pickle(encodings_path)

#         vc = cv2.VideoCapture(0)
#         while vc.isOpened():
#             ret, frame = vc.read()
#             if not ret:
#                 print("no frame")
#                 break
#             frame = recognize(frame, face_detector, face_encoder, encoding_dict)
#             cv2.imshow('frame', frame)

#             if cv2.waitKey(5) & 0xFF == 27:
#                 break

####ddd####
class FaceDetector(object):
    def recognize(img,
              detector,
              encoder,
              encoding_dict,
              recognition_t=0.3,
              confidence_t=0.99,
              required_size=(160, 160), ):
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
                if dist < recognition_t and dist < distance:
                #if and dist <recognition_t:
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
                cv2.putText(img, name + f'__{distance:.2f}', (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,  (0, 200, 200), 2)
 #               cv2.putText(img, name , (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
#                        (0, 200, 200), 2)
        return img


####메인 출력 
    if __name__ == '__main__':
        encoder_model = 'C:/Users/admin/facenet_keras.h5'
        encodings_path = 'C:/Users/admin/encodings.pkl'

        face_detector = mtcnn.MTCNN()
        face_encoder = load_model(encoder_model)
        encoding_dict = load_pickle(encodings_path)

        vc = cv2.VideoCapture(0)
        while vc.isOpened():
            ret, frame = vc.read()
            if not ret:
                print("no frame")
                break
            frame = recognize(frame, face_detector, face_encoder, encoding_dict)
            cv2.imshow('frame', frame)

            if cv2.waitKey(5) & 0xFF == 27:
                break

