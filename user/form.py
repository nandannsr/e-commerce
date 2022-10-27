from django import forms
from  accounts.models import Account
from accounts.models import UserProfile

class RegisterForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        
        'placeholder': 'Enter Password'
    }))
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        
        'placeholder': 'Repeat Password'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
        
        
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        phone_number = cleaned_data.get('phone_number')
        if len(phone_number) == 10 and phone_number.isdigit():
          user = Account.objects.filter(phone_number=phone_number).exists()
          if user:
            raise forms.ValidationError(
                "Phone number exists.!"
            )
          else:
             password = cleaned_data.get('password')
             confirm_password = cleaned_data.get('confirm_password')
        
        
             if password != confirm_password:
                  raise forms.ValidationError(
                    "Password does not match!."
                  )
        else:
            raise forms.ValidationError(
                "Invalid Phone number.!"
            )          
        
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter the First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter the Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your Email'
            
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number', 'email')
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
        
        
class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':{"image files only"}}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')  
          
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'