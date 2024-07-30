# Project name
ChatApp

# Project description
A simple real-time chat application built with Django, Python, HTML, CSS. 

Functionality:
+ Allow users to enter a username before joining the chat.
+ Display a list of online users - incomplete
+ Send and receive messages in real-time.
+ Persist chat messages in local storage so that they are not lost on page refresh.
+ Display timestamps for each message.


# Installation section
1. Install Packages:
    + python -m pip install -r requirements.txt
1. Login to Docker Desktop
1. Open the Command Prompt
    + in Command Prompt (powershell) `docker run --rm -p 6379:6379 redis:7`
    + in Command Prompt (admin) `python manage.py runserver`
1. Open 2 web browsers e.g. Edge & Opera GX
1. paste the link from cmd where it says Starting ASGI/Daphne version 4.1.2 development server at http://127.0.0.1:8000/ in both browsers

# Usage section
Enter different usernames but the same room name in each browser then start chatting in the chatroom.