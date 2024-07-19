# import render
from django.shortcuts import render
# import HttpResponse to test that the view shows after runserver
from django.http import HttpResponse

# Create your views here.
# create a view for the homepage of the app 
# - load index.html into the function
def index(request):
    """A view for the homepage of the ChatApp.

    :param request: The HTTP request object containing information about the client's request.
    :type request: HttpRequest
    :return: Return the index template
    :rtype: HttpResponse
    """
    # runserver to check if HttpResponse shows in webpage then comment out HttpResponse
    # return HttpResponse("<h2>Hello World</h2>")
    # render the index template
    return render(request, "index.html")

# create a view for the chat room of the app 
# - load chat_room.html into the function
def chat_room(request, room_name):
    """A view for the chat room of the ChatApp.

    :param request: The HTTP request object containing information about the client's request.
    :type request: HttpRequest
    :param room_name: The user inputs the name of the chat room they want to enter.
    :type room_name: str
    :return: Return the chat_room template
    :rtype: HttpResponse
    """
    # the response is the dictionary for the room names
    # pass the context variables into a single dictionary to render in the template correctly
    context = {"room_name": room_name}

    # render the context to the chat_room template of ChatApp
    return render(request, "chat_room.html", context)