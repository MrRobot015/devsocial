from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import CustomUserCreationForm,ProfileForm,SkillForm,MessageForm

from .utils import searchProfiles, paginateProfiles


# =========================================================
def loginUser(request):
    """login process and authenticate and validation"""
    
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        user_name = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=user_name)
            user = authenticate(request, username=user_name, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "successfully logged in")
                return redirect(request.GET['next'] if 'next' in request.GET else 'account')

            else:
                messages.error(request, "username or password is incorrect")
        except:
            messages.error(request, "username doesn't exist")

        

    return render(request, "users/login_register.html")


# =========================================================
def logoutUser(request):
    """logout users"""
    logout(request)
    messages.info(request, " user was sucessfully logout ")
    return redirect("login")


# =========================================================
def registerUser(request):
    """user registeration and form validation"""
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "user has been created successfully")
            login(request, user)
            return redirect("edit-account")
        else:
            messages.error(request, "an erorr ass occurred during registeration..!!")

    context = {
        "page": page, 
        "form": form
        }
    return render(request, "users/login_register.html", context)


# =========================================================
def porfiles(request):
    """display profiles and search in profiles"""
    profiles , search_query = searchProfiles(request)
    profiles , custom_range = paginateProfiles(request, profiles, 3)
    context = {
        'profiles': profiles,
        'search_query':search_query,
        'custom_range':custom_range,
        
        }
    return render(request, "users/profiles.html", context)


# =========================================================
def userProfile(request, pk):
    """display a profile """
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {
        "profile": profile,
        "topSkills": topSkills, 
        "otherSkills": otherSkills
        }
    return render(request, "users/user-profile.html", context)


# =========================================================
@login_required(login_url="login")
def account(request):
    """display logged in user account"""
    user = request.user.profile
    skills = user.skill_set.all()
    projects = user.project_set.all()

    context = {
        'user':user,
        'skills':skills,
        'projects':projects,
        }
    return render(request, "users/account.html", context)
# =========================================================
@login_required(login_url='login')
def editAccount(request):
    """edit logged in user account"""
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST , request.FILES , instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "account has been updated successfully")
            return redirect('account')
            
        else:
            messages.error(request, " an error occurred")

    context = {'form':form}
    return render(request, "users/profile_form.html", context)

# =========================================================

@login_required(login_url='login')
def createSkill(request):
    """create skill & add it to the logged in user account"""
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "skill has been created successfully")
            return redirect('account')
        else:
            messages.error(request, "error occurred..!!")

    context = {'form':form}
    return render(request, "users/skill_form.html", context)

# =========================================================

@login_required(login_url='login')
def updateSkill(request , pk):
    """update skill in the logged in user account"""
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST , instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "skill has been updated successfully")
            return redirect('account')
        else:
            messages.error(request, "error occurred..!!")

    context = {'form':form}
    return render(request, "users/skill_form.html", context)

# =========================================================
@login_required(login_url='login')
def deleteSkill(request, pk):
    """delete skill in the logged in user account"""
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "skill has been deleted")
        return redirect('account')
        
    context = {'object':skill}
    return render(request, "delete_template.html" , context)

# =========================================================

@login_required(login_url="login")
def inbox(request):
    """display the logged in user messages inbox"""
    profile = request.user.profile
    messagesRequest = profile.messages.all()
    count = messagesRequest.filter(is_read=False).count()

    context = {
        'messagesRequest':messagesRequest,
        'count':count,
        }
    return render(request, "users/inbox.html", context)


# =========================================================

@login_required(login_url='login')
def message(request, pk):
    """display a single message from the logged in user inbox"""
    profile = request.user.profile
    the_message = profile.messages.get(id=pk)

    if the_message.is_read == False:
        the_message.is_read = True
        the_message.save()
    context = {'message':the_message}
    return render(request, "users/message.html", context)


# =========================================================


def createMessage(request, pk):
    """create the message and saved to the DB and linked to a profile as recipient"""
    form = MessageForm()
    recipient = Profile.objects.get(id=pk)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            the_message = form.save(commit=False)
            the_message.recipient = recipient
            if request.user.is_authenticated:
                sender = request.user.profile
                the_message.sender = sender
                the_message.name = sender.name
                the_message.email = sender.email

            the_message.save()
            messages.success(request, "Message send successfully")
            return redirect('user-profile', pk = recipient.id)
        else:
            messages.error(request, "an erorr occurred")
    context = {'form':form}

    return render(request, "users/message_form.html", context)

