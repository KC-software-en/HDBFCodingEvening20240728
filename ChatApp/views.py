# import render
from django.shortcuts import render
# import HttpResponse to test that the view shows after runserver
from django.http import HttpResponse

# Create your views here.
# create a view for the homepage of the app - index. load html into the function
def index(request):
    # runserver to check if HttpResponse shows in webpage then comment out HttpResponse
    # return HttpResponse("<h2>Hello World</h2>")
    return render(request, "index.html")
