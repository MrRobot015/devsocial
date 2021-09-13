from django.shortcuts import render , redirect
#from django.http import HttpResponse
from django.contrib import messages
from .models import Project
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, paginateProjects

#=========================================================
def projects(request):
    """display all projects"""
    projects , search_query = searchProjects(request)
    projects , custom_range = paginateProjects(request, projects, 6)

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range,
        
        }
    return render(request, "projects/projects.html", context)

#=========================================================
def project(request, pk):
    """display a single project"""
    
    projectObj = Project.objects.get(id=pk)
    
    #review and vote block
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.owner = request.user.profile
        review.project = projectObj
        review.save()

        projectObj.getVoteCount

        messages.success(request,"your review as been added successfully")
        return redirect('project', pk = projectObj.id)
        #end of review and vote block

    context = {
        "project": projectObj,
        "form":form,
        }
    return render(request, "projects/project.html", context)

#=========================================================
@login_required(login_url='login')
def createProject(request):
    """create Project and add it to the DB and linked to the logged user as owner"""
    profile = request.user.profile # this line to get the logged_in user profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST , request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile # this line to set the logged_in user to be the owner of the project
            project.save()
            messages.success(request, "project has been created successfully")
            return redirect('account')

        else:
            messages.error(request, " an error occurre")
            
    context = {'form': form}
    return render(request, "projects/form.html" , context)

#=========================================================
@login_required(login_url='login')
def updateProject(request, pk):
    """update one of the logged in user projects"""

    #the to line make sure that the logged_in user can edit his projects only
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    #the form for edit the project info
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST , request.FILES , instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "project has been updated successfully")
            return redirect('account')

        else:
            messages.error(request, " an error occurre")
    context = {'form': form}
    return render(request, "projects/form.html" , context)

#=========================================================
@login_required(login_url='login')
def deleteProject(request , pk):
    """delete one of the logged in user projects from the DB"""

    profile = request.user.profile
    project= profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        messages.success(request, "project has been delete successfully")
        return redirect('account')
    context={
        'object': project,
    }
    return render(request , "delete_template.html" , context)

#=========================================================