from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Skill,Message

#================================================================
    #registeration form part1
    # basic info
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name", "email" , "username", 
            "password1" , "password2",
            ]
        labels = {
            "first_name": "Name",
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, feild in self.fields.items():
            feild.widget.attrs.update({"class": "input"})
#================================================================
    #registeration form part2
    # add/editing profile model info
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name","location","email",
            "username", "title","bio",
            "profile_image","social_github",
            "social_linkedin", "social_twitter",
            "social_stackoverflow", "social_website",
        ]
        labels ={
            'title':'pro_title'
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, feild in self.fields.items():
            feild.widget.attrs.update({"class": "input"})

#================================================================
    #skill form

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude =['owner']
    
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, feild in self.fields.items():
            feild.widget.attrs.update({"class": "input"})

#================================================================
    #messages form

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
        
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, feild in self.fields.items():
            feild.widget.attrs.update({"class": "input"})
       