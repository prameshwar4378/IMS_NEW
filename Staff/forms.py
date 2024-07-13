
from django.contrib.auth.forms import UserCreationForm
from Developer.models import CustomUser,DB_Session,DB_Fees,DB_Result,DB_Subjects,DB_Schedule_Exam,DB_Attendance,DB_Web_Notification
from django import forms
from django.contrib.auth.forms  import AuthenticationForm
from django.utils import timezone
from django.core.exceptions import ValidationError


FINANCIAL_YEAR = (
    ("2022-23", "2022-23"), 
    ("2023-24", "2023-24"), 
    ("2024-25", "2024-25"), 
    ("2025-26", "2025-26"), 
    ("2026-27", "2026-27"), 
    ("2028-28", "2028-28"), 
    
)   
STUDENT_STATUS=(("Active","Active"),("Inactive","Inactive"))

class CustomStudentCreationForm(UserCreationForm):
    student_admission_date = forms.DateField(initial=timezone.now().date(), widget=forms.DateInput(attrs={'type': 'date'}))
    # academic_session=forms.ChoiceField(choices=FINANCIAL_YEAR, widget=forms.Select(attrs={'onchange': 'Call_Get_PRN_Function()', 'class': 'form-control'}))
    is_student = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), initial=True)
    status = forms.ChoiceField(choices=STUDENT_STATUS, initial='Active')
    class Meta:
        model = CustomUser
        fields = ('is_student','username','academic_session','student_profile','student_name','student_gender','student_dob','student_village','student_taluka','student_dist','parent_name','parent_mobile','parent_village','parent_taluka','parent_dist','student_collage','student_collage_address','batch','group','student_prn_no','student_admission_date','student_class','student_mobile','status','password1','password2')
        labels = {
            'student_name': 'Full Name',
            'student_profile': 'Upload Profile Image',
            'student_gender': 'Gender',
            'student_dob': 'Date of Birth',
            'student_mobile': 'Mobile Number',
            'student_village': 'Village',
            'student_taluka': 'Taluka',
            'student_dist': 'Dist',
        }   
        widgets = { 
            # 'academic_session': forms.ChoiceField(choices=FINANCIAL_YEAR,attrs={'onChange': 'Call_Get_PRN_Function()'}),
            'student_dob': forms.TextInput(attrs={'type': 'date'}),
            'student_name': forms.TextInput(attrs={'autofocus': True, }),
            'student_prn_no': forms.TextInput(attrs={'readonly': True }),
            'is_student':forms.HiddenInput(),
        }
    
    def clean_student_profile(self):
        student_profile = self.cleaned_data.get('student_profile', False)
        if student_profile:
            # Check if the file size is greater than 1MB (1048576 bytes)
            if student_profile.size > 1048576:
                raise ValidationError("The uploaded image size should not exceed 1MB.")
            return student_profile
        else:
            raise ValidationError("Couldn't read uploaded image.")
 
        
    # validatoions start     
    def clean_student_mobile(self):
        mobile = self.cleaned_data.get('student_mobile')
        if mobile:
            if not mobile.isdigit() or len(mobile) != 10:
                raise ValidationError('Enter a valid 10 digit mobile number.')
        return mobile
         
    def clean_parent_mobile(self):
        mobile = self.cleaned_data.get('parent_mobile')
        if mobile:
            if not mobile.isdigit() or len(mobile) != 10:
                raise ValidationError('Enter a valid 10 digit mobile number.')
        return mobile


    # validatoions stop     
   
 
class CustomStudentUpdateForm(UserCreationForm):
    student_admission_date = forms.DateField(initial=timezone.now().date(), widget=forms.DateInput(attrs={'type': 'date'}))
    # academic_session=forms.ChoiceField(choices=FINANCIAL_YEAR, widget=forms.Select(attrs={'onchange': 'Call_Get_PRN_Function()', 'class': 'form-control'}))
    is_student = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), initial=True)
    status = forms.ChoiceField(choices=STUDENT_STATUS, initial='Active')
    class Meta:
        model = CustomUser
        fields = ('is_student','academic_session','student_profile','student_name','student_gender','student_dob','student_village','student_taluka','student_dist','parent_name','parent_mobile','parent_village','parent_taluka','parent_dist','student_collage','student_collage_address','batch','group','student_prn_no','student_admission_date','student_class','student_mobile','status','password1','password2')
        labels = {
            'student_name': 'Full Name',
            'student_profile': 'Upload Profile Image',
            'student_gender': 'Gender',
            'student_dob': 'Date of Birth',
            'student_mobile': 'Mobile Number',
            'student_village': 'Village',
            'student_taluka': 'Taluka',
            'student_dist': 'Dist',
        }   
        widgets = { 
            # 'academic_session': forms.ChoiceField(choices=FINANCIAL_YEAR,attrs={'onChange': 'Call_Get_PRN_Function()'}),
            'student_dob': forms.TextInput(attrs={'type': 'date'}),
            'student_name': forms.TextInput(attrs={'autofocus': True, }),
            'student_prn_no': forms.TextInput(attrs={'readonly': True }),
            'is_student':forms.HiddenInput(),
        }
        
    # validatoions start     
    def clean_student_mobile(self):
        mobile = self.cleaned_data.get('student_mobile')
        if mobile:
            if not mobile.isdigit() or len(mobile) != 10:
                raise ValidationError('Enter a valid 10 digit mobile number.')
        return mobile
         
    def clean_parent_mobile(self):
        mobile = self.cleaned_data.get('parent_mobile')
        if mobile:
            if not mobile.isdigit() or len(mobile) != 10:
                raise ValidationError('Enter a valid 10 digit mobile number.')
        return mobile

    
    def clean_student_profile(self):
        student_profile = self.cleaned_data.get('student_profile', False)
        if student_profile:
            # Check if the file size is greater than 1MB (1048576 bytes)
            if student_profile.size > 1048576:
                raise ValidationError("The uploaded image size should not exceed 1MB.")
            return student_profile
        else:
            raise ValidationError("Couldn't read uploaded image.")
 
    # validatoions stop     
   
 




class FormStudentReceivedFees(forms.ModelForm):
    class Meta:
        model = DB_Fees
        fields = ('student_username','operator_username','operator_name','student_prn_no','student_name','student_class','received_remark','received_amount','amount_word','payment_mode','due_date','due_amount','due_remark')
        widgets={
            'student_prn_no':forms.HiddenInput(),
            'student_name':forms.HiddenInput(),
            'student_username':forms.HiddenInput(),
            'amount_word':forms.HiddenInput(),
            'operator_username':forms.HiddenInput(),
            'operator_name':forms.HiddenInput(),
            'received_date': forms.TextInput(attrs={'type': 'date'}),
            'due_date': forms.TextInput(attrs={'type': 'date'}),
            'received_amount': forms.NumberInput(attrs={'onChange': 'numberToWord()'}),
        }
            
 

class FormAddFees(forms.ModelForm):
    class Meta:
        model = DB_Fees
        fields = ('add_fees','fees_remark','student_prn_no','student_username')
        widgets={
            'student_prn_no':forms.HiddenInput(), 
            'student_username':forms.HiddenInput(), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_prn_no'].widget.attrs.update({'id': 'id_student_prn_no_add_fees'})
        self.fields['student_username'].widget.attrs.update({'id': 'id_student_username_add_fees'})

 
# Education Session for Staff 
class Form_academic_session(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('academic_session',)

 
# Education Session for Staff 
class Form_Subject(forms.ModelForm):
    class Meta:
        model=DB_Subjects
        fields=('class_name','subject_name')


 
# Schedult Exam For Student
class Form_Schedule_Exam(forms.ModelForm):
    class Meta:
        model=DB_Schedule_Exam
        exclude=('institute_code',)
        widgets={
            'exam_start_date': forms.TextInput(attrs={'type': 'date'}),
            'exam_end_date': forms.TextInput(attrs={'type': 'date'}),
            'academic_session': forms.TextInput(attrs={'type': 'hidden'}),
        }
        def save(self, commit=True):
            instance = super().save(commit=False)
            # Get the session value using the request object from the form
            session_value = self.request.session.get('my_key')
            # Set the model field value to the session value
            instance.my_field = session_value
            if commit:
                instance.save()
            return instance


from datetime import date

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = DB_Attendance
        fields = ('id','student_prn_no', 'student_name', 'is_present')
        widgets={
            'student_prn_no': forms.TextInput(attrs={'class':'form-control'}),
            'student_name': forms.TextInput(attrs={'class':'form-control'}),
            'is_present': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

 
class UpdateAttendanceForm(forms.ModelForm):
    id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = DB_Attendance
        fields = ('id','student_prn_no', 'student_name', 'is_present')
        widgets={
            'id':forms.HiddenInput(), 
            'student_prn_no': forms.TextInput(attrs={'class':'form-control'}),
            'student_name': forms.TextInput(attrs={'class':'form-control'}),
            'is_present': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }
 
class Create_Web_Notification_Form(forms.ModelForm):
    class Meta:
        model = DB_Web_Notification
        exclude = ('institute_code',)
        widgets={ 
            'notification_valid_up_to': forms.TextInput(attrs={'type':'date'}),
            'notification_message': forms.Textarea(attrs={'rows': 4}),
        } 