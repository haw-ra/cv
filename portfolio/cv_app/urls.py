from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('cv/', views.home, name='home'),
    path('builder/', views.cv_builder, name='cv_builder'),
    path('builder/education/<int:profile_id>/', views.add_education, name='add_education'),
    path('builder/experience/<int:profile_id>/', views.add_experience, name='add_experience'),
    path('builder/skill/<int:profile_id>/', views.add_skill, name='add_skill'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/profile/<int:profile_id>/', views.edit_profile, name='edit_profile'),
    
    # الروابط الجديدة الخاصة بالحذف
    path('delete/education/<int:edu_id>/', views.delete_education, name='delete_education'),
    path('delete/experience/<int:exp_id>/', views.delete_experience, name='delete_experience'),
    path('delete/skill/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    path('choose-template/', views.choose_template, name='choose_template'),
    path('register/', views.register, name='register'),  # صفحة إنشاء حساب جديد
]