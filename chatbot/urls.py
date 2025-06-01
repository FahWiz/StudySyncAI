from django.urls import path,include
from .views import (
    assistant_page, chatbot_api, home_page, auth_page,
    register_user, login_user, logout_user, dashboard,
    save_study_plan,schedule_page,mark_as_complete,profile_view
) 

urlpatterns = [
    path('assistant/', assistant_page, name='assistant_page'),
    path('chatbot/', chatbot_api, name='chatbot_api'),
    path('', home_page, name='home'),
    path('auth/', auth_page, name='auth_page'),
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path('dashboard/', dashboard, name='dashboard'),
    path('scheduler/', schedule_page, name='scheduler'),
    path('save-study-plan/', save_study_plan, name='save_study_plan'),
    path('mark-as-complete/<int:detail_id>/', mark_as_complete, name='mark_as_complete'),
    path('profile/',profile_view,name='profile'),
]