import random
from http import HTTPStatus
from markdown2 import Markdown
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import html

from . import util
from .forms import NewPageForm


def index(request):
    # The search form contains an action attribute to redirect to this view after submitting.
    # The form submits its data with the GET method.
    # That means that the submitted data will be visible in the URL.
    # The key "q" is the name attribute of the HTML input element and
    # its value will be the string that the user wants to search for.
    if request.method == "GET" and "q" in request.GET and len(request.GET["q"]) > 0:
        # redirect to /wiki/<search_string>
        return HttpResponseRedirect(reverse('wiki_page', args=[request.GET["q"]]))

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, page):
    status_code = HTTPStatus.OK
    page_content = ""
    page_found = True

    # check if there is a Markdown file with the same name as the requested page
    if not util.get_entry_name(page):
        page_found = False
        # get all entries where the first letters of the requested page name match
        entries = util.list_entries()
        entries_match = [entry for entry in entries if entry.lower().find(page.lower()) == 0]
        if len(entries_match) > 0:
            # generate Markdown content to display
            page_content = (
                f"# {page}\n"
                "The following entries are matching:\n\n"
            )
            for entry in entries_match:
                entry_link = reverse('wiki_page', args=[entry])
                page_content = page_content + f"* [{entry}]({entry_link})\n"
        else:
            page_content = (
                f"# {page}\n"
                "Page not found"
            )
            status_code = HTTPStatus.NOT_FOUND
    else:
        page_content = util.get_entry(page)
        # The page content that comes from the user must be escaped to prevent XSS,
        # because in the template autoescape is turned off.
        page_content = html.escape(page_content)

    markdowner = Markdown()
    page_content = markdowner.convert(page_content)
    return render(request, "encyclopedia/wiki_page.html", {
        "page": page,
        "page_content": page_content,
        "page_found": page_found
    }, status=status_code)

def newPage(request):
    if request.method == "POST":
        # bind the form: https://docs.djangoproject.com/en/3.1/topics/forms/#the-view
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('wiki_page', args=[title]))
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })

    return render(request, "encyclopedia/new_page.html", {
        'form': NewPageForm()
    })

def editPage(request, page):
    page = util.get_entry_name(page)
    if not page:
        return HttpResponse(f"<p>Error {HTTPStatus.NOT_FOUND}: Page not found</p>",
            status=HTTPStatus.NOT_FOUND)
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(page, content)
        return HttpResponseRedirect(reverse('wiki_page', args=[page]))

    page_content = util.get_entry(page)
    return render(request, "encyclopedia/edit_page.html", {
        "page": page,
        "page_content": page_content
    })

def randomPage(request):
    pages = util.list_entries()
    num_pages = len(pages)
    if num_pages == 0:
        return HttpResponse(f"<p>Error {HTTPStatus.NOT_FOUND}: Page not found</p>",
            status=HTTPStatus.NOT_FOUND)

    rand_ind = random.randrange(num_pages)
    return HttpResponseRedirect(reverse('wiki_page', args=[pages[rand_ind]]))
