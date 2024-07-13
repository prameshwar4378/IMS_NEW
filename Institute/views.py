from django.shortcuts import render, redirect
from .forms import CustomStaffCreationForm,Form_Financial_Year_Session,CustomStaffUpdateForm
from django.contrib import messages
from Developer.models import DB_Session,CustomUser
from django.contrib.auth.decorators import login_required, user_passes_test
import random

from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here.


################### Custom Decorator Start ####################

def is_institute(user):
    return user.is_authenticated and hasattr(user, 'is_institute') and user.is_institute

def institute_required(view_func):
    decorated_view_func = login_required(user_passes_test(is_institute, login_url='/accounts/login/')(view_func))
    return decorated_view_func

def profile_completed_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_institute_profile_completed:
            messages.warning(request,"Please Complete Your Profile")
            return redirect('/Institute/complete_your_profile')  # Redirect to complete profile page
        return view_func(request, *args, **kwargs)
    return wrapper


################### Custom Decorator End ####################

@institute_required 
@profile_completed_required
def update_academic_session(request):
    name=request.user.username
    user = CustomUser.objects.get(username=name)
    user.save()
    if request.method == 'POST':
            academic_session = request.POST.get('cmb_update_academic_session')
            user.academic_session = academic_session
            user.save()
            messages.success(request, 'Session Updated Success...!.')
    return redirect('/Institute/')
 

@institute_required
@profile_completed_required
def home(request): 
    # code for update session common for all function start
    if request.method=="POST":
        if 'cmb_update_academic_session' in request.POST:
            update_academic_session(request)
            return redirect('/Institute')
    # code for update session common for all function End
    return render(request,'institute_dashboard.html')

 
@institute_required
@profile_completed_required
def staff_list(request):
        # code for update session common for all function start
    if request.method=="POST":
        if 'cmb_update_academic_session' in request.POST:
            update_academic_session(request)
            return redirect('/Institute/staff_list')
    # code for update session common for all function End
    rec=CustomUser.objects.filter(is_staff=True, institute_code=request.user.institute_code,is_superuser=False)
    return render(request,'staff_list.html',{'rec':rec})


@institute_required
@profile_completed_required
def add_staff(request):
    # code for update session common for all function start
    if request.method=="POST":
        if 'cmb_update_academic_session' in request.POST:
            update_academic_session(request)
            return redirect('/Institute/add_staff')
    # code for update session common for all function End
    
    staff_count=CustomUser.objects.filter(academic_session=request.user.academic_session,institute_code=request.user.institute_code,is_staff=True).count()
    staff_number=int(staff_count)+1
    staff_id=request.user.institute_code + "-EMP-" + str(staff_number)
    
    if request.method == 'POST':
        form = CustomStaffCreationForm(request.POST, request.FILES)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.institute_name = request.user.institute_name
            fm.institute_address = request.user.institute_address
            fm.institute_logo = request.user.institute_logo
            fm.institute_code = request.user.institute_code
            fm.save()
            form = CustomStaffCreationForm()
            messages.success(request,'Staff Added Successfully...!')
            return redirect('/Institute/add_staff/')
    else:
        form = CustomStaffCreationForm()
    return render(request,'add_staff.html', {'form': form,'staff_id':staff_id})


@institute_required
@profile_completed_required
def manage_session(request):
    rec=DB_Session.objects.filter()
    if request.method == 'POST':
        form = Form_Financial_Year_Session(request.POST)
        if form.is_valid():
            form.save()
            form = Form_Financial_Year_Session()
            messages.success(request,'Session Added Successfully...!')
            return redirect('/Institute/manage_session/')
    else:
        form = Form_Financial_Year_Session() 
    return render(request,'manage_session.html', {'form_add_session': form,'rec':rec})


@institute_required
@profile_completed_required
def update_session(request,id):
    if request.method=="POST":
        pi=DB_Session.objects.get(pk=id)
        fm=Form_Financial_Year_Session(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Session Updated Successfully')
            return redirect('/Institute/manage_session/')
        # return redirect('/Admin_Home/admin_vehical_records/')
    else:
        pi=DB_Session.objects.get(pk=id)
        fm=Form_Financial_Year_Session(instance=pi)
    return render(request,'update_session.html', {'form': fm})
       

@institute_required 
@profile_completed_required
def delete_session(request,id):
        pi=DB_Session.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Session Deleted Successfully!!!')
        return redirect('/Institute/manage_session/')


@institute_required
@profile_completed_required
def update_staff(request,id):
    # code for update session common for all function start
    if request.method=="POST":
        if 'cmb_update_academic_session' in request.POST:
            update_academic_session(request)
            return redirect('/Institute/staff_list')
    # code for update session common for all function End

    if request.method=="POST":
        pi=CustomUser.objects.get(pk=id)
        fm=CustomStaffUpdateForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect('/Institute/staff_list')
        # return redirect('/Admin_Home/admin_vehical_records/')
    else:
        pi=CustomUser.objects.get(pk=id)
        fm=CustomStaffUpdateForm(instance=pi)
    return render(request,'update_staff.html', {'form': fm})
       

@institute_required      
@profile_completed_required
def delete_staff(request,id):
        pi=CustomUser.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Profile Deleted Successfully!!!')
        return redirect('/Institute/staff_list')

@institute_required
def first_tour(request):
    if request.user.tour_is_completed:
        return redirect('/Institute') 
    return render(request,'first_tour.html')

@institute_required
def complete_first_tour(request): 
    user = CustomUser.objects.get(id=request.user.id)
    user.tour_is_completed = True
    user.save()
    messages.success(request, 'Tour Completed Success...!.')
    return redirect('/Institute')

@institute_required
def complete_your_profile(request):
    # code for update session common for all function start
    if request.method=="POST":
        if 'cmb_update_academic_session' in request.POST:
            update_academic_session(request)
            return redirect('/Institute/staff_list')
    # code for update session common for all function End

    username=request.user.username
    random_letters = random.sample(username, 2)
    auto_generate_institute_code = ''.join(random_letters).upper() + str("-") + str(10)

    if request.method == 'POST':
            institute_name = request.POST.get('txt_institute_name')
            institute_address = request.POST.get('txt_institute_address')
            institute_code = request.POST.get('txt_institute_code')
            institute_logo = request.FILES.get('txt_institute_logo')
            institute_code_exist=CustomUser.objects.filter(institute_code=auto_generate_institute_code).exists()
            if institute_code_exist:
                messages.warning(request,"Institute Code is alredy Exist")
            else:
                user = CustomUser.objects.get(id=request.user.id)
                user.institute_name = institute_name
                user.institute_address = institute_address
                user.institute_code = institute_code
                user.institute_logo = institute_logo
                user.is_institute_profile_completed=True
                user.save()
                
                # Email Templates Start 
                # subject = 'Registration Successfully ...!'
                # from_email = 'prameshwar437@gmail.com'
                # recipient_list = [request.user.email]

                # username=request.user.username
                # if 'get_session_password' in request.session and request.session['get_session_password']:
                #     password_in_session = request.session['get_session_password'][0]
                # else:
                #     password_in_session = "----"
                # password = '****' + str(password_in_session[-4:])
                # html_message = render_to_string('registration_complete_email_template.html', {'username':username,'password_in_session':password,'institute_name':institute_name})
                # send_mail(
                #     subject=subject,
                #     message='Congratulations for registred IMS',
                #     from_email=from_email,
                #     recipient_list=recipient_list,
                #     html_message=html_message,
                # )

                messages.success(request, 'Profile Updated Success...!.')
                return redirect('/Institute/')
    return render(request,'complete_your_profile.html',{'auto_generate_institute_code':auto_generate_institute_code})
