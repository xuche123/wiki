from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from markdown2 import markdown
from . import util
import random


class NewEntryForm(forms.Form):
    title = forms.CharField(
        label="Title",
        required=True,
        max_length=100
    )
    content = forms.CharField(widget=forms.Textarea, required=True)

    def clean_title(self):
        title = self.cleaned_data['title']
        if title in util.list_entries():
            raise ValidationError("Page already exists!")
        return title


class EditEntryForm(NewEntryForm):
    def clean_title(self):
        title = self.cleaned_data['title']
        return title


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
                "count": len(matches),
                "matches": matches
            })
    return HttpResponseRedirect(reverse("index"))


def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid() and form.clean_title():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            file = util.get_entry(title)
            if file:
                html = markdown(file)
                return render(request, "encyclopedia/entry.html", {
                    "html": html,
                    "title": title
                })
            # return HttpResponseRedirect(reverse("index"))

            
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })

    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })


def edit(request, entry):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid() and form.clean_title():
            content = form.cleaned_data["content"]
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })
    return render(request, "encyclopedia/edit.html", {
        "form": EditEntryForm(initial={'title': entry, 'content': util.get_entry(entry)})
    })

def random_page(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect(reverse('wiki', args=[entry]))