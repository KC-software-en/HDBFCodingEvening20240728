# import render
from django.shortcuts import render
# import HttpResponse to test that the view shows after runserver
from django.http import HttpResponse

# Create your views here.
# create a view for the homepage of the app - load index.html into the function
def index(request):
    """A view for the homepage of the ChatApp - index. load html into the function

    :param request: The HTTP request object containing information about the client's request.
    :type request: HttpRequest
    :return: Return the index template
    :rtype: HttpResponse
    """
    # runserver to check if HttpResponse shows in webpage then comment out HttpResponse
    # return HttpResponse("<h2>Hello World</h2>")
    return render(request, "index.html")
