# from django.urls import path
# from . import views

# urlpatterns = [
#     path('dashboard', views.teacher_dashboard, name='teacher_dashboard'),
#     # use TeacherViewSet for CRUD operations
#     path('teachers', views.TeacherViewSet.as_view({'get': 'list', 'post': 'create'}), name='teacher_list'),
#     path('teachers/<int:pk>', views.TeacherViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='teacher_detail'),
#     # path('profile', views.techer_profile, name='teacher_profile'),
#     path('manage', views.manage_classes, name='manage_classes'),
#     path('grade', views.grade_assignments, name='grade_assignments'),
#     path('contact', views.contact_students, name='contact_students'),
#     path('create', views.create_assignment, name='create_assignment'),
#     path('schedule', views.schedule_classes, name='schedule_classes'),
# ]