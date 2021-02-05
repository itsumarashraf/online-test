from django.urls import path,include
from . import views
from users import urls


urlpatterns = [
    path("track/", views.track, name='track'),
    path("updatetrack/",views.updatetrack,name='updatetrack'),    
]