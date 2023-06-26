from imutils.video import VideoStream
from imutils.video import FPS
import imutils
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import cv2,os,urllib.request,pickle
import numpy as np
from django.conf import settings
from recognition import extract_embeddings
import datetime
from recognition import train_model
from student_management_app.models import CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel, Attendance, AttendanceReport, StudentResult,LectureRoom,Subjecttostudent
# load our serialized face detector model from disk
protoPath = os.path.sep.join([settings.BASE_DIR, "face_detection_model/deploy.prototxt"])
modelPath = os.path.sep.join([settings.BASE_DIR,"face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
# load our serialized face embedding model from disk
embedder = cv2.dnn.readNetFromTorch(os.path.join(settings.BASE_DIR,'face_detection_model/openface_nn4.small2.v1.t7'))
# load the actual face recognition model along with the label encoder
recognizer = os.path.sep.join([settings.BASE_DIR, "output/recognizer.pickle"])
recognizer = pickle.loads(open(recognizer, "rb").read())
le = os.path.sep.join([settings.BASE_DIR, "output/le.pickle"])
le = pickle.loads(open(le, "rb").read())
dataset = os.path.sep.join([settings.BASE_DIR, "dataset"])
user_list = [ f.name for f in os.scandir(dataset) if f.is_dir() ]



class FaceDetect(object):
	def __init__(self):
		# extract_embeddings.embeddings()
		# train_model.model_train()
		# initialize the video stream, then allow the camera sensor to warm up
		self.vs = VideoStream(src=0).start()
		# start the FPS throughput estimator
		self.fps = FPS().start()

	def __del__(self):
		cv2.destroyAllWindows()

	

		

	def get_frame(self):
		# grab the frame from the threaded video stream
		frame = self.vs.read()
		frame = cv2.flip(frame,1)

		# resize the frame to have a width of 600 pixels (while
		# maintaining the aspect ratio), and then grab the image
		# dimensions
		frame = imutils.resize(frame, width=600)
		(h, w) = frame.shape[:2]

		# construct a blob from the image
		imageBlob = cv2.dnn.blobFromImage(
			cv2.resize(frame, (300, 300)), 1.0, (300, 300),
			(104.0, 177.0, 123.0), swapRB=False, crop=False)

		# apply OpenCV's deep learning-based face detector to localize
		# faces in the input image
		detector.setInput(imageBlob)
		detections = detector.forward()
		#MEDIA_ROOT#= detector.setInput(imageBlob)


		# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections
			if confidence > 0.55:
				# compute the (x, y)-coordinates of the bounding box for
				# the face
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# extract the face ROI
				face = frame[startY:endY, startX:endX]
				(fH, fW) = face.shape[:2]

				# ensure the face width and height are sufficiently large
				if fW < 20 or fH < 20:
					continue

				# construct a blob for the face ROI, then pass the blob
				# through our face embedding model to obtain the 128-d
				# through our face embedding model to obtain the 128-d
				faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
					(96, 96), (0, 0, 0), swapRB=True, crop=False)
				embedder.setInput(faceBlob)
				vec = embedder.forward()

				# perform classification to recognize the face
				preds = recognizer.predict_proba(vec)[0]
				j = np.argmax(preds)
				proba = preds[j]
				global name
				name = le.classes_[j]
				print(proba)


				# draw the bounding box of the face along with the
				# associated probability
				if proba >=0.6:
					text = "{}: {:.2f}%".format(name, proba * 100)
					y = startY - 10 if startY - 10 > 10 else startY + 10
					cv2.rectangle(frame, (startX, startY), (endX, endY),
						(0, 0, 255), 2)
					cv2.putText(frame, text, (startX, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
					#if proba >= 0.83:
						# list_data = []
						# data_small={"name":name}
						# list_data.append(data_small)
						# return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
						# subject_model = Subjects.objects.get(subject_name=subject)
						# d_today = datetime.date.today()
						# cos_id = CustomUser.objects.get(first_name=name)
						# stud_num = cos_id.id
						# students_num = Students.objects.get()
						# subject_model_id=subject_model.id
						# attendance_model= Attendance(subject_id_id=subject_model_id,session_year_id_id=1,attendance_date=d_today)
						# attendance_model().save
						# attendancereport_model= Attendance.objects.get(subject_id_id=subject_model_id,attendance_date=d_today)
						# atten_re_model =attendancereport_model.id
						# atten_retosave=AttendanceReport(attendance_id_id=atten_re_model,status=1,student_id_id=stud_num)
						# atten_retosave.save()
						# subjects = Subjects.objects.filter(staff_id = request.user.id)
					#print(subject)
					# print(subject.values_list)

					
						
					
				else:
					text = "{}: {:.2f}%".format("unknown", proba * 100)
					y = startY - 10 if startY - 10 > 10 else startY + 10
					cv2.rectangle(frame, (startX, startY), (endX, endY),
						(0, 0, 255), 2)
					cv2.putText(frame, text, (startX, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)		
			# else : 
			# 	cv2.rectangle(frame, (startX, startY), (endX, endY),
			# 		(0, 0, 255), 2)
			# 	cv2.putText(frame, text, (startX, startY),
			# 		cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)		

		# update the FPS counter
		self.fps.update()
		ret, jpeg = cv2.imencode('.jpg', frame)
		return jpeg.tobytes()
		


