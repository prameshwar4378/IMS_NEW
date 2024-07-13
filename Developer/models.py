from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
import io 

 
GENDER = (
    ("Male", "Male"), 
    ("Female", "Female"), 
    
)  

FINANCIAL_YEAR = (
    ("2022-23", "2022-23"), 
    ("2023-24", "2023-24"), 
    ("2024-25", "2024-25"), 
    ("2025-26", "2025-26"), 
    ("2026-27", "2026-27"), 
    ("2028-28", "2028-28"), 
    
)   


CLASS = (
    ("1st Standerd", "1st Standerd"), 
    ("2nd Standerd", "2nd Standerd"), 
    ("3rd Standerd", "3rd Standerd"), 
    ("4th Standerd", "4th Standerd"), 
    ("5th Standerd", "5th Standerd"), 
    ("6th Standerd", "6th Standerd"), 
    ("7th Standerd", "7th Standerd"), 
    ("8th Standerd", "8th Standerd"), 
    ("9th Standerd", "9th Standerd"), 
    ("10th Standerd", "10th Standerd"), 
    ("11th Standerd", "11th Standerd"), 
    ("12th Standerd", "12th Standerd"), 
)   

STUDENT_STATUS=(("Active","Active"),("Inactive","Inactive"))

 

class CustomUser(AbstractUser):
    # Genaral fields 
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,null=True,unique=True)
    academic_session=models.CharField(max_length=255,null=True,blank=True, choices=FINANCIAL_YEAR,default="2022-23")

    # fields for Institute 
    is_institute=models.BooleanField(default=False)
    institute_logo=models.ImageField( upload_to="institute_logo/", null=True,blank=True)
    institute_name = models.CharField(max_length=255,null=True)
    institute_address = models.CharField(max_length=500,null=True)
    institute_code = models.CharField(max_length=500,null=True)
    institute_is_completed=models.BooleanField(default=False)

    # fields for Staff 
    is_staff=models.BooleanField(default=False)
    staff_name=models.CharField(max_length=255,null=True)
    staff_id_no=models.CharField(max_length=50,null=True)
    staff_profile=models.ImageField( upload_to="staff_profile/", null=True,blank=True)

    # fields for Student 
    is_student=models.BooleanField(default=False)
    student_profile=models.ImageField(upload_to="student_profile/", null=True,blank=True)
    student_prn_no=models.CharField(max_length=50,null=True,unique=True)
    student_admission_date=models.DateField(auto_now=False, auto_now_add=False,null=True)
    student_name=models.CharField(max_length=255,null=True)
    student_gender=models.CharField(max_length=255,null=True,choices=GENDER)
    student_dob=models.DateField(auto_now=False, auto_now_add=False,null=True)
    student_mobile=models.CharField(max_length=255,null=True)
    student_village=models.CharField(max_length=255,null=True)
    student_taluka=models.CharField(max_length=255,null=True)
    student_dist=models.CharField(max_length=255,null=True)

    parent_name=models.CharField(max_length=255,null=True,blank=True)
    parent_mobile=models.CharField(max_length=255,null=True,blank=True)
    parent_village=models.CharField(max_length=255,null=True,blank=True)
    parent_taluka=models.CharField(max_length=255,null=True,blank=True)
    parent_dist=models.CharField(max_length=255,null=True,blank=True) 

    student_collage=models.CharField(max_length=255,null=True,blank=True)
    student_collage_address=models.CharField(max_length=255,null=True,blank=True)
    
    student_class=models.CharField(max_length=255,null=True,choices=CLASS)
    batch=models.CharField(max_length=255,null=True,blank=True)
    group=models.CharField(max_length=255,null=True,blank=True)
    status=models.CharField(max_length=255,null=True,choices=STUDENT_STATUS)
    date_time=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    tour_is_completed=models.BooleanField(default=False)
    is_institute_profile_completed=models.BooleanField(default=False)


 
 
PAYMENT_MODE = (
    ("Cash", "Cash"), 
    ("Phone Pay", "Phone Pay"), 
    ("Google Pay", "Google Pay"), 
    ("Amazone Pay", "Amazone Pay"), 
    ("Other Online", "Other Online"), 
)   

class DB_Fees(models.Model):
    add_fees=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    fees_remark=models.CharField(max_length=250,null=True)
    academic_session=models.CharField(max_length=100, null=True)
    institute_code = models.CharField(max_length=500,null=True)

    student_username=models.CharField(max_length=250,null=True)
    operator_username=models.CharField(max_length=250,null=True) #this field used for checking Operator Name
    operator_name=models.CharField(max_length=250,null=True) #this field used for checking Operator Name
    student_prn_no=models.CharField(max_length=50,null=True)
    student_name=models.CharField(max_length=250,null=True)
    student_class=models.CharField(max_length=50,choices=CLASS,null=True)
    received_date=models.DateField(auto_now=False, auto_now_add=True)
    received_remark=models.CharField(max_length=250 ,null=True)
    received_amount=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    amount_word=models.CharField(max_length=250,null=True,blank=True)
    payment_mode=models.CharField(max_length=50,choices=PAYMENT_MODE)
    due_date=models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    due_amount=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    due_remark=models.CharField(max_length=250,null=True,blank=True)
    date_time=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)


class DB_Session(models.Model):
    financial_year=models.CharField(max_length=50, null=True, choices=FINANCIAL_YEAR)

class DB_Subjects(models.Model):
    class_name=models.CharField(max_length=50, null=True, choices=CLASS) 
    subject_name=models.CharField(max_length=100, null=True)
    institute_code = models.CharField(max_length=500,null=True)


class DB_Result(models.Model):
    academic_session=models.CharField(max_length=100, null=True)
    institute_code = models.CharField(max_length=500,null=True)
    student_prn_no=models.CharField(max_length=100, null=True)
    subject_name=models.CharField(max_length=100, null=True)
    student_class=models.CharField(max_length=100, null=True)
    min_marks=models.CharField(max_length=100, null=True)
    obtained_marks=models.CharField(max_length=100, null=True)
    out_off_marks=models.CharField(max_length=100, null=True)
    percentage=models.CharField(max_length=100, null=True)
    result=models.CharField(max_length=100, null=True)
    exam_title=models.CharField(max_length=100, null=True)
    exam_start_date=models.CharField(max_length=100, null=True)
    exam_end_date=models.CharField(max_length=100, null=True)

class DB_Schedule_Exam(models.Model):
    academic_session=models.CharField(max_length=100, null=True)
    institute_code = models.CharField(max_length=500,null=True)
    class_name=models.CharField(max_length=100, null=True,choices=CLASS)
    exam_title=models.CharField(max_length=100, null=True) 
    exam_start_date=models.DateField(auto_now=False, auto_now_add=False,null=True)
    exam_end_date=models.DateField(auto_now=False, auto_now_add=False,null=True)

class DB_Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    academic_session=models.CharField(max_length=100, null=True)
    institute_code = models.CharField(max_length=500,null=True)
    student_name=models.CharField(max_length=50,null=True)
    student_prn_no=models.CharField(max_length=50,null=True)
    student_class=models.CharField(max_length=50,null=True)
    attendance_date = models.DateField(null=True)
    is_present = models.BooleanField(default=False)
    date_time=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)

class DB_Web_Notification(models.Model):
    academic_session=models.CharField(max_length=100, null=True,blank=True)
    institute_code = models.CharField(max_length=500,null=True)
    student_class=models.CharField(max_length=100, null=True,blank=True,choices=CLASS)
    student_prn_no=models.CharField(max_length=50,null=True,blank=True)
    notification_subject=models.CharField(max_length=250,null=True)
    notification_message=models.TextField(null=True)
    upload_file1=models.FileField(upload_to="Notes", max_length=100,null=True,blank=True)
    upload_file2=models.FileField(upload_to="Notes", max_length=100,null=True,blank=True)
    upload_file3=models.FileField(upload_to="Notes", max_length=100,null=True,blank=True)
    notification_valid_up_to=models.DateField(auto_now=False, auto_now_add=False,null=True,blank=True)
    date_time=models.DateField(auto_now=False, auto_now_add=True,null=True)


