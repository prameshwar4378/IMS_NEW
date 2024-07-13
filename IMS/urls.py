"""Institute URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Developer import urls as Devloper_url
from Staff import urls as Staff_url
from Institute import urls as Institute_url
from Student import urls as Student_url
from Developer import views as Developer_views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', Developer_views.index, name="index"),
    path('', Developer_views.login, name="login12"),
    path('accounts/login/', Developer_views.login, name="login"),
    path('logout/', Developer_views.logout, name="logout"),
    path('Developer/',include(Devloper_url)),
    path('Institute/',include(Institute_url)),
    path('Staff/',include(Staff_url)),
    path('Student/',include(Student_url)),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
