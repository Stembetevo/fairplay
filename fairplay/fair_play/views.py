from django.shortcuts import render

# Create your views here.
def index(request):
    #Main page view
    return render(request, 'index.html')
