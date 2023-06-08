from django.urls import path
from .views import *

#app_name = 'cloud_app'

urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('register_car/', register_car, name='register_car'),
    path('index/', index, name='index'),
    path('logout/', logout_view, name='logout'),
    path('view_all_cars/', view_all_cars, name='view_all_cars'),
    path('forgot/', forgot, name='forgot'),
]
    # Add more paths for other views as needed

