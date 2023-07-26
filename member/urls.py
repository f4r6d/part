from django.urls import path
from . import views

app_name = 'member'
urlpatterns = [
    path('', views.index, name='index'),
    path('admins', views.admins, name='admins'),

    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),

    path('members/', views.members, name='members.index'),
    path('members/create/', views.MemberCreateView.as_view(), name='members.create'),
    path('members/<int:member_id>/', views.show, name='members.show'),
    path('members/<int:member_id>/delete/', views.delete, name='members.delete'),
    path('members/<int:pk>/edit/', views.MemberUpdateView.as_view(), name='members.edit'),
]