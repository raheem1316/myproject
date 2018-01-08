from django.conf.urls import url

from queriesapp import views

urlpatterns = [
        url(r'^sample/$',views.sample,name='sample'),
        url(r'^$',views.home,name='home'),
        url(r'^signup/$', views.signup, name='signup'),
        url(r'^login/$', views.signin, name='login'),
        url(r'^addpost/$', views.addpost, name='addpost'),
        url(r'^editprofile/$', views.editprofile, name='editprofile'),
        url(r'^profile/change_password/$', views.change_password, name='change_password'),
        url(r'all_answers/(\d+)/$',views.all_answers,name='all_answers'),
        url(r'delete_comment/(\d+)/$',views.delete_comment,name='delete_comment'),
        url(r'^adskite-bot/$', views.adskite, name='adskite'),
        url(r'^hotel-booking/$', views.hotel_booking, name='hotel_booking'),
        url(r'^courses-details/$', views.course_details, name='course_details'),
        url(r'^weather-details/$', views.weather_details, name='weather_details'),
        url(r'^logout/$', views.signout, name='logout'),

]