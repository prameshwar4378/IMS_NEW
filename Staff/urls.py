
from django.urls import path
from Staff import views as Staff_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', Staff_view.staff_dashboard,name="staff_dashboard"),  
    path('student_fees_list/', Staff_view.student_fees_list,name="student_fees_list"), 
    path('new_admission/', Staff_view.new_admission,name="new_admission"),  
    path("student_fees_dashboard/<int:id>",Staff_view.student_fees_dashboard, name='student_fees_dashboard'), 
    path("print_admission_form/<int:id>",Staff_view.print_admission_form, name='print_admission_form'), 
    path("print_fees_receipt/<int:id>",Staff_view.print_fees_receipt, name='print_fees_receipt'),  
    path("update_student_profile/<int:id>",Staff_view.update_student_profile, name='update_student_profile'), 
    path("delete_student/<int:id>",Staff_view.delete_student, name='delete_student'), 
    path("delete_fees_record/<int:id>",Staff_view.delete_fees_record, name='delete_fees_record'), 
    path('due_list/', Staff_view.due_list, name='due_list'),
    path('due_clear/<int:id>',Staff_view.due_clear, name='due_clear'), 
    path('due_update/<int:id>', Staff_view.due_update, name='due_update'),
    path('update_academic_session/', Staff_view.update_academic_session, name='update_academic_session'),
    path('export_pdf_deu_records/', Staff_view.export_pdf_deu_records, name='export_pdf_deu_records'),
    path('export_excel_deu_records/', Staff_view.export_excel_deu_records, name='export_excel_deu_records'),
    path('manage_subjects/', Staff_view.manage_subjects, name='manage_subjects'),
    path('delete_subject/<int:id>', Staff_view.delete_subject, name='delete_subject'),
    path('student_result_list/', Staff_view.student_result_list, name='student_result_list'),  
    path('student_result_dashboard/<int:id>', Staff_view.student_result_dashboard, name='student_result_dashboard'), 
    path('delete_result/<int:id>', Staff_view.delete_result, name='delete_result'), 
    path('schedule_exam/', Staff_view.schedule_exam, name='schedule_exam'), 
    path('delete_exam_schedule/<int:id>', Staff_view.delete_exam_schedule, name='delete_exam_schedule'), 
    path('student_attendance_list/', Staff_view.student_attendance_list, name='student_attendance_list'), 
    path('create_attendance/', Staff_view.create_attendance, name='create_attendance'), 
    path('update_attendance/', Staff_view.update_attendance, name='update_attendance'), 
    path('inactive_students_list/', Staff_view.inactive_students_list, name='inactive_students_list'), 
    path('create_web_notification/', Staff_view.create_web_notification, name='create_web_notification'), 
    path('delete_web_notification/<int:id>', Staff_view.delete_web_notification, name='delete_web_notification'), 
    path('update_web_notification/<int:id>',Staff_view.update_web_notification, name='update_web_notification'), 
    path('web_notification_details/<int:id>',Staff_view.web_notification_details, name='web_notification_details'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)