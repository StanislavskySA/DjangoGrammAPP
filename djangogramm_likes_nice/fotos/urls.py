from django.urls import path
from .views import MainPage, EditProfile, Feedback, LoginUser

from .views import LogoutUser, RegisterUser, MySubscriptions
from .views import MyPhotos, MyFollower, validate_username

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('my_subscriptions/', MySubscriptions.as_view(), name='my_subscriptions'),
    path('my_photos/', MyPhotos.as_view(), name='my_photos'),
    path('my_followers/', MyFollower.as_view(), name='my_followers'),
    path('user_profile/', EditProfile.as_view(), name='user_profile'),
    path('feedback/', Feedback.as_view(), name='feedback'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('validate_username', validate_username, name='validate_username')
]
