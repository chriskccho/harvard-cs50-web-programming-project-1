from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
import secrets
from django.contrib import messages



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
    

def newentry(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title.upper() in (entry.upper() for entry in util.list_entries()):
            messages.error(request, 'This entry is already in the encyclopedia.')
            return HttpResponseRedirect(reverse("newentry"))
        else: 
            util.save_entry(title,description)
            return HttpResponseRedirect(reverse('entry', kwargs={'entry': title}))
    return render(request, "encyclopedia/newentry.html")
    
def editentry(request, entry):
    page = util.get_entry(entry)
    if request.method == 'POST':
        changed = request.POST.get('edited')
        util.save_entry(entry,changed)
        return HttpResponseRedirect(reverse('entry', kwargs={'entry': entry}))
    return render(request, "encyclopedia/editentry.html", {
        "entrycontent":page,
        "entryTitle": entry
    })
    




            


