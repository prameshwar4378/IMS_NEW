import django_filters
from django import forms
from Developer.models import DB_Fees,CustomUser,DB_Attendance
from django_filters import DateFilter
from django.forms import DateInput


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

class Attendance_Filter(django_filters.FilterSet):
    start_date = DateFilter(field_name='attendance_date', lookup_expr='gte', widget=DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='attendance_date', lookup_expr='lte', widget=DateInput(attrs={'type': 'date'}))
    student_class = django_filters.ChoiceFilter(choices=CLASS)
    def __init__(self, *args, **kwargs):
        super(Attendance_Filter, self).__init__(*args, **kwargs)
        self.filters['attendance_date'].label = "Start Date - MM/DD/YYYY"
        self.filters['attendance_date'].label = "End Date - MM/DD/YYYY"

    class Meta:
        model = DB_Attendance
        fields = ['attendance_date','student_prn_no','student_class']
        widgets = {
            'attendance_date': DateInput(attrs={'type': 'date'})
        }




class Student_name_Filter(django_filters.FilterSet):
     class Meta:
        model = CustomUser
        fields = ['student_class']
        # widgets = {
        #     'due_date': DateInput(attrs={'type': 'date'})
        # }



class DueFees_Filter(django_filters.FilterSet):
    start_date = DateFilter(field_name='due_date', lookup_expr='gte', widget=DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='due_date', lookup_expr='lte', widget=DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(DueFees_Filter, self).__init__(*args, **kwargs)
        self.filters['due_date'].label = "Start Date - MM/DD/YYYY"
        self.filters['due_date'].label = "End Date - MM/DD/YYYY"

    class Meta:
        model = DB_Fees
        fields = ['due_date','student_prn_no','student_class']
        widgets = {
            'due_date': DateInput(attrs={'type': 'date'})
        }


