from .import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('',views.index),
    path('register/',views.register),
    path('login/',views.login),
    path('student_home/',views.student_home),
    path('admin_home/',views.admin_home),
    path('event_notification/',views.event_notification),
    path('edit_event_notification/<int:id>/',views.edit_event_notification),
    path('delete_event_notification/<int:id>/', views.delete_event_notification,),
    path('student_event/',views.student_event),
    path('sent_notes/',views.sent_notes),
    path('edit_notes/<int:id>/',views.edit_notes),
    path('delete_notes/<int:id>/', views.delete_notes,), 
    path('students_view/',views.students_view),
    path('students_reply/<int:id>/',views.students_reply),
    path('student_profile/', views.student_profile),
    path('student_edit_profile/',views.student_edit_profile),    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)