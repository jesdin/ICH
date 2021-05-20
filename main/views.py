from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import urllib
import os
from main.windowing import _save

# Create your views here.
def home(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    print("session ID", request.session.session_key)
    return render(request, 'index.html')

def predict(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    return render(request,'predict.html')

def classify(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    # print("tmp\\"+ request.session.session_key  +".dcm")
    return render(request, 'classify.html')

def getimage(request):
    skey = request.session.session_key
    urls = request.GET.get("image")
    path = "assets\\tmp\\"+ skey
    urllib.request.urlretrieve (urls, path + ".dcm")
    _save(path)
    data = {
        'path': path
    }
    os.remove(path + ".dcm")
    # data = {
    #     "image": main.windowing.get_blob(image).decode("utf-8"),
    #     # "windowed": main.windowing.get_blob(windowed)
    # }
# .decode("utf-8")
    return JsonResponse(data, status=200)
