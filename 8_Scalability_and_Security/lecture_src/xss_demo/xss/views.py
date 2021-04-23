from django.shortcuts import HttpResponse, render

# The url path that was entered gets reflected in the response.
# Javascript can be injected when using a URL like this:
# 127.0.0.1:8000/<script>alert('hi');</script>
def index(request, path):
    return HttpResponse(f"Requested Path: {path}")
