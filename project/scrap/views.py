'''
All view request is needed Authorization check.
'''
import hmac
import uuid
try:
    from hashlib import sha1
except ImportError:
    import sha
    sha1 = sha.sha

from django.shortcuts import render
from .models import Scrap, Category, User

def index(request):
    pass

def view_public_scrap(request, category_id=1):
    if request.method != 'GET':
        pass
        #Render Error Page... > Invalid Request
    
    try:
        category = Category.objects.get(id=category_id)
    except:
        pass
        #Render Error Page... > Category does not exist
    scrap = Scrap.objects.filter(category=category, is_public=True)
    #Render Public Scrap list Page... > Success!

def view_scrap(request, directory_name):
    if request.method != 'GET':
        pass
        #Render Error Page... > Invalid Request

    scrap = Scrap.objects.get(directory=directory_name)
    if scrap.user != scrap.user:
        pass
        #Render Error Page... > UnAuthorized
    #Render Scrap View Page... > Success!

def view_shared_scrap(request, share_key):
    if request.method != 'GET':
        pass
        #Render Error Page... > Invalid Request
    
    try:
        scrap = Scrap.objects.get(share_key=share_key)
    except:
        pass
        #Render Error Page... > Shared scrap does not exist.
    #Render Shared scrap page... Success!


