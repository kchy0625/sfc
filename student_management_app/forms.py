from pickle import TRUE
from django import forms 
from django.forms import Form
from student_management_app.models import Courses, CustomUser, LectureRoom, SessionYearModel, Subjects


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    email = forms.EmailField(label="이메일", max_length=50,required=True,widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="비밀번호", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="힉번", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="이름", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="사용자이름", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="주소", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    

    
    #For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
       
    except:
        course_list = []
    
    #For Displaying Session Years
    # try:
    #     session_years = SessionYearModel.objects.all()
    #     session_year_list = []
    #     for session_year in session_years:
    #         single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
    #         session_year_list.append(single_session_year)
        
    # except:
    #     session_year_list = []
    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    
    course_id = forms.ChoiceField(label="학과", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="성별", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=True, widget=forms.FileInput(attrs={"class":"form-control"}))

   

class EditStudentForm(forms.Form):
    email = forms.EmailField(label="이메일", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="학번", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="이름", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="주소", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        course_list = []

    #For Displaying Session Years
    # try:
    #     session_years = SessionYearModel.objects.all()
    #     session_year_list = []
    #     for session_year in session_years:
    #         single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
    #         session_year_list.append(single_session_year)
            
    # except:
    #     session_year_list = []

    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    
    course_id = forms.ChoiceField(label="Course", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))


#요일 받는거 
class subjectForm(forms.Form):
    Subjects_day = forms.ChoiceField(label="subjects_day",widget=forms.Select(attrs={"class":"form-control"}))
    subject_start_time = forms.ChoiceField(label = "subjects_start_time",widget = forms.DateInput(attrs = {"class":"form-contorl"}))
    subject_start_time = forms.ChoiceField(label = "subjects_stop_time",widget = forms.DateInput(attrs = {"class":"form-contorl"}))

    try:
        lecturerooms = LectureRoom.objects.all()
        lectureroom_list = []
        for lectureroom in lecturerooms:
            single_lectureroom = (lectureroom.id, lectureroom.lectureroom_name)
            lectureroom_list.append(single_lectureroom)

    except:
        lectureroom_list = []


    lectureroom_id = forms.ChoiceField(label="lectureroom", choices=lectureroom_list, widget=forms.Select(attrs={"class":"form-contorl"}))

class StaffForm(forms.Form):
    try:
        subjectes = Subjects.objects.all()
        subjects_list = []
        for subjects in subjectes:
            single_subjects = (subjects.id, subjects.subjects_name)
            subjects_list.append(single_subjects)

    except:
        subjects_list = []

    subject_id = forms.ChoiceField(label="subject", choices=subjects_list, widget=forms.Select(attrs={"class":"form-contorl"}))      