from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import urllib
import json
import main.windowing

# Create your views here.
def home(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    print("session ID", request.session.session_key)
    return render(request, 'index.html')

def classify(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    print("session ID", request.session.session_key)
    return render(request, 'classify.html')

def getimage(request):
    print("session ID", request.session.session_key)
    data = {
        's': request.session.session_key
    }
    # urls = request.GET.get("image") #.split("~")
    # urllib.request.urlretrieve (urls, "file.dcm")
    # image = main.windowing._read()
    # # windowed = main.windowing.get_window()
    # data = {
    #     "image": main.windowing.get_blob(image).decode("utf-8"),
    #     # "windowed": main.windowing.get_blob(windowed)
    # }
# .decode("utf-8")
    return JsonResponse(data, status=200)