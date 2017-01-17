from django.shortcuts import render
from django.http import JsonResponse
from requests_oauthlib import OAuth1Session
import requests
from requests_oauthlib import OAuth1
import json
from .models import Token
from django.views.decorators.csrf import csrf_protect, csrf_exempt



CONSUMER_KEY = "T3Bzs2t0XavyiqBOYBIgfoNwE"
CONSUMER_SECRET = "MM16sqoTdPuuTBlVB0BpC6aqLWDfRGP4OUZMAPl7hP9upVGJeB"
# ACCESS_KEY = "820285096074719233-w8kj7tX2WNzfiFuyXKqTPazxeytceZp"
# ACCESS_SECRET = "lyoCa8YL92Czygdp97U1CZZ71aoUwnzgHfPeKCMFO6bzc"
request_token_url = 'https://api.twitter.com/oauth/request_token'
base_authorization_url = 'https://api.twitter.com/oauth/authorize'
access_token_url = 'https://api.twitter.com/oauth/access_token'
get_tweets_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
post_tweets_url = 'https://api.twitter.com/1.1/statuses/update.json'

# Create your views here.


def sign_in_using_twitter(request):
    return render(request, 'twitter_app/sign_in.html', {})


def init_oauth(request):
	oauth = OAuth1Session(CONSUMER_KEY,
							client_secret=CONSUMER_SECRET,
							callback_uri="http://localhost:8080/show_tweets")
	fetch_response = oauth.fetch_request_token(request_token_url)
	authorize_url = base_authorization_url + "?oauth_token={0}".format(fetch_response.get("oauth_token"))
	return JsonResponse({"redirect_url":authorize_url})


def show_tweets(twitter_response):
	oauth = OAuth1Session(CONSUMER_KEY,
							client_secret=CONSUMER_SECRET,
							resource_owner_key=twitter_response.GET.get('oauth_token', None),
							verifier=twitter_response.GET.get('oauth_verifier', None))
	oauth_tokens = oauth.fetch_access_token(access_token_url)
	oauth = OAuth1(CONSUMER_KEY,
					client_secret=CONSUMER_SECRET,
					resource_owner_key=oauth_tokens.get('oauth_token'),
					resource_owner_secret=oauth_tokens.get('oauth_token_secret'))
	response = requests.get(url=get_tweets_url, auth=oauth, params={"count":50})
	save_token(oauth_tokens)
	return render(twitter_response, 'twitter_app/show_tweet.html', {"tweets":json.loads(response.text)})


def save_token(oauth_tokens):
	record = Token.objects.filter(user_id=oauth_tokens.get('user_id')).count()
	if not record:
		token = Token(oauth_token=oauth_tokens.get('oauth_token'),
						oauth_secret=oauth_tokens.get('oauth_token_secret'),
						user_id=oauth_tokens.get('user_id'))
	else:
		token = Token.objects.get(user_id=oauth_tokens.get('user_id'))
		token.oauth_token = oauth_tokens.get('oauth_token')
		token.oauth_secret = oauth_tokens.get('oauth_token_secret')
	token.save()


@csrf_exempt
def post_tweet(request):
	token = Token.objects.get(user_id=request.POST.get('user_id', ''))
	oauth = OAuth1(CONSUMER_KEY,
					client_secret=CONSUMER_SECRET,
					resource_owner_key=token.oauth_token,
					resource_owner_secret=token.oauth_secret)
	response = requests.post(url=post_tweets_url, auth=oauth, data={"status":request.POST.get('message', '')})
	response_data = json.loads(response.text)
	return JsonResponse({"message":"success" if response_data.has_key("id") else "error"})