from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,DB_Fees
from django import forms
from django.contrib.auth.forms  import AuthenticationForm
from django.core.exceptions import ValidationError

class Custom_Institute_Creation_Form(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'})
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
    is_institute = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), initial=True)
    class Meta:
        model = CustomUser
        fields = ('username','email', 'institute_name','institute_address','institute_code','institute_logo','is_institute','password1','password2')


    def clean_institute_logo(self):
        institute_logo = self.cleaned_data.get('institute_logo', False)
        if institute_logo:
            # Check if the file size is greater than 1MB (1048576 bytes)
            if institute_logo.size > 1048576:
                raise ValidationError("The uploaded image size should not exceed 1MB.")
            return institute_logo
        else:
            raise ValidationError("Couldn't read uploaded image.")
 


class Custom_Institute_Update_Form(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'})
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    is_institute = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), initial=True)
    class Meta:
        model = CustomUser
        exclude = ('username',)
        fields = ('email', 'institute_name', 'institute_address', 'institute_code', 'institute_logo', 'is_institute', 'password1', 'password2')

    def clean_institute_logo(self):
        institute_logo = self.cleaned_data.get('institute_logo', False)
        if institute_logo:
            # Check if the file size is greater than 1MB (1048576 bytes)
            if institute_logo.size > 1048576:
                raise ValidationError("The uploaded image size should not exceed 1MB.")
            return institute_logo
        else:
            raise ValidationError("Couldn't read uploaded image.")
 

 


class login_form(AuthenticationForm):
    username=forms.CharField(label='username',widget=forms.TextInput(attrs={'class':'input100','placeholder':'Enter Username'}))
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'input100','placeholder':'Enter Password'}))
 