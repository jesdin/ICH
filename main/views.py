from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def classify(request):
    return render(request, 'classify.html')