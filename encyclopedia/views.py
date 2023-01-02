from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
from markdown2 import Markdown
import random

from encyclopedia import util
from encyclopedia.forms import CreateNewEntryForm, EditEntryForm


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    content_md = util.get_entry(title)
    if content_md:
        convertor = Markdown()
        content_html = str(convertor.convert(content_md)).strip()
        page_title = content_md.split('\n')[0].split(' ')[1]

        return render(request,"encyclopedia/page.html", context={"content": content_html, "title": page_title})
    else:
        return render(request, "encyclopedia/pageNotFound.html", context={"title": title})
        

def search(request):
    if request.method == "GET":
        search_item = request.GET["q"]
        content_md = util.get_entry(search_item)
        
        if content_md:
            convertor = Markdown()
            content_html = str(convertor.convert(content_md)).strip()
            page_title = content_md.split('\n')[0].split(' ')[1]
            return render(request,"encyclopedia/page.html", context={"content": content_html, "title": page_title})
        else:
            # If there is a substring in a query those entries would be returned
            existing_pages = util.list_entries()
            entries = []
            found = False
            for page in existing_pages:
                if search_item in page:
                    entries.append(page)
                    found = True 
            return render(request, "encyclopedia/search.html", context={"entries": entries, "search_item":search_item, "found":found})         
        
    
    return redirect("encyclopedia:index")


def new_page(request):
    create_form = CreateNewEntryForm()
    if request.method == "POST":
        form = CreateNewEntryForm(request.POST)
        if form.is_valid():
            title = str(form.cleaned_data["title"])
            content = form.cleaned_data["content"]
            
            # Check whether this title exists already in list of entries
            for entry in util.list_entries():
                if title.casefold() == entry.casefold():
                    return render(request, 'encyclopedia/create.html', context={"error": True, "title": entry})
           
            # if this line is executed then, it means no entries in list_entries() with title name
            content= f"# {title}\n" + content
            util.save_entry(title, content)
            return redirect(reverse('encyclopedia:wiki', kwargs={"title": title}))    

    return render(request, 'encyclopedia/create.html', context={"create_form": create_form, "error": False})


def edit_page(request, title):
    if request.method == "GET":
        content_md = util.get_entry(title)
        if content_md:
            form = EditEntryForm(initial={"title": title, "content":content_md})
            return render(request, 'encyclopedia/edit.html', context={"form": form, "error": False, "entry_title": title})
        else:
            return render(request, 'encyclopedia/edit.html', context={"error": True, "entry_title": title})
    
    elif request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            edited_title = str(form.cleaned_data["title"])
            edited_content = form.cleaned_data["content"]
            
            # There should be always in the content # {title} ...
            first_two_char = [edited_content[0], edited_content[1]]
            if not "#" in first_two_char:
                edited_content = f"# {edited_title}\n" + edited_content
            
            # If title is changed then in content # {title} should be also changed with edited_title no matter
            # of user edition
            if edited_title.casefold() != title.casefold():
                edited_content = f"# {edited_title}\n" + "".join(edited_content.split('\n')[1:])
                # Entry with old title name is going to be deleted
                util.delete_entry(title)
                # Page title is edited title
                title = edited_title
                
                
            util.save_entry(edited_title, edited_content)
            
            return redirect(reverse('encyclopedia:wiki', kwargs={"title": title}))
        
        else:
            return redirect(reverse('encyclopedia:edit_page', kwargs={"title": title}))
        

def delete_page(request, title):
    all_entries = util.list_entries()
    if title in all_entries:
        util.delete_entry(title)
    return redirect(reverse('encyclopedia:index'))


def random_page(request):
    all_entries = util.list_entries()
    random_entry_title = random.choice(all_entries)
    return redirect(reverse('encyclopedia:wiki', kwargs={"title": random_entry_title}))
