from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import secrets



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdowner = Markdown()
    page = util.get_entry(entry)
    if page is None:
        return render(request, "encyclopedia/noentry.html", {
            "entryTitle": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(page),
            "entryTitle": entry
        })

def search(request):
    if request.method == 'GET':
        searched = request.GET.get('q')
        listofentries = util.list_entries()
        substring = list()
        for i in range(len(listofentries)):
            if listofentries[i].upper() == searched.upper():
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': searched}))
            if searched.upper() in listofentries[i].upper():
                substring.append(listofentries[i])
        return render(request, "encyclopedia/index.html", {
            'entries':substring
        })

def random(request):
    lstofentries = util.list_entries()
    random_entry = secrets.choice(lstofentries)
    return HttpResponseRedirect(reverse('entry', kwargs={'entry': random_entry}))
    



            


