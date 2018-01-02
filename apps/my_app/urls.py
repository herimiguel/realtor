from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register, name='register'),
	url(r'^login$', views.login, name='login'),
	url(r'^dashboard$', views.dashboard, name='dashboard'),
	url(r'^logOut$', views.logOut, name='logout'),
	url(r'^(?P<id>\d+)/delete$', views.delete, name='delete'),
	url(r'^showBuyer$', views.showBuyer, name='showBuyer'),	
	url(r'^finance$', views.finance, name='finance'),	
	url(r'^englishDash$', views.englishDash, name='englishDash'),
	url(r'^spanishDash$', views.spanishDash, name='spanishDash'),
	url(r'^learn$', views.learn, name='learn')
]