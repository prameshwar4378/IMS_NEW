from django.shortcuts import render
from django.contrib.auth import login as authlogin, authenticate,logout as DeleteSession
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import Custom_Institute_Creation_Form,login_form,Custom_Institute_Update_Form
from django.contrib import messages
from Institute.forms import CustomStaffCreationForm
from Developer.models import CustomUser
import csv

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    lg_form=login_form() 
    rg_form=Custom_Institute_Creation_Form()
    if request.method=='POST':
        if 'txt_sign_in_username' in request.POST: 
            username = request.POST.get('txt_sign_in_username', False)
            password = request.POST.get('txt_sign_in_password', False)
            user=authenticate(request,username=username,password=password)
            if user is not None:
                authlogin(request,user)
                if user.is_superuser==True:
                    return redirect('/Developer',{'user',user})
                elif user.is_institute==True:
                    return redirect('/Institute',{'user',user})
                elif user.is_staff==True:
                    return redirect('/Staff',{'user',user})
                elif user.is_student==True:
                    return redirect('/Student',{'user',user})
            else:
                lg_form=login_form()
                messages.warning(request,'Opps...! User does not exist... Please try again..!')


        if 'txt_sign_up_username' in request.POST:  
            username = request.POST.get('txt_sign_up_username', False)
            email = request.POST.get('txt_sign_up_email', False)
            password = request.POST.get('txt_sign_up_password', False)

            request.session['get_session_password']=request.POST.get('txt_sign_up_password'),
            
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request,'Username already exists!')
            else:
                create_user = CustomUser(
                    username=username,
                    email=email,
                    is_institute=True,
                )
                create_user.set_password(password)
                create_user.save() 
                messages.success(request,'Registration Successfully ...!')
                
                # Authenticate and login the user
                user = authenticate(username=username, password=password)
                if user is not None:
                    authlogin(request, user)

                # Redirect the user to the appropriate page
                return redirect('/Institute/first_tour',{'user',user})
    return render(request,'login.html',{'form':lg_form,'rg_form':rg_form})


def logout(request):
    DeleteSession(request)
    return redirect('/accounts/login')

def home(request):
    return render(request,'developer_dashboard.html')

def institute_list(request):
    rec=CustomUser.objects.filter(is_institute=True)
    return render(request,'institute_list.html', {'rec': rec})

import time
def add_institute(request):
    if request.method == 'POST':
        form = Custom_Institute_Creation_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Institute Added Successfully ...!')
            return redirect('/Developer/add_institute/')
    else:
        form = Custom_Institute_Creation_Form()
    return render(request, 'add_institute.html', {'form': form})
 
def update_institute(request,id):
    if request.method=="POST":
        pi=CustomUser.objects.get(pk=id)
        fm=Custom_Institute_Update_Form(request.POST,request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Notification Updated Successfully')
            return redirect('/Developer/institute_list/')
    else:
        pi=CustomUser.objects.get(pk=id)
        fm=Custom_Institute_Update_Form(instance=pi)
    return render(request,'update_institute.html',{'form':fm})

      
 
def delete_institute(request,id):
        pi=CustomUser.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Institute Deleted Successfully!!!')
        return redirect('/Developer/institute_list/')

from Developer import import_export

def import_export(request):
    if request.method == "POST":  
        if 'institute_import' in request.FILES: 
            csv_file = request.FILES['institute_import']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            for i in decoded_file:
                print(i)
            reader = csv.DictReader(decoded_file)
            for row in reader:
                try:
                    CustomUser.objects.create(
                        username=row['username'],
                        academic_session=row['academic_session'],
                        institute_name=row['institute_name'],
                        institute_address=row['institute_address'],
                        institute_code=row['institute_code']
                    )
                except Exception as e:
                    return redirect('/')
                
    return render(request,'import_export.html')
