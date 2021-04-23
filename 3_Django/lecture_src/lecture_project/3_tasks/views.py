from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

class NewTaskForm(forms.Form):
    # the members of this class map to HTML form <input> elements
    task = forms.CharField(label="New Task")
    # the min and max values provide client-side validation (in the generated HTML),
    # but the Form class can also be used for server side validation with is_valid()
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })

def add(request):
    # POST method used when submitting the form
    if request.method == "POST":
        # Create a form instance and populate it with data from the request: 
        # This is called “binding data to the form” (it is now a bound form)
        # https://docs.djangoproject.com/en/3.1/topics/forms/#the-view
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
    # if GET method (used when opening the page)
    else:
        return render(request, "tasks/add.html", {
            "form": NewTaskForm()
        })
