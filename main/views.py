from django.shortcuts import render
from django.http import JsonResponse, FileResponse, Http404
import urllib
import os
from main.windowing import _save, get_window
from main.classify import get_classification

# Create your views here.
def home(request):
    # create session if it does not exist
    if not request.session.exists(request.session.session_key):
        request.session.create()
    return render(request, 'index.html')

def predict(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    return render(request,'predict.html')

def classify(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    return render(request, 'classify.html')

def getimage(request):
    # get session key
    skey = request.session.session_key

    # save dicom file
    urls = request.GET.get("image")
    PATH = "assets\\tmp\\"+ skey
    urllib.request.urlretrieve (urls, PATH + ".dcm")
    
    # get windowed image and save images to tmp
    image = get_window(PATH + ".dcm")
    _save(PATH, image)

    # get prediction
    prediction = get_classification(image)
    data = {
        'path': PATH,
        'prediction': prediction
    }

    # delete dcm file
    os.remove(PATH + ".dcm")
    return JsonResponse(data, status=200)

def paper(request):
    try:
        return FileResponse(open('assets\\pdf\\Paper.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()