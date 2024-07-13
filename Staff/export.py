from Developer.models import DB_Fees,DB_Result,CustomUser,DB_Attendance
from .filters import DueFees_Filter
from django.template.loader import get_template
from django.db.models import Sum,Q
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa 
import csv


def export_pdf_due(request): 
    template = get_template('staff__export_pdf_due_records.html')
    due_records=DB_Fees.objects.exclude(Q(due_amount__isnull=True) | Q(due_amount=0)).filter(academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    Filter=DueFees_Filter(request.GET, queryset=due_records)
    rec2=Filter.qs 
    total_value = rec2.aggregate(Sum('due_amount'))
    total_due_amount = str(total_value['due_amount__sum'])
    context={'rec':rec2,'total_due_amount':total_due_amount}
  
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Due Records.pdf"'
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), response)
    if not pdf.err:
        return response
    return HttpResponse('Error generating PDF file: %s' % pdf.err, status=400)


def export_excel_deu(request):
    responce=HttpResponse(content_type='text/csv')
    writer=csv.writer(responce)
    writer.writerow(['student_prn_no','student_name','student_class','received_date','payment_mode','received_amount','received_remark','due_date','due_amount','due_remark'])
    for data in DB_Fees.objects.filter(due_amount__isnull=False).filter(academic_session=request.user.academic_session,institute_code=request.user.institute_code).values_list('student_prn_no','student_name','student_class','received_date','payment_mode','received_amount','received_remark','due_date','due_amount','due_remark'):
       writer.writerow(data)    
    responce['Content-Disposition'] = 'attachment; filename="Student Due Records.csv"'
    return responce

def export_result_report_subject_wise(request,subject,prn):
    template = get_template('staff__export_pdf_result_subject_wise.html')
    result_records=DB_Result.objects.filter(subject_name=subject,student_prn_no=prn,academic_session=request.user.academic_session,institute_code=request.user.institute_code)
    profile_rec=CustomUser.objects.get(student_prn_no=prn,academic_session=request.user.academic_session,institute_code=request.user.institute_code)

    institute_address=profile_rec.institute_address
    institute_name=profile_rec.institute_name
    institute_logo=profile_rec.institute_logo
    student_name=profile_rec.student_name
    student_class=profile_rec.student_class
    context={
        'rec':result_records,
        "institute_address":institute_address,
        "institute_name":institute_name,
        "institute_logo":institute_logo,
        "student_name":student_name,
        "student_class":student_class,
        "student_prn_no":prn,
        "subject_name":subject
        }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Result.pdf"'
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), response)
    if not pdf.err:
        return response
    return HttpResponse('Error generating PDF file: %s' % pdf.err, status=400)



def export_attendance(request):
    academic_session = "2022-2023"  # Replace with the actual academic session value

    # Get all attendance records for the academic session
    attendance_records = DB_Attendance.objects.filter(academic_session=academic_session,institute_code=request.user.institute_code)

    # Group attendance records by month
    attendance_by_month = {}
    for record in attendance_records:
        month = record.attendance_date.strftime("%B")  # Get the month name
        if month not in attendance_by_month:
            attendance_by_month[month] = []
        attendance_by_month[month].append(record)

    # Define the CSV header and rows
    csv_header = ["Month", "Student Name", "PRN No.", "Class", "Attendance Date", "Attendance Status"]
    csv_rows = []
    for month, records in attendance_by_month.items():
        for record in records:
            row = [
                month,
                record.academic_session,
                record.student_name,
                record.student_prn_no,
                record.student_class,
                record.attendance_date.strftime("%Y-%m-%d"),
                "Present" if record.is_present else "Absent"
            ]
            csv_rows.append(row)

    # Write CSV response
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="attendance_{academic_session}.csv"'

    writer = csv.writer(response)
    writer.writerow(csv_header)
    writer.writerows(csv_rows)

    return response