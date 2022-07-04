from secrets import choice
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation
from django.db.models import Q
from .models import Usredetails

class LoginForm(forms.Form):
    email=forms.EmailField(max_length=30, required=True,label=_('Email'),widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))
    password = forms.CharField(max_length=30, required=True,label=_('Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    def clean(self):
        email    = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        # user_qs = User.objects.filter(email=email,is_superuser=True)
        user_qs = User.objects.filter(is_superuser=True ,email=email)
        print('user_qs',user_qs)
        if user_qs.exists():
            user_obj = user_qs.first()
            if not user_obj.check_password(password):
                print('invalid pass')
                raise forms.ValidationError('Invalid password')
        else:
            print('not exit')
            raise forms.ValidationError('User with this email does not exist')
        return self.cleaned_data  

class MypasswordResetform(PasswordResetForm):
    email=forms.EmailField(max_length=30, required=True,label=_('Email'),widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))

class MySetPasswordform(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
    )

class Profileform(forms.ModelForm):
    username=forms.CharField(max_length=30, required=True,label='Username',widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.CharField(max_length=30, required=True,label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1=forms.CharField(max_length=30, required=True,label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(max_length=30, required=True,label='Conform Password(again))',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(max_length=30, required=True,label='First Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(max_length=30, required=True,label='Last Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    mobile_number=forms.CharField(required=True,label='Mobile Number',widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(max_length=30, required=True,label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    gender=forms.ChoiceField(choices=(("male","male"),("female","female"),("other","other")),required=True,label='Gender')
    hobbies=forms.ChoiceField(choices=(("dance","Dance"),("Travling","Travling"),("Reading","Reading")),required=True,label='hobbies')
    profile=forms.ImageField(required=True,label='Profile Image')

    class Meta:
        model=Usredetails
        fields=('username','password1','password2','first_name','last_name','email','address','gender','hobbies','profile','mobile_number')

    def clean(self):
        email    = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        use=User.objects.filter(username=self.cleaned_data.get('username'))
        us=User.objects.filter(email=email)
        if us.exists():
            raise forms.ValidationError('email already')
        if use.exists():
            raise forms.ValidationError('username already')
        if not len(password1) >= 8 or not len(password2) >=8:
            print('8')
            raise forms.ValidationError('Password must be atleast 8 characters long') 
        if password1 != password2:
            print('same')
            raise forms.ValidationError('Both new password and confirm password must be same') 
        return self.cleaned_data 

class AdminProfileEditForm(forms.Form):
    first_name=forms.CharField(max_length=30, required=True,label='First Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(max_length=30, required=True,label='Last Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    mobile_number=forms.CharField(required=True,label='Mobile Number',widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(max_length=30, required=True,label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    gender=forms.ChoiceField(choices=(("male","male"),("female","female"),("other","other")),required=True,label='Gender')
    hobbies=forms.ChoiceField(choices=(("Dance","Dance"),("Travling","Travling"),("Reading","Reading")),required=True,label='hobbies')
    profile=forms.ImageField(required=True,label='Profile Image')
    address=forms.CharField(max_length=30, required=True,label='address',widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model=Usredetails
        fields=('first_name','last_name','email','address','gender','hobbies','profile','mobile_number')
    
    def clean(self):
        first_name   = self.cleaned_data.get('first_name')
        last_name    = self.cleaned_data.get('last_name')
        mobile_number= self.cleaned_data.get('mobile_number') 
        email        = self.cleaned_data.get('email') 
        gender       = self.cleaned_data.get('gender') 
        address      =self.cleaned_data.get('address')
        hobbies        =self.cleaned_data.get('hobbies')
        if not address or address=='':
            raise forms.ValidationError('please provide address')    #nofilederror
        if not first_name or first_name == '':
            raise forms.ValidationError('please provide first name')

        if not last_name or last_name == '':
            raise forms.ValidationError('please provide last name')

        if not email or email == '':
            raise forms.ValidationError('please provide address')

        if not mobile_number or mobile_number == "":
            raise forms.ValidationError('please provide mobile_number')  
        if not gender or gender == "":
            raise forms.ValidationError('please provide mobile_number') 
        # if not hobbies or hobbies == "":
        #     raise forms.ValidationError('please provide mobile_number') 

        if not mobile_number.isdigit():
            raise forms.ValidationError('please provide valid mobile_number')

         

          

       

     
           
           
        


    

