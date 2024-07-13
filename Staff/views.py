from django.shortcuts import render,get_object_or_404,redirect
from .forms import CustomStudentCreationForm,Form_academic_session,Form_Subject,Form_Schedule_Exam,Create_Web_Notification_Form,CustomStudentUpdateForm
from Developer.models import CustomUser,DB_Fees,DB_Session,DB_Result,DB_Subjects,DB_Schedule_Exam,DB_Attendance,DB_Web_Notification
from Staff.forms import FormStudentReceivedFees,FormAddFees,AttendanceForm,UpdateAttendanceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from django.db.models import Sum
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa 
from .filters import DueFees_Filter,Student_name_Filter,Attendance_Filter
from . import export
from django.forms import formset_factory
from datetime import date
import requests

def send_received_fees_sms(auth_key, mobiles, message, sender, route, unicode, pe_id, template_id):
    url = 'http://apitxt.com/api/sendMsg'
    payload = {
        'authkey': auth_key,
        'mobiles': mobiles,
        'message': message,
        'sender': sender,
        'route': route,
        'unicode': unicode,
        'pe_id': pe_id,
        'template_id': template_id
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return True
    else:
        return False


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def update_academic_session(request):
    name=request.user.username
    user = CustomUser.objects.get(username=name)
    user.save()
    fm=Form_academic_session()
    if request.method == 'POST':
            my_field_value = request.POST.get('academic_session')
            user.academic_session = my_field_value
            user.save()
            messages.success(request, 'Session Updated Success...!.')
            return redirect('/Staff')

    contaxt={'name':name,'form':fm}
    return render(request,'staff__update_education_session.html',contaxt)



@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def staff_dashboard(request):
    today = date.today()
    student_records=CustomUser.objects.filter(is_student=True,date_time__date=today,academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    today_admission=student_records.count()

    fees_records=DB_Fees.objects.filter(date_time__date=today,received_amount__isnull=False,academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    total_fees=0
    for i in fees_records:
        total_fees+=int(i.received_amount)

    total_present_students=DB_Attendance.objects.filter(date_time__date=today,is_present=True,academic_session=request.user.academic_session,institute_code=request.user.institute_code).count()
    total_students=CustomUser.objects.filter(is_student=True,academic_session=request.user.academic_session,institute_code=request.user.institute_code).count()
    if total_students > 0:
        present_student_in_percentage=(total_present_students/total_students)*100
    else:
        present_student_in_percentage=0
    
    allocated_fees_DB=DB_Fees.objects.filter(add_fees__isnull=False,academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    total_allocated_fees=0
    for i in allocated_fees_DB:
        total_allocated_fees+=int(i.add_fees)
    collected_fees_DB=DB_Fees.objects.filter(received_amount__isnull=False,academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    total_collected_amount=0
    for i in collected_fees_DB:
        amount=i.received_amount
        total_collected_amount+=int(amount)
    total_pending_fees=total_allocated_fees-total_collected_amount
    label_expenses=['Allocated Fees','Collected Fees','Pending_fees']
    data_expenses=[total_allocated_fees,total_collected_amount,total_pending_fees]

    student_data_male_for_charts=CustomUser.objects.filter(is_student=True,academic_session=request.user.academic_session,institute_code=request.user.institute_code,student_gender="Male").count()
    student_data_female_for_charts=CustomUser.objects.filter(is_student=True,academic_session=request.user.academic_session,institute_code=request.user.institute_code,student_gender="Female").count()
    label_active_students=['Male','Female']
    data_active_students=[student_data_male_for_charts,student_data_female_for_charts]

    exam_schedule_records=DB_Schedule_Exam.objects.filter(academic_session=request.user.academic_session,institute_code=request.user.institute_code).last()
    if exam_schedule_records:
        exam_name_for_result_chart = f"{exam_schedule_records.exam_title} ({exam_schedule_records.exam_start_date} To {exam_schedule_records.exam_end_date})"
    else:
        exam_name_for_result_chart=""

    if exam_schedule_records:
        result_records=DB_Result.objects.filter(exam_title=exam_schedule_records.exam_title,institute_code=request.user.institute_code,academic_session=request.user.academic_session)
    else:
        result_records=""

    label_subject_name_result=[]
    data_marks_result=[]
    for i in result_records:
        if i.subject_name in label_subject_name_result:
            subject_index_value=label_subject_name_result.index(i.subject_name)
            data_marks_result[subject_index_value]+=int(i.obtained_marks)
        else:
            label_subject_name_result.append(i.subject_name)
            data_marks_result.append(int(i.obtained_marks)) 

    label_notification=['Active','Inactive']
    data_notification=[]
    notification_rec=DB_Web_Notification.objects.filter(academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    active=0
    inactive=0

    
    for i in notification_rec:
        if not i.notification_valid_up_to:
            active+=1
            continue
        elif today < i.notification_valid_up_to:
            active+=1
        elif today > i.notification_valid_up_to:
            inactive+=1
    data_notification.append(active)
    data_notification.append(inactive)

 
    context={
            'today_admission':today_admission,
            'total_fees':total_fees,
            'total_present_students':total_present_students,
            'present_student_in_percentage':present_student_in_percentage,
            'total_allocated_fees':total_allocated_fees,
            'total_collected_amount':total_collected_amount,
            'total_pending_fees':total_pending_fees,
            'labels_charts_expenses':label_expenses,
             'data_charts_expenses':data_expenses,
             'label_active_students':label_active_students,
             'data_active_students':data_active_students,
            'exam_name_for_result_chart':exam_name_for_result_chart,
            'label_subject_name_result':label_subject_name_result,
            'data_marks_result':data_marks_result,
            'label_notification':label_notification,
            'data_notification':data_notification,
             }
    return render(request,'staff__staff_dashboard.html',context)



@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def student_fees_list(request):
    rec=CustomUser.objects.filter(is_student=True,status="Active",academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    return render(request,'staff__student_fees_list.html',{'rec':rec})

@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def new_admission(request):
    session_student=request.user.academic_session
    record=CustomUser.objects.filter(academic_session=session_student,is_student=True,institute_code=request.user.institute_code)
    if record.count()==0:
        student_count="1"
    else:
        student_count=str(record.count()+1)
    split_session1=session_student[-5:-3]
    split_session2=session_student[-2:]
    institute_code=request.user.institute_code
    prn_no=institute_code+str('-')+split_session1+split_session2+str("0")+str("0")+student_count

    if request.method == 'POST':
        form = CustomStudentCreationForm(request.POST, request.FILES)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.institute_name = request.user.institute_name
            fm.institute_address = request.user.institute_address
            fm.institute_logo = request.user.institute_logo
            fm.institute_code = request.user.institute_code
            form.save()
            messages.success(request, 'Registration Successfully...!.')
            form = CustomStudentCreationForm()
            return redirect('/Staff/new_admission/')
    else:
        form = CustomStudentCreationForm()
    return render(request,'staff__admission_form.html', {'form': form,'academic_session':session_student,'auto_prn':prn_no})

 

@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def student_fees_dashboard(request,id):
    dt=get_object_or_404(CustomUser,id=id)
    prn_no=dt.student_prn_no
    rec = DB_Fees.objects.filter(student_prn_no=prn_no)

    total_fees=0
    collected_fees=0 
    pending_dues=0  
    for i in rec:
        if i.add_fees != None:
            total_fees+=i.add_fees
        if i.received_amount != None:
            collected_fees += int(i.received_amount)
        if i.due_amount != None:
            pending_dues += int(i.due_amount)
            print("Due Amount is",i.due_amount)
 
    total_pending=total_fees - collected_fees
    
    form_receive_fees = FormStudentReceivedFees()
    form_add_fees = FormAddFees()

    if request.method == 'POST':
        if 'received_amount' in request.POST:
            form_receive_fees = FormStudentReceivedFees(request.POST)
            if form_receive_fees.is_valid():
                fm1 = form_receive_fees.save(commit=False)
                fm1.institute_code = request.user.institute_code
                fm1.academic_session = request.user.academic_session
                form_receive_fees.save()
                messages.success(request, 'Fees Received Successfully...!')
                
                name = dt.student_name
                print(name)
                print(name)
                print(name)
                installment_number = 3
                amount = request.POST.get('received_amount') 
                sender_name = "IMS"
                message = f"Dear {name}, You have successfully paid {installment_number} installment of amount Rs.{amount}.00. Happy Learning...! Thanks and Regards, {sender_name} - PWRDAS"


                auth_key = "UGNyZ0o1SmJQd0NVTjBETzB5Z2pydz09"
                mobiles = dt.student_mobile
                print(mobiles)
                print(mobiles)
                print(mobiles)
                message = message
                sender = "PWRDAS"
                route = "4"
                unicode = "0"
                pe_id = "1701163403601611113"
                template_id = "1707163436871688505"
                send_received_fees_sms(auth_key, mobiles, message, sender, route, unicode, pe_id, template_id)
                form_receive_fees = FormStudentReceivedFees()
                return redirect(f'/Staff/student_fees_dashboard/{id}')
        
        elif 'add_fees' in request.POST:
            form_add_fees = FormAddFees(request.POST)
            if form_add_fees.is_valid():
                fm = form_add_fees.save(commit=False)
                fm.student_class = dt.student_class
                fm.academic_session = request.user.academic_session
                fm.institute_code = request.user.institute_code
                form_add_fees.save()
                messages.success(request, 'Fees Added Successfully...!')
                form_add_fees = FormAddFees()
                return redirect(f'/Staff/student_fees_dashboard/{id}')
          
        elif 'txt_update_allocated_fees' in request.POST:
                allocated_id = request.POST.get('txt_update_allocated_id')
                allocated_fees = request.POST.get('txt_update_allocated_fees')
                allocated_fees_remark = request.POST.get('txt_update_allocated_fees_remark')
                print(allocated_id)
                print(allocated_fees)
                print(allocated_fees_remark)
                DB_Fees.objects.filter(id=allocated_id).update(add_fees=allocated_fees, fees_remark=allocated_fees_remark)
                messages.success(request, 'Fees Updated Successfully...!')
                return redirect(f'/Staff/student_fees_dashboard/{id}')
  
    else:
        form_receive_fees = FormStudentReceivedFees()
        form_add_fees = FormAddFees()

    context ={'fees_form':form_receive_fees,'add_fees_form':form_add_fees,'data':dt,'fees_rec':rec,'total_fees':total_fees,'collected_fees':collected_fees,'pending_dues':pending_dues,'total_pending':total_pending}

    return render(request,"staff__student_fees_dashboard.html",context )




@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def update_student_profile(request,id):
    if request.method=="POST":
        pi=CustomUser.objects.get(pk=id)
        fm=CustomStudentUpdateForm(request.POST,request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect('/Staff/new_admission/')

        # return redirect('/Admin_Home/admin_vehical_records/')
    else:
        pi=CustomUser.objects.get(pk=id)
        fm=CustomStudentUpdateForm(instance=pi)
    return render(request,'staff__update_student_profile.html',{'form':fm})


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def delete_student(request,id):
        pi=CustomUser.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Profile Deleted Successfully!!!')
        return redirect('/Staff/student_fees_list/')



@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def delete_fees_record(request,id):
        dt=get_object_or_404(DB_Fees,id=id)
        user=dt.student_username
        var_username = CustomUser.objects.get(username=user)
        student_id=var_username.id
        pi=DB_Fees.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Record Deleted Successfully!!!')
        return redirect(f'/Staff/student_fees_dashboard/{student_id}')
        

@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def print_admission_form(request,id):
    dt=get_object_or_404(CustomUser,id=id)
    return render(request,"staff__print_admission_form.html",{'id':id,'data':dt})

 
def print_fees_receipt(request,id):
    dt=get_object_or_404(DB_Fees,id=id)
    institute_details=get_object_or_404(CustomUser,student_prn_no=dt.student_prn_no)
    return render(request,"staff__print_fees_receipt.html",{'data':dt,'institute_details':institute_details})


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def due_list(request):
    due_records=DB_Fees.objects.filter(due_amount__isnull=False, due_amount__gt=0, academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    Filter=DueFees_Filter(request.GET, queryset=due_records)
    rec2=Filter.qs 
    total_students=rec2.count()
    total_value = rec2.aggregate(Sum('due_amount'))
    total_due_amount = str(total_value['due_amount__sum'])
    context={'rec':rec2,'filter':Filter,'total_students':total_students,'total_due_amount':total_due_amount}
    return render(request,"staff__due_list.html",context)

@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def due_update(request,id):
    rec=DB_Fees.objects.get(pk=id)
    student_profile=CustomUser.objects.get(student_prn_no=rec.student_prn_no)
    student_id_for_dashboard=student_profile.id
    if request.method=="POST":
        pi=DB_Fees.objects.get(pk=id)
        fm=FormStudentReceivedFees(request.POST,request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Fees Updated Successfully')
            return redirect(f'/Staff/student_fees_dashboard/{student_id_for_dashboard}')
    else:
        pi=DB_Fees.objects.get(pk=id)
        fm=FormStudentReceivedFees(instance=pi)
    return render(request,"staff__update_due_record.html",{'form':fm})


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def due_clear(request,id):
    today=date.today()
 

    DB_Fees.objects.filter(id=id).update(
        due_date=None,
        due_amount=None,
        due_remark=None
    )
 
    record=DB_Fees.objects.filter(id=id)
    for i in record:
        student_username=i.student_username
        operator_username=i.operator_username
        operator_name=i.operator_name
        payment_mode=i.payment_mode
        student_class=i.student_class
        received_date=today
        received_amount=i.received_amount
        received_remark=i.received_remark
        academic_session=request.user.academic_session
        student_name=i.student_name
        student_prn_no=i.student_prn_no
        institute_code=i.institute_code 

    insert_rec=DB_Fees(
        student_username=student_username,
        operator_username=operator_username,
        operator_name=operator_name,
        payment_mode=payment_mode,
        student_class=student_class,
        received_date=received_date,
        received_amount=received_amount,
        received_remark=received_remark + " - From Due",
        academic_session=academic_session,
        student_name=student_name,
        student_prn_no=student_prn_no,
        institute_code=institute_code,
    )
    insert_rec.save()
    
    messages.success(request,'Due has cleared and Amount added to the student profile') 
    return redirect('/Staff/due_list') 

@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def export_pdf_deu_records(request):
    responce = export.export_pdf_due(request)
    return responce


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def export_excel_deu_records(request):
    responce = export.export_excel_deu(request)
    return responce

@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def manage_subjects(request):
    rec=DB_Subjects.objects.filter(institute_code=request.user.institute_code)
    form=Form_Subject()
    if request.method=="POST":
        form=Form_Subject(request.POST)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.institute_code = request.user.institute_code
            form.save()
            messages.success(request,'Subject Added Successfully')
            form=Form_Subject()
            return redirect('/Staff/manage_subjects/')
    else:
        form=Form_Subject()
    context={'form':form,'rec':rec}
    return render(request,'staff__subjects.html',context)


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def delete_subject(request,id):
        pi=DB_Subjects.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Subject Deleted Successfully!!!')
        return redirect('/Staff/manage_subjects/')


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def student_result_list(request):
    rec=CustomUser.objects.filter(is_student=True,status="Active",academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    return render(request,'staff__student_result_list.html',{'rec':rec})


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def student_result_dashboard(request,id):
    student_profile_record=CustomUser.objects.get(id=id)
    result_record=DB_Result.objects.filter(student_prn_no=student_profile_record.student_prn_no,academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    exam_name = DB_Schedule_Exam.objects.filter(class_name=student_profile_record.student_class,academic_session=request.user.academic_session,institute_code=request.user.institute_code).order_by('-id')

    # student_name=student_record.student_name
    if request.method == 'POST':
        # Get data from POST request
        if 'add_result' in request.POST: 
            academic_session = request.POST.get('add_academic_session')
            student_class = request.POST.get('student_class')
            student_prn_no = request.POST.get('student_prn_no')
            subject_name = request.POST.get('subject_name')
            min_marks = request.POST.get('min_marks')
            obtained_marks = request.POST.get('obtained_marks')
            out_off_marks = request.POST.get('out_off_marks')
            percentage = request.POST.get('percentage')
            result = request.POST.get('result')
            exam_data = request.POST.get('cmb_exam_name')
            exam_title, exam_start_date, exam_end_date = exam_data.split(" | ")

            if DB_Result.objects.filter(academic_session=academic_session,student_prn_no=student_prn_no,institute_code=request.user.institute_code,subject_name=subject_name,exam_title=exam_title, exam_start_date=exam_start_date, exam_end_date=exam_end_date).exists():
                messages.info(request,'Record alredy exist You can update the Reocord !!!')
            else:
                save_result = DB_Result(
                    academic_session=academic_session,
                    institute_code=request.user.institute_code,
                    student_prn_no=student_prn_no,
                    subject_name=subject_name,
                    student_class=student_class,
                    min_marks=min_marks,
                    obtained_marks=obtained_marks,
                    out_off_marks=out_off_marks,
                    percentage=percentage,
                    result=result,
                    exam_title=exam_title,
                    exam_start_date=exam_start_date,
                    exam_end_date=exam_end_date,
                )
                save_result.save()
                messages.success(request,'Marks Added Successfully!!!')
        elif 'txt_update_result_id' in request.POST: 
            result_id = request.POST.get('txt_update_result_id')
            update_exam_data = request.POST.get('cmb_update_exam_name')
            update_exam_title, update_exam_start_date, update_exam_end_date = update_exam_data.split(" | ")
        
            # Select the record with the given ID and update its fields
            DB_Result.objects.filter(id=result_id).update(
                academic_session=request.POST.get('txt_update_academic_session'),
                institute_code=request.user.institute_code,
                student_prn_no=request.POST.get('txt_update_student_prn_no'),
                subject_name=request.POST.get('cmb_update_subject_name'),
                min_marks=request.POST.get('txt_update_min_marks'),
                obtained_marks=request.POST.get('txt_update_obtained_marks'),
                out_off_marks=request.POST.get('txt_update_out_off_marks'),
                percentage=request.POST.get('txt_update_percentage'),
                result=request.POST.get('txt_update_result'),
                exam_title=update_exam_title,
                exam_start_date=update_exam_start_date,
                exam_end_date=update_exam_end_date 
            )
            messages.success(request, 'Marks Updated Successfully!!!')
        elif 'report_type' in request.POST:
            report_type=request.POST.get('report_type')
            if report_type == "Subject Wise":
                subject_name_1=request.POST.get('select_subject_for_report')
                student_prn_no=student_profile_record.student_prn_no
                responce = export.export_result_report_subject_wise(request,subject_name_1,student_prn_no)
                return responce

            elif report_type == "Exam Wise":
                exam_name_1=request.POST.get('select_exam_for_report')
                title_1, start_date_1, end_date_1 = exam_name_1.split(" | ")
                st_name=student_profile_record.student_name
                st_prn=student_profile_record.student_prn_no

                result_data = DB_Result.objects.filter(exam_title=title_1,exam_start_date=start_date_1,exam_end_date=end_date_1)
                
                if result_data:
                    student_class = result_data.first().student_class
                    st_class=student_class


                labels_charts = []
                data_charts = []
                st_total_obtained=0
                st_total_out_off=0
                st_total_min=0
                st_result=[]
                for i in result_data:
                    labels_charts.append(i.subject_name)
                    data_charts.append(i.obtained_marks)
                    st_total_obtained+=int(i.obtained_marks)
                    st_total_out_off+=int(i.out_off_marks)
                    st_total_min+=int(i.min_marks)
                    st_result.append(i.result)

                if "Fail" in st_result:
                    st_result="Fail"
                else:
                    st_result="Pass"

                if st_total_out_off >0:
                    st_percentage=(st_total_obtained/st_total_out_off)*100
                else:
                    st_percentage="---"
                    
                st_profile=student_profile_record.student_profile
                institute_name=student_profile_record.institute_name
                institute_logo=student_profile_record.institute_logo
                institute_address=student_profile_record.institute_address


                context={'rec':result_data,
                         'st_profile':st_profile,
                         'st_name':st_name,
                         'institute_name':institute_name,
                         'institute_logo':institute_logo,
                         'institute_address':institute_address,
                         'st_prn':st_prn,
                         'st_class':st_class,
                         'exam_title':title_1,
                         'exam_start_date':start_date_1,
                         'exam_end_date':end_date_1,
                         'st_total_min':st_total_min,
                         'st_total_obtained':st_total_obtained,
                         'st_total_out_off':st_total_out_off,
                         'st_percentage':st_percentage,
                         'st_result':st_result,
                         'labels_charts':labels_charts,
                         'data_charts':data_charts,
                         }
                
                return render(request,'staff__print_result_exam_wise.html',context)
            
        return redirect('student_result_dashboard', id=id)        

    labels = []
    data_chart = []
    if result_record.count() != 0:
        for i in result_record:
            if i.subject_name not in labels:
                labels.append(str(i.subject_name))
            index_val=labels.index(i.subject_name)
            if index_val < len(data_chart):
                data_chart[index_val]=data_chart[index_val]+int(i.obtained_marks)
            else:
                data_chart.append(int(i.obtained_marks))
    subjects=DB_Subjects.objects.filter(class_name=student_profile_record.student_class,institute_code=request.user.institute_code)
    context={'subject_name':subjects,'st_data':student_profile_record,'result_record':result_record,'exam_record':exam_name,'labels':labels,'data':data_chart}
    return render(request,'staff__student_result_dashboard.html',context)



@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def delete_result(request,id):
        pi=DB_Result.objects.get(pk=id)
        id_for_page_redirect=CustomUser.objects.get(student_prn_no=pi.student_prn_no).id
        pi.delete()
        messages.success(request,'Result Deleted Successfully!!!')
        return redirect(f'/Staff/student_result_dashboard/{id_for_page_redirect}')
 

@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def schedule_exam(request):
    rec=DB_Schedule_Exam.objects.filter(academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    form=Form_Schedule_Exam()
    if request.method=="POST":
        form=Form_Schedule_Exam(request.POST)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.institute_code = request.user.institute_code
            form.save()
            messages.success(request,'Exam Created Successfully')
            form=Form_Schedule_Exam()
            return redirect('/Staff/schedule_exam/')
    else:
        form=Form_Schedule_Exam()
    context={'form':form,'rec':rec}
    return render(request,'staff__schedule_exam.html',context)


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def delete_exam_schedule(request,id):
        pi=DB_Schedule_Exam.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Exam  Deleted Successfully!!!')
        return redirect('/Staff/schedule_exam/')

 
import calendar

@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def student_attendance_list(request):
    month_names = list(calendar.month_name)
    class_name=""
    attendancea_alredy_taken=""
    attendance_records=DB_Attendance.objects.filter(academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    Filter=Attendance_Filter(request.GET, queryset=attendance_records)
    filtered_rec=Filter.qs

    Filter1=Attendance_Filter(request.GET, queryset=attendance_records)
    filter_total_attendance_rec=Filter1.qs
    total_attendance_count=Filter1.qs.count()

    Filter2=Attendance_Filter(request.GET, queryset=attendance_records.filter(is_present=True))
    present_rec_count=Filter2.qs.count()
    
    Filter3=Attendance_Filter(request.GET, queryset=attendance_records.filter(is_present=False))
    absent_rec_count=Filter3.qs.count()

    if total_attendance_count > 0:
        percentage=(present_rec_count/total_attendance_count)*100
    else:
        percentage=0

    if request.method=="POST":
        if 'txt_set_session_date' in request.POST:
            request.session['get_session_date']=request.POST.get('txt_set_session_date'),
            request.session['get_session_class']=request.POST.get('cmb_set_session_class_name'),
        
            if request.session.get('get_session_class'):
                class_name=request.session.get('get_session_class')
                for i in class_name:
                    class_name=i
                student_record=CustomUser.objects.filter(is_student=True,student_class=class_name,academic_session=request.user.academic_session,institute_code=request.user.institute_code).count()
                if student_record > 0:
                    get_date=request.POST.get('txt_set_session_date')
                    get_class=request.POST.get('cmb_set_session_class_name')
                    attedance_rec=DB_Attendance.objects.filter(attendance_date=get_date,student_class=get_class,academic_session=request.user.academic_session,institute_code=request.user.institute_code).count()
                    if attedance_rec > 0:
                        attendancea_alredy_taken="Attendance Alredy Taken"
                        return redirect('/Staff/update_attendance/')
                    else:
                        return redirect('/Staff/create_attendance/')
        elif 'cmb_month_export' in request.POST:
            class_name=request.POST.get('cmb_class_name_export'),
            month_name=request.POST.get('cmb_month_export'),
            class_name=class_name[0]
            month_name=month_name[0]
            responce=export_attendance(request,class_name,month_name)
            return responce

    labels_charts = ['Present','Absent']
    data_charts = []
    total=attendance_records.count()
    present=0
    absent=0
    for i in attendance_records:
        if i.is_present==True:
            present+=1
        else:
            absent+=1

    data_charts.append(present)
    data_charts.append(absent)
    contaxt={'class_name':class_name,
             'month_names':month_names,
             'labels_charts':labels_charts,
             'data_charts':data_charts,
             'attendancea_alredy_taken':attendancea_alredy_taken,
             'filter_total_attendance_rec':filtered_rec,
             'total_attendance_count':total_attendance_count,
             'present_rec_count':present_rec_count,
             'absent_rec_count':absent_rec_count,
             'percentage':percentage,
             'filter':Filter,
             }        
    return render(request,'staff__student_attendance_list.html',contaxt)


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def create_attendance(request):  
    session_date=request.session.get('get_session_date')
    for i in session_date:
        session_date=i        
    session_class_name=request.session.get('get_session_class')
    for i in session_class_name:
        session_class_name=i

    student_record=CustomUser.objects.filter(is_student=True,student_class=session_class_name,academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    initial_data = [{'student_name': student.student_name, 'student_prn_no': student.student_prn_no} for student in student_record]
    MyFormSet = formset_factory(AttendanceForm, extra=0)

    if request.method == 'POST':
        formset = MyFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                fm = form.save(commit=False)
                fm.student_class = session_class_name
                fm.attendance_date = session_date
                fm.academic_session = request.user.academic_session
                fm.institute_code = request.user.institute_code
                form.save()
            messages.success(request,'Attendance Submited Successfully!!!')
            return redirect('/Staff/student_attendance_list/')
    else: 
        formset = MyFormSet(initial=initial_data)
    return render(request, "staff__create_attendance.html",{'formset':formset,'date':session_date,'class_name':session_class_name,'student_record':student_record})



@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def update_attendance(request):  
    session_date=request.session.get('get_session_date')
    for i in session_date:
        session_date=i        
    session_class_name=request.session.get('get_session_class')
    for i in session_class_name:
        session_class_name=i

    student_record=DB_Attendance.objects.filter(student_class=session_class_name,attendance_date=session_date,academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    initial_data = [{'id': student.id, 'student_name': student.student_name, 'student_prn_no': student.student_prn_no,'is_present':student.is_present} for student in student_record]
    MyFormSet = formset_factory(UpdateAttendanceForm, extra=0)
 
    if request.method == 'POST':
        formset = MyFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                print(form.cleaned_data['id'])
                attendance_id = form.cleaned_data['id']
                is_present = form.cleaned_data['is_present']
                DB_Attendance.objects.filter(id=attendance_id).update(is_present=is_present)
            messages.success(request, 'Attendance updated successfully!')
            return redirect('/Staff/student_attendance_list/')
        else:
            messages.error(request,'Form not valid!!!')
    else: 
        formset = MyFormSet(initial=initial_data)
    return render(request, "staff__update_attendance.html",{'formset':formset,'date':session_date,'class_name':session_class_name,'student_record':student_record})

import csv


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def export_attendance(request,class_name,month_name):
        month_number = datetime.strptime(month_name, "%B").month # get the month number from the month name
        attendance_data = DB_Attendance.objects.filter(attendance_date__month=month_number,student_class=class_name,academic_session=request.user.academic_session,institute_code=request.user.institute_code)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
        writer = csv.writer(response)
        writer.writerow(['Academic Session', 'Student Name', 'PRN No.', 'Class', 'Attendance Date', 'Attendance Status'])
        for row in attendance_data:
            writer.writerow([row.academic_session, row.student_name, row.student_prn_no, row.student_class, row.attendance_date, row.is_present])
        return response


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def inactive_students_list(request):
    rec=CustomUser.objects.filter(is_student=True,status="Inactive",academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    return render(request,'staff__inactive_students_list.html',{'rec':rec})

@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def create_web_notification(request):
    rec=DB_Web_Notification.objects.filter(academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    today = date.today()

    total=rec.count()
    active=0
    inactive=0
    for i in rec:
        if  i.notification_valid_up_to == None:
            active+=1
            continue
        else:
            if today <= i.notification_valid_up_to:
                active+=1
            elif today > i.notification_valid_up_to:
                inactive+=1
        

    form=Create_Web_Notification_Form() 
    if request.method=="POST":
        form=Create_Web_Notification_Form(request.POST, request.FILES) 
        if form.is_valid():
            fm = form.save(commit=False)
            fm.academic_session = request.user.academic_session
            fm.institute_code = request.user.institute_code
            form.save()
            messages.success(request,'Notification triggered Successfully')
            form=Create_Web_Notification_Form()
            return redirect('/Staff/create_web_notification/')
    else:
        form=Create_Web_Notification_Form()
    context={'form':form,'rec':rec,'today':today,'active':active,'inactive':inactive,'total':total}
    return render(request,'staff__create_web_notification.html',context)



@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def delete_web_notification(request,id):
        pi=DB_Web_Notification.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Notification Deleted Successfully!!!')
        return redirect('/Staff/create_web_notification/')



@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def update_web_notification(request,id):
    if request.method=="POST":
        pi=DB_Web_Notification.objects.get(pk=id)
        fm=Create_Web_Notification_Form(request.POST,request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Notification Updated Successfully')
            return redirect('/Staff/create_web_notification/')
    else:
        pi=DB_Web_Notification.objects.get(pk=id)
        fm=Create_Web_Notification_Form(instance=pi)
    return render(request,'staff__update_web_notification.html',{'form':fm})


@user_passes_test(lambda user: user.is_staff)
@login_required(login_url='/login/')
def web_notification_details(request,id):
    dt=get_object_or_404(DB_Web_Notification,id=id)
    return render(request,"staff__web_notification_details.html",{'id':id,'data':dt})

