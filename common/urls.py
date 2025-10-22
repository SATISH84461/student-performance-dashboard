from django.urls import path
from . import views

urlpatterns = [
    path('test', views.TeacherList.as_view(), name='teacher-list'),
    path('performance', views.Performance.as_view(), name='performance'),
    path('convert-file', views.TeacherList2.as_view(), name='convert-file'),
    path('performance2', views.Performance2.as_view(), name='performance2'),
    path('student-subjects', views.StudentSubjectListAPIView.as_view(), name='student-subjects'),
    path('teacher-class-results', views.TeacherClassResultsAPIView.as_view(), name='teacher-class-results'),
    path('', views.home, name='home'),
    path('upload-results', views.upload_file_view, name='upload-results'),
    path('student-result', views.student_result, name='student-result'),
    path('teacher-result', views.teacher_result, name='teacher-result'),
]