
from django.urls import path
from Student import views as Student_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', Student_view.student_dashboard,name="student_dashboard"),   
    path('attendance/', Student_view.attendance,name="student__student_attendance"),   
    path('student_due/', Student_view.student_due,name="student__student_due"),    
    path('student__fees_dashboard/', Student_view.student_fees,name="student__fees_dashboard"),    
    path('result_dashboard/', Student_view.result_dashboard,name="student__result_dashboard"),     
    path('notification_list/', Student_view.notification_list,name="student__notification_list"),      
    path('web_notification_details/<int:id>', Student_view.web_notification_details,name="student__web_notification_details"),      
]
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)