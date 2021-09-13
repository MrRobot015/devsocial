from django.urls import path
from . import views

urlpatterns=[
    #projects displaying urls
    path('' , views.projects ,name="projects"),
    path('project/<str:pk>/' , views.project , name="project"),

    #projects creation and management urls
    #the user most be authentcated to access these urls
    path('create-project/' , views.createProject , name="create-project"),
    path('update-project/<str:pk>/' , views.updateProject , name="update-project"),
    path('delete-project/<str:pk>/' , views.deleteProject , name="delete-project"),
]