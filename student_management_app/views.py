# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
from .forms import AddStudentForm
from student_management_app.EmailBackEnd import EmailBackEnd
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from student_management_app.models import CustomUser, LectureRoom, Staffs, Courses, StudentResult, Subjects, Students, SessionYearModel, FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport
def home(request):
    return render(request, 'index.html')

def loginPage(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_home')
                
            elif user_type == '2':
                # return HttpResponse("Staff Login")
                return redirect('staff_home')
                
            elif user_type == '3':
                # return HttpResponse("Student Login")
                return redirect('student_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('login')

def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


#def error_404(request,exception):
 #   return render(request,'error.html')

def register(request):
    form = AddStudentForm()
    context = {
        "form": form
    }
    return render(request, 'register.html', context)


def register_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('register')
    else:
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            print(form.is_valid())
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            session_year_id = form.cleaned_data['session_year_id']
            course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
     
            else:
                profile_pic_url = None


            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
                #user = CustomUser.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, user_type=3)
                course_obj = Courses.objects.get(id=course_id)
                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj
                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year_obj
                user.students.address = address
                user.students.gender = gender
                user.students.profile_pic = profile_pic_url
                #user.email = form.cleaned_data.get('email',None)
                user.save()
                a=user.save()
                messages.success(request, "Student Added Successfully!")
                return redirect('register')
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect('register')
        else:
            return redirect('register')

# 오류 페이지 error페이지로 연결
def error400(request,exception):
    return render(request, 'error_template/error400.html')

def error401(request,exception):
    return render(request, 'error_template/error401.html')

def error402(request,exception):
    return render(request, 'error_template/error402.html')  

def error403(request,exception):
    return render(request, 'error_template/error403.html')      

def error404(request,exception):
    return render(request, 'error_template/error404.html')

def error500(request):
    return render(request, 'error_template/error500.html')