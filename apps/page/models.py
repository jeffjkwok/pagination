from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import pytz, math
# Create your models here.
class UserManager(models.Manager):
	def getData(self, data):
		if data:
			page = int(data['page'])
			name = data['name']
			start = data['from']
			end = data['to']
		else:
			page = 1
			name =''
			start=''
			end = ''
		if start=='':
			start = datetime(1000,01,01)
		if end =='':
			end = datetime.now()

		first_name_search = User.objects.filter(first_name__icontains=name).filter(created_at__range=(start,end))
		first_name_list = [user for user in first_name_search]
		last_name_search = User.objects.filter(last_name__icontains=name).filter(created_at__range=(start,end))
		last_name_list = [user for user in last_name_search]
		for user in last_name_list:
			if user not in first_name_list:
				first_name_list.append(user)

		pages = range(1, int(math.ceil(len(first_name_list)/10.0))+1)
		print pages
		print len(first_name_list)

		if page == 1:
			allUsers = first_name_list[:10]
		else:
			fromUsers = (page-1)*10
			toUsers = page*10
			allUsers = first_name_list[fromUsers:toUsers]

		context = {
			'users': allUsers,
			'pages': pages
		}
		return context

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
