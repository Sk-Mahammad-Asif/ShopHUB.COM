from django import forms
from django.contrib.auth.forms import  UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from .models import Customer
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

#from django.contrib.auth import authenticate

class CustomerRegistrationForm(UserCreationForm):
    password1=forms.CharField(label='Password *',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password(again) *',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        labels={'email':'Email'}
        widgets={'username':forms.TextInput(attrs={'class':'form-control'})}

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists try new")
        return email




class LoginForm(AuthenticationForm):
	

    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password=forms.CharField(label=_("Password"), strip=False ,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

    #class Meta:
        #model=User
        #fields=['username','password']
        #labels={'username':'Username'}
        #widgets={'username':forms.TextInput(attrs={'class':'form-control'})}



class MyPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(label=_("Old Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))    
    new_password1=forms.CharField(label=_('New Password'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(label=_('Confirm Password'),widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(label=_("Email*:  (Which You have already register)"),max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label=_('New Password'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(label=_('Confirm Password'),widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):

    class Meta:
        model=Customer
        fields=['name','locality','city','state','zipcode','profile_pic']
        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),'locality':forms.TextInput(attrs={'class':'form-control'})
        ,'city':forms.TextInput(attrs={'class':'form-control'}),'state':forms.Select(attrs={'class':'form-control'}),
        'zipcode':forms.NumberInput(attrs={'class':'form-control'})}    


class SearchForm(forms.Form):
    title=forms.CharField(label='Title',max_length=100)







    #def clean_username(self):
        #username = self.data['username']
        #if '@' in username:
            #try:
                #username = User.objects.get(email=username).username
            #except ObjectDoesNotExist:
                #raise ValidationError(
                    #self.error_messages['invalid_login/email'],
                    #code='invalid_login/email',
                    #params={'username':self.username_field.verbose_name,'autofocus':True},
                #)
        #return username        