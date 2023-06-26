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
import datetime
from pytz import timezone
from django.http.response import StreamingHttpResponse
import csv
from urllib import response
from matplotlib.style import context
from django.forms.models import model_to_dict
from student_management_app.camera import FaceDetect
from student_management_app.models import CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel, Attendance, AttendanceReport, LeaveReportStaff, FeedBackStaffs, StudentResult,LectureRoom,Subjecttostudent,FeedBackStudent
from recognition.camera import *

def staff_home(request):
    # Fetching All Students under Staff

    subjects = Subjects.objects.filter(staff_id=request.user.id)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)
    
    final_course = []
    # Removing Duplicate Course Id
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)
    
    students_count = Students.objects.filter(course_id__in=final_course).count()
    subject_count = subjects.count()

    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
    # Fetch All Approve Leave
    staff = Staffs.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()

    #Fetch Attendance Data by Subjects
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance = Students.objects.filter(course_id__in=final_course)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
        student_list.append(student.admin.first_name+" "+ student.admin.last_name)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    context={
        "students_count": students_count,
        "attendance_count": attendance_count,
        "leave_count": leave_count,
        "subject_count": subject_count,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
        "student_list": student_list,
        "attendance_present_list": student_list_attendance_present,
        "attendance_absent_list": student_list_attendance_absent
    }
    return render(request, "staff_template/staff_home_template.html", context)



def staff_take_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "staff_template/take_attendance_template.html", context)


def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, "staff_template/staff_apply_leave_template.html", context)


def staff_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('staff_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('staff_apply_leave')


# def staff_feedback(request):
#     print(request.user.id)
#     staff_obj = Staffs.objects.get(admin=request.user.id)
#     feedback_data = FeedBackStaffs.objects.filter(staff_id=staff_obj)
#     context = {
#         "feedback_data":feedback_data
#     }
#     return render(request, "staff_template/staff_feedback_template.html", context)


def staff_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Staffs.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStaffs(staff_id=staff_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('staff_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('staff_feedback')


# WE don't need csrf_token when using Ajax
@csrf_exempt
def get_students(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in students:
        data_small={"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def get_student1(request):

    students =Students.objects.all()
    list_data = []
    for student in students:
        data_small = {"id":student.admin.id, "stu_id":student.admin.first_name, "name":student.admin.last_name,"cor":student.course_id_id}
        list_data.append(data_small)
    return JsonResponse(json.dump(list_data),content_type="application/json", safe=False)    


@csrf_exempt
def save_attendance_data(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date_a = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")   
    subject_model = Subjects.objects.get(id=subject_id)
    session_year_model = SessionYearModel.objects.get(id=session_year_id)
    attendance_date1 = Attendance.objects.filter(attendance_date=attendance_date_a)

    try:
        attendance_data_c = Attendance.objects.get(attendance_date=attendance_date_a)
        attendance_data_d=attendance_data_c.id
    except Attendance.DoesNotExist:
        attendance_data_c =None
        attendance_data_d=None  
    json_student = json.loads(student_ids)
    print(json_student)
    try:
        if attendance_date1:
            for stud in json_student:
                student23 = Students.objects.get(admin=stud['id'])
                if stud['status'] == 1:
                    attr_re = AttendanceReport.objects.get(student_id_id=student23,attendance_id_id=attendance_data_d)
                    attr_re.status = 1
                    attr_re.save()
                        
            return HttpResponse("OK")
        else :
            attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date_a, session_year_id=session_year_model)
            attendance.save()
            for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
                student = Students.objects.get(admin=stud['id'])
                attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
                attendance_report.save()
            return HttpResponse("OK")
    except:
        return HttpResponse("Error")    

@csrf_exempt
def save_studenttostudent_data(request):
    student_dataes = request.POST.get("student_dataes")
    subject_id = request.POST.get("subject_id")
    json_student = json.loads(student_dataes)
    subject_model = Subjects.objects.get(id=subject_id)
    subtostu = Subjecttostudent.objects.filter(subject_id_id=subject_id)
    print(subject_model)
    subjecttostudent_model=Subjecttostudent.objects.all()


    try:
        for stud in json_student:
            print('성공')
            
            cos_id = CustomUser.objects.get(first_name=stud['학번'])
            stud_id = (cos_id.id)
            stud_id1 = Students.objects.get(admin_id = stud_id)
            stud2 = stud_id1.id
            subjecttostudent_model=Subjecttostudent.objects.filter(student_id_id=stud2,subject_id_id = subject_model.id)
            print("성공1")
            if subjecttostudent_model:
                continue
            else:
                subtostu = Subjecttostudent(student_id_id=stud2,subject_id_id = subject_model.id)
                subtostu.save()
            

            #print(stud3)
            
            
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")          
    






def staff_update_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "staff_template/update_attendance_template.html", context)

@csrf_exempt
def get_attendance_dates(request):
    

    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(subject_id=subject_model, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "session_year_id":attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)



@csrf_exempt
def get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date') # 화면에서 선택한 출석 날짜(attendance)의 id
    attendance = Attendance.objects.get(id=attendance_date)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name, "name1":student.student_id.admin.last_name, "status":student.status, "attendanceDate":str(attendance.attendance_date)}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def update_attendance_data(request):
    student_ids = request.POST.get("student_ids")

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_student = json.loads(student_ids)

    try:
        
        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])

            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status=stud['status']

            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)

    context={
        "user": user,
        "staff": staff
    }
    return render(request, 'staff_template/staff_profile.html', context)


def staff_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('staff_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staffs.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('staff_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('staff_profile')



def staff_add_result(request):
    #subjects = Subjects.objects.filter(staff_id=request.user.id)

    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        #"subjectos " : subjectos,
        "session_years": session_years,
    }
    return render(request, "staff_template/add_result_template.html", context)


def staff_add_result_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_add_result')
    else:
        student_admin_id = request.POST.get('student_list')
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')
        subject_id = request.POST.get('subject')

        student_obj = Students.objects.get(admin=student_admin_id)
        subject_obj = Subjects.objects.get(id=subject_id)

        try:
            # Check if Students Result Already Exists or not
            check_exist = StudentResult.objects.filter(subject_id=subject_obj, student_id=student_obj).exists()
            if check_exist:
                result = StudentResult.objects.get(subject_id=subject_obj, student_id=student_obj)
                result.subject_assignment_marks = assignment_marks
                result.subject_exam_marks = exam_marks
                result.save()
                messages.success(request, "Result Updated Successfully!")
                return redirect('staff_add_result')
            else:
                result = StudentResult(student_id=student_obj, subject_id=subject_obj, subject_exam_marks=exam_marks, subject_assignment_marks=assignment_marks)
                result.save()
                messages.success(request, "Result Added Successfully!")
                return redirect('staff_add_result')
        except:
            messages.error(request, "Failed to Add Result!")
            return redirect('staff_add_result')




def staff_add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    lectureroom = LectureRoom.objects.all()
    
    
    context = {
        "courses": courses,
        "staffs": staffs,
        "lectureroom" : lectureroom
    }
    return render(request, 'staff_template/staff_add_subject_template.html', context)



def staff_add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('staff_add_subject')
    else:
        subject_name = request.POST.get('subject')
        subject_num = request.POST.get('subject_num')
        subjects_day = request.POST.get('subjects_day')
        subjects_start_time = request.POST.get('subjects_start_time')
        subjects_stop_time = request.POST.get('subjects_stop_time')
        subjects_start_time2 = subjects_start_time.replace(':','')
        subjects_start_time3 = int(subjects_start_time2)
        
        subjects_stop_time2 = subjects_stop_time.replace(':','')
        subjects_stop_time3 = int(subjects_stop_time2)




        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        lectureroom_id = request.POST.get('lectureroom')
        lectureroom = LectureRoom.objects.get(id=lectureroom_id)
       
        
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)

        try:
            
            subject = Subjects(subject_name=subject_name,subject_num=subject_num, course_id=course, staff_id=staff, subjects_day = subjects_day, subjects_start_time= subjects_start_time3, subjects_stop_time = subjects_stop_time3,lectureroom_id=lectureroom)
           
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return redirect('staff_add_subject')
        except:
            messages.error(request, "Failed to Add Subject!")
            return redirect('staff_add_subject')


def add_subjecttostudent(request):
    subjects = Subjects.objects.filter(staff_id = request.user.id)
    student_info = CustomUser.objects.filter(user_type="3")
    context = {
        "subjects" : subjects,
        "student_info" : student_info
    }
    return render(request, 'staff_template/add_subjecttostudent_template.html', context)


def add_subjecttostudent_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subjecttostudent')
    else:
        subject_id = request.POST.get('subject')
        subject = Subjects.objects.get(id=subject_id)

        try:
            
            subjecttostudent = Subjecttostudent(subject=subject)
           
            subjecttostudent.save()
            messages.success(request, "Student Added Successfully!")
            return redirect('add_subjecttostudent')
        except:
            messages.error(request, "Failed to Add Student!")
            return redirect('add_subjecttostudent') 

# def search_subject(request):
#     subject_names =request.GET('subject_name',None)
#     subject_numes = request.Get('subject_num',None)
#     if subject_names:
#         subject_namese = Subjects.objects.filter(subject_name=subject_names)
#     if subject_numes:
#         subject_nums = Subjects.objects,filter(subject_num=subject_numes)
def staff_check(request):
    subjects = Subjects.objects.filter(staff_id = request.user.id)
    student_info = CustomUser.objects.filter(user_type="3")
    context = {
        "subjects" : subjects,
        "student_info" : student_info
    
    }
    return render(request, 'staff_template/staff_check.html', context)

def gen(camera,staff_id):
	while True:
		frame = camera.get_frame(staff_id)
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@csrf_exempt
def facecam_feed1(request):
        subjects = Subjects.objects.filter(staff_id = request.user.id)
        lectureRoom_name = Staffs.objects.get(admin_id=request.user.id)
        print(lectureRoom_name.id)
        staff_id= lectureRoom_name.id
        return StreamingHttpResponse(gen(FaceDetect(),lectureRoom_name),
					content_type='multipart/x-mixed-replace; boundary=frame')

                 

@csrf_exempt
def save_subject_for_check(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    sub_id = request.POST.get("subject")
    global sub_id_j
    sub_id_j = json.loads(sub_id)
    print(sub_id_j)
    try:
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")    

def staff_feedback(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {

        "feedbacks": feedbacks
    }
    return render(request, 'staff_template/staff_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")

@csrf_exempt
def get_subjects(request):
    print("성공aja")
    w_today = datetime.date.today().strftime("%A") ##오늘 요일
    nowhour_str=datetime.datetime.now(timezone('Asia/Seoul')).hour
    nowmin_str=datetime.datetime.now(timezone('Asia/Seoul')).minute
    nowhour = str(nowhour_str)
    nowhour_forstop = nowhour_str+1
    nowhour_forstop1 =str(nowhour_forstop)
    nowmin_str1 = nowmin_str+30
    nowmin_str2 = nowmin_str
    nowmin_forstart = str(nowmin_str1)
    nowmin_forstop = str(nowmin_str2)
    lectureRoom_name = Staffs.objects.get(admin_id=request.user.id)
    staff_name = lectureRoom_name.address
    staff_name1 = staff_name.replace(' ','')
    lecture_name = LectureRoom.objects.get(lectureroom_name=staff_name1)
    lec_id=lecture_name.id 
    #nowtime = nowhour+nowmin ##현재시간
    nowtime_for_start = nowhour+nowmin_forstart
    print("tjdrhd312312")
    nowtime_for_stop = nowhour_forstop1+nowmin_forstop
    subjects = Subjects.objects.get(lectureroom_id_id = lec_id,subjects_start_time__lte=nowtime_for_start,
                                        subjects_stop_time__gte=nowtime_for_stop,subjects_day=w_today)
    subjects1 = Subjects.objects.get(lectureroom_id_id = lec_id,subjects_start_time__lte=nowtime_for_start,
                                        subjects_stop_time__gte=nowtime_for_stop,subjects_day=w_today)                                    
    print(subjects)                                    
    subject_name = subjects.subject_name
    print(subject_name) 

    list_data = []

    
    data_small = {"subject_name":subject_name}
    list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def get_student_check(request):
    print("tjdrhd1")
    subject = request.POST.get("subject_data")
    print(subject)
    try :
        print("과목받기 성공")
        subject_model = Subjects.objects.get(subject_name = subject)
        print("과목받기 성공")
        subject_id_for = subject_model.id
        print("과목받기 성공")
        atten_model1 = Attendance.objects.get(subject_id =subject_id_for,attendance_date = datetime.date.today())
        atten_model=atten_model1.id
        print(atten_model)

        atten_re_model = AttendanceReport.objects.filter(attendance_id_id = atten_model)
        print("출석리포트")
        list_data = []
        for student in atten_re_model:
            data_small={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name, "name1":student.student_id.admin.last_name, "status":student.status,}
            list_data.append(data_small)
            print("동작성공")

        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
    except:
        list_data = []
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
   
    