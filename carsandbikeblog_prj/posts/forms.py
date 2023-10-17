from django import forms
from .models import postsm,Reviews
from django.contrib.auth.models import User
#importing from the django library,the package forms
#creating a form class inheriting the class Forms from package forms
class MyLoginForm(forms.Form):
    #create two fields in the form for username and password
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
        #the only check we have to do is compare passwords
        #creating a CharField object by passing values into the constructor
        password = forms.CharField(label="Password",widget=forms.PasswordInput)
        password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)

        class Meta:
            #in meta , we specify which model the form is for and the fields
            model = User
            fields = ('username','first_name','email','password')
        #naming convection is clean_<fieldname>
        def clean_password2(self):
            #clean the data in the context
            cd=self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords not matching')
            return cd['password2']

class PostAddForm(forms.ModelForm):
    class Meta:
        model = postsm #the post model from model.py and its fields for user to input
        fields = ('post_title', 'post_description', 'post_shortname', 'post_image')

class PostEditForm(forms.ModelForm):
    class Meta:
        model = postsm #the post model from model.py and its fields for user to input
        fields = ('post_title', 'post_description', 'post_shortname', 'post_image')
class ReviewsAddForm(forms.ModelForm):
    class Meta:
        model = Reviews #the post model from model.py and its fields for user to input
        fields = ( 'rating','title', 'description', 'video_url')

class ReviewerRegistrationForm(forms.ModelForm):
    # the only check we have to do is compare passwords
    # creating a CharField object by passing values into the constructor
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        # in meta , we specify which model the form is for and the fields
        model = User
        fields = ('username', 'first_name', 'email', 'password')

    # naming convection is clean_<fieldname>
    def clean_password2(self):
        # clean the data in the context
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords not matching')
        return cd['password2']