from django.shortcuts import render
from django.http.response import StreamingHttpResponse
# from recognition.camera import FaceDetect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from student_management_app.models import CustomUser, Staffs,Subjects
# Create your views here.
from django.shortcuts import render, redirect
import datetime

def index(request):
	subjects = Subjects.objects.filter(staff_id = request.user.id)
	print(subjects.id)
	return render(request, 'recognition/home.html')

# def gen(camera,subject):
# 	while True:
# 		frame = camera.get_frame(subject=subject)
# 		yield (b'--frame\r\n'
# 				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
# @csrf_exempt		
# def facecam_feed(request):
# 	now = datetime.now()
# 	hour = now.hour
# 	subjects = Subjects.objects.get()
# 	print(subjects)
# 	return StreamingHttpResponse(gen(FaceDetect(),subjects),
# 					content_type='multipart/x-mixed-replace; boundary=frame')

				