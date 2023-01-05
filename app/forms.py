from django import forms
import re
from .models import LoginModel,Client,project
from django.contrib.auth.forms import UserCreationForm
import datetime
DEPARTMENT_CHOICE = [
    ("Development Department","Development Department"),
    ("Managers Department","Managers Department"),
    ("Application Department","Application Department"),
    ("Accounts Department","Accounts Department")
]
PRIORITY_CHOICE = [
    ("High","High"),
    ("Medium","Medium"),
    ("Low","Low")
]
STATUS_CHOICE = [
    ("Completed","Completed"),
    ("Pending","Pending"),
    ("On Progress","On Progress")
]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['names','CompanyName','Phone','email']


class ProjectForm(forms.ModelForm):
    client = forms.CharField(widget=forms.Select())
    class Meta:
        model = project
        fields = ['ProjectId','Title','Department','Status','Priority','From','to','client']

    def clean_From(self):
        see = self.cleaned_data['From'].date().year
        year_today = datetime.date.today().year
        if see < year_today:
            raise forms.ValidationError(f"Year must be between {year_today} to {year_today + 5}")
        return self.cleaned_data['From']
    def clean_to(self):
        see = self.cleaned_data['to'].date().year
        year_today = datetime.date.today().year
        if see < year_today:
            raise forms.ValidationError(f"Year must be between {year_today} to {year_today + 5}")
        return self.cleaned_data['to']




class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255,label="Email Id", widget = forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=8,max_length=16,label="Password", widget = forms.PasswordInput(attrs={'class': 'form-control'}))

class RegForm(UserCreationForm):
    username = forms.CharField(min_length=4,max_length=255,label="Username", widget = forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=255,label="Email Id", widget = forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(min_length=8,max_length=16,label="Password", widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(min_length=8,max_length=16,label="Re Enter Password", widget = forms.PasswordInput(attrs={'class': 'form-control'}), help_text = "Enter the same password as above, for verification.")

    class Meta:
        model = LoginModel
        fields = ['username','email','password1','password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""


    def clean(self):
        super(RegForm, self).clean()
        # print ("here is " + str(self.cleaned_data))
        try:
            password = self.cleaned_data['password1']
        except:
            password = ""
        try:
            pass2 = self.cleaned_data['password2']
        except:
            pass2 = ""


        pattern = re.compile('[A-Z]')
        pattern2 = re.compile('[a-z]')
        pattern3 = re.compile('[0-9]')
        pattern4 = re.compile('[!@#$%^&*(),.?":{}|<>]')

        if not pattern.search(password) or not pattern2.search(password) or not pattern3.search(password) or not pattern4.search(password):
                list = ['should contain at least one upper case','should contain at least one lower case','should contain at least one digit','should contain at least one Special character']
                self.add_error('password1',list)
                try:
                    del self._errors['password2']
                except:
                    pass

        else:
            if password != pass2:
                error_message = 'Password did not matched. Enter the same password as above'
                field = 'password2'
                # if self._errors['password2']:
                #     del self._errors['password2']
                try:
                    del self._errors['password2']
                except:
                    pass
                self.add_error(field,error_message)
        return self.cleaned_data




    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = LoginModel.objects.get(email=email)
        except:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")
        

    def clean_username(self):
        username = self.cleaned_data['username']
        print("username "+ str(username))
        try:
            user_name = LoginModel.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")