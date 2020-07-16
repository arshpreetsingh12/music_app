from django.db import models
from django.contrib.auth.models import User
# Create your models here.

""" This table for admin's extra details. """
class AdminDetail(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=50, null=True, blank=True)
	address = models.CharField(max_length=100, null=True, blank=True)
	created_at  = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)