from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


#=======================================================================================#
#=====this file the contains all helpers functions and utility's for users app==========#
#=======================================================================================#

def paginateProfiles(request, profiles, results):
    """divide data(profiles) and display it on multiple pages within one page"""

    page = request.GET.get('page')
    paginator = Paginator(profiles,results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    
    letfIndex = (int(page)-1)

    if letfIndex < 1:
        letfIndex = 1

    rightIndex = (int(page)+2)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(letfIndex,rightIndex)
    
    return profiles, custom_range

#-----------------------------------------------#


def searchProfiles(request):
    """return the profiles that contain the search_query value & the search_query"""
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(title__icontains=search_query) |
        Q(skill__in=skills)
    )


    return profiles , search_query