from django.shortcuts import render
from markdown2 import markdown
from pathlib import Path

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
