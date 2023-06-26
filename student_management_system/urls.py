from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from student_management_system import settings
from django.conf import settings
#from student_management_app.views import error404,error500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('student_management_app.urls')),
    path('',include('detectme.urls')),
    path('',include('recognition.urls')),
      
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'student_management_app.views.error400'
handler404 = 'student_management_app.views.error401'
handler404 = 'student_management_app.views.error402'
handler404 = 'student_management_app.views.error403'
handler404 = 'student_management_app.views.error404'
handler500 = 'student_management_app.views.error500'

