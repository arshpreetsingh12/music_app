from api.models import *
from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect,HttpResponse 

def GetUserRole(request):
    if request.user.is_authenticated:
        try:
            user_role = ""
            if request.user.is_superuser or request.user.is_staff:
                user_role = "Admin"
            else:
                user_dtl = UserDetail.objects.get(user = request.user)   
                if user_dtl.is_artist:
                    user_role = "Artist"
                else:
                     user_role = "Listener"
            return {
               'user_role':user_role
                }

        except Exception as e:
            return {}

    else:
       return {}
