
from django.urls import path
from Institute import views as Institute_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Institute_view.home,name="institute_dashboard"),  
    path('staff_list/', Institute_view.staff_list,name="staff_list"),  
    path('complete_your_profile/', Institute_view.complete_your_profile,name="complete_your_profile"), 
    path('staff_list/', Institute_view.staff_list,name="staff_list"), 
    path('add_staff/', Institute_view.add_staff,name="add_staff"),  
    path('manage_session/', Institute_view.manage_session,name="manage_session"),   
    path('delete_session/<int:id>', Institute_view.delete_session,name="delete_session"),    
    path('update_staff/<int:id>', Institute_view.update_staff,name="update_staff"),   
    path('delete_staff/<int:id>', Institute_view.delete_staff,name="delete_staff"),    
    path('first_tour/', Institute_view.first_tour,name="first_tour"),    
    path('complete_first_tour/', Institute_view.complete_first_tour,name="complete_first_tour"),    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

    