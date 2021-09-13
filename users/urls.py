from django.urls import path
from . import views

urlpatterns = [
    #user registeration And login urls
    path('login/', views.loginUser , name='login'),
    path('logout/', views.logoutUser , name='logout'),
    path('register/', views.registerUser , name='register'),

    #logged in user account and account management urls
    #the user most be authentcated to access these urls
    path('account/', views.account , name='account'),
    path('edit-account/', views.editAccount , name='edit-account'),
    path('create-skill/', views.createSkill ,name='create-skill'),
    path('update-skill/<str:pk>/', views.updateSkill ,name='update-skill'),
    path('delete-skill/<str:pk>/', views.deleteSkill ,name='delete-skill'),

    #messages and messages creation urls
    path('inbox/', views.inbox , name='inbox'),#need a authentcate user to access
    path('message/<str:pk>/', views.message , name='message'),
    path('create_message/<str:pk>/', views.createMessage , name='create_message'),

    #profiles displaying urls
    path('' , views.porfiles, name='profiles'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
]