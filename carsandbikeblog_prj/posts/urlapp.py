
from django.urls import path
from .views import posts_list,post_details,user_login_view,register,add_post,edit_post,delete_post,add_review,register_reviewer
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordChangeDoneView
urlpatterns = [
    path('', posts_list,name='home_path'),
    path('post_details/<int:post_id>/', post_details,name='post_details'),
    #path('login/', user_login_view, name='login_path'),
    #instead of our custom view we used built in LoginView
    #Since LoginView is a class,convert it into a view and use as_view
    path('accounts/login/',LoginView.as_view() , name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change/done', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('accounts/register/', register
         , name='register'),
    path('accounts/register_reviewer/', register_reviewer
         , name='register_reviewer'),
    path('accounts/add_post/', add_post
         , name='add_post'),
    path('accounts/edit_post/<int:passed_id>/',edit_post
         , name='edit_post'),
    path('accounts/delete_post/<int:passed_id>/', delete_post
         , name='delete_post'),
    path('accounts/add_review/<int:passed_id>/', add_review
         , name='add_review'),
]