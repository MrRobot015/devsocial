from django.core import paginator
from django.db.models import Q
from .models import Project , Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#=======================================================================================#
#====this file the contains all helpers functions and utility's for projects app========#
#=======================================================================================#

def paginateProjects(request, projests, results):
    """divide data(projects) and display it on multiple pages within one page"""

    page = request.GET.get('page')
    paginator = Paginator(projests,results)

    try:
        projests = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projests = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projests = paginator.page(page)
    
    letfIndex = (int(page)-1)

    if letfIndex < 1:
        letfIndex = 1

    rightIndex = (int(page)+2)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(letfIndex,rightIndex)
    
    return projests, custom_range

#-----------------------------------------------#

def searchProjects(request):
    """return the projects that contain the search_query value & the search_query"""
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")
    
    tags = Tag.objects.filter(name__icontains=search_query)

    projests = Project.objects.distinct().filter(
        Q(title__icontains=search_query)|
        Q(description__icontains=search_query)|
        Q(owner__name__icontains=search_query)|
        Q(tags__in=tags),
    )
    return projests ,search_query