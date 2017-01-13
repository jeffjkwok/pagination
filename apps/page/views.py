from django.shortcuts import render,redirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import User
import requests

# Create your views here.
def index(req):
	users = User.objects.all()
	if len(users) == 0:
		response = requests.get('https://randomuser.me/api/?results=33')
		results = response.json()['results']
		for result in results:
			User.objects.create(first_name=result['name']['first'], last_name=result['name']['last'], email = result['email'], created_at= result['registered'] )

	if req.method == "POST":
		return render(req, 'page/index.html', User.objects.getData(req.POST))
	return render(req, 'page/index.html', User.objects.getData(None))

