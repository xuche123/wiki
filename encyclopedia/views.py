from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, entry):
    file = util.get_entry(entry)
    if file:
        html = markdown(file)
        return render(request, "encyclopedia/entry.html", {
            "html": html,
            "title": entry
        })
    else:
        return render(request, "encyclopedia/error.html")


def search(request):
    if request.method == "POST":
        q = request.POST["q"]
        if util.get_entry(q):
            return HttpResponseRedirect(reverse("wiki", args=[q]))
        else:
            lists = util.list_entries()
            matches = []
            for list in lists:
                if q.lower() in list.lower():
                    matches += [list]
            return render(request, "encyclopedia/search.html", {
                "matches": matches
            })
    return HttpResponseRedirect(reverse("index"))
