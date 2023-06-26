import os
import pickle
import numpy as np
import cv2
import mtcnn
from keras.models import load_model
from utils import get_face, get_encode, l2_normalizer, normalize
import schedule
import time
import datetime

# hyper-parameters
# encoder_model = 'C:/djangostudent/facenet_keras.h5'
# people_dir = 'C:/Users/admin/data'
# encodings_path = 'C:/djangostudent/data_folderl/encodings.pkl'
# required_size = (160, 160)

# face_detector = mtcnn.MTCNN()
# face_encoder = load_model(encoder_model)

# encoding_dict = dict()

# for person_name in os.listdir(people_dir):
#     person_dir = os.path.join(people_dir, person_name)
#     encodes = []
#     for img_name in os.listdir(person_dir):
#         img_path = os.path.join(person_dir, img_name)
#         img = cv2.imread(img_path)
#         img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = face_detector.detect_faces(img_rgb)
#         if results:
#             res = max(results, key=lambda b: b['box'][2] * b['box'][3])
#             face, _, _ = get_face(img_rgb, res['box'])

#             face = normalize(face)
#             face = cv2.resize(face, required_size)
#             encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
#             encodes.append(encode)
#     if encodes:
#         encode = np.sum(encodes, axis=0)
#         encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]
#         encoding_dict[person_name] = encode


# for key in encoding_dict.keys():
#     print(key)

# with open(encodings_path, 'wb') as file:
#     pickle.dump(encoding_dict, file)

# def prepare_data(self):
#     encoder_model = 'C:/djangostudent/facenet_keras.h5'
#     people_dir = 'C:/Users/admin/data'
#     encodings_path = 'C:/djangostudent/data_folderl/encodings.pkl'
#     required_size = (160, 160)

#     face_detector = mtcnn.MTCNN()
#     face_encoder = load_model(encoder_model)

#     encoding_dict = dict()

#     for person_name in os.listdir(people_dir):
#         person_dir = os.path.join(people_dir, person_name)
#         encodes = []
#         for img_name in os.listdir(person_dir):
#             img_path = os.path.join(person_dir, img_name)
#             img = cv2.imread(img_path)
#             img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             results = face_detector.detect_faces(img_rgb)
#             if results:
#                 res = max(results, key=lambda b: b['box'][2] * b['box'][3])
#                 face, _, _ = get_face(img_rgb, res['box'])

#                 face = normalize(face)
#                 face = cv2.resize(face, required_size)
#                 encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
#                 encodes.append(encode)
#         if encodes:
#             encode = np.sum(encodes, axis=0)
#             encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]
#             encoding_dict[person_name] = encode


#     for key in encoding_dict.keys():
#         print(key)

#     with open(encodings_path, 'wb') as file:
#         pickle.dump(encoding_dict, file)

# def massage():
#     print("데이터 학습중")

# schedule.every(12).weeks.at("00:00").do(prepare_data, massage)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
def prepare_data(self):
    encoder_model = 'C:/djangostudent/facenet_keras.h5'
    people_dir = 'C:/Users/admin/data'
    encodings_path = 'C:/djangostudent/data_folderl/encodings.pkl'
    required_size = (160, 160)

    face_detector = mtcnn.MTCNN()
    face_encoder = load_model(encoder_model)

    encoding_dict = dict()

    for person_name in os.listdir(people_dir):
        person_dir = os.path.join(people_dir, person_name)
        encodes = []
        for img_name in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_name)
            img = cv2.imread(img_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = face_detector.detect_faces(img_rgb)
            if results:
                res = max(results, key=lambda b: b['box'][2] * b['box'][3])
                face, _, _ = get_face(img_rgb, res['box'])

                face = normalize(face)
                face = cv2.resize(face, required_size)
                encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
                encodes.append(encode)
        if encodes:
            encode = np.sum(encodes, axis=0)
            encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]
            encoding_dict[person_name] = encode


    for key in encoding_dict.keys():
        print(key)

    with open(encodings_path, 'wb') as file:
        pickle.dump(encoding_dict, file)

