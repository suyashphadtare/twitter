from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.sign_in_using_twitter, name='sign_in'),
    url(r'^init_oauth$', views.init_oauth, name='init_oauth'),
    url(r'^show_tweets$', views.show_tweets, name='show_tweets'),
    url(r'^post_tweet$', views.post_tweet, name='post_tweets')
]