from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),    # This line has changed!
    url(r'^register$', views.register),
    url(r'^login$', views.login), 
    url(r'^travel$', views.travel),
    url(r'^addtravelplan$', views.addtravelplan), 
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^plans/(?P<id>\d+)$', views.plans),
    url(r'^travel_plan/add$', views.create), 
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^remove/(?P<id>\d+)$', views.remove), 
]