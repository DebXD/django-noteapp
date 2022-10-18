
from django.shortcuts import render, redirect
from .models import Note, decrypt_note, decrypt_single_note
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CreateNoteForm

from cryptography.fernet import Fernet

def home(request):

    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user = request.user.id
        notes = Note.objects.filter(user_id=user).order_by('-date_posted').select_related()# using filter method to retrive multiple objects in a query set..... 
                                                                                            #use get method to retrive only one object
        notelist = decrypt_note(notes, user)
        context = {'notes': notelist}                                        
        return render(request, 'note/home.html', context)

def note_detail(request, id):
    user = request.user
    if user.is_authenticated:

        user_notes = Note.objects.filter(user_id=user.id).select_related()
        note = user_notes.get(id=id)
        user = user_notes.filter(user_id=user.id).first()
        dec_note = decrypt_single_note(note, user)
        context = { 'note' : dec_note}
        return render(request, 'note/note_detail.html', context)
    else:
        messages.warning(request, 'Login to get Your Note!')
        return redirect('login')

def note_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateNoteForm(request.POST)
            
            if form.is_valid():
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')
                if title == '' and content == '':
                    messages.warning(request, 'No Text Entered')
                    return redirect('home')
                else:
                    user_obj = User.objects.get(id=request.user.id)
                    key = Fernet.generate_key()

                    f = Fernet(key)
                    enc_title = f.encrypt(title.encode())
                    enc_content = f.encrypt(content.encode())

                    note_obj = Note(title=enc_title, content=enc_content, key=key, user_id=user_obj)
                    note_obj.save()
                    messages.success(request, 'Your note has been saved!')
                    return redirect('home')
            else:
                messages.warning(request, 'There is something wrong!')
                return redirect('home')

        else:
            form = CreateNoteForm()
            context = { 'form': form}
            return render(request, 'note/note_create.html', context)
    else:
        messages.warning(request, 'Login to Create Note!')
        return redirect('login')

def note_update(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            updated_title = request.POST.get('title')
            updated_content = request.POST.get('content')
            if updated_title == '' and updated_content == '':
                messages.warning(request, 'No Text Entered!')
                return redirect('home')
            else:
                note_obj = Note.objects.filter(id=id).select_related().first()
                f = Fernet(note_obj.key)
                enc_title = f.encrypt(updated_title.encode())
                enc_content = f.encrypt(updated_content.encode())
                note_obj.title=enc_title
                note_obj.content=enc_content
                note_obj.save()
 
                    #note_obj = Note(title=enc_title, content=enc_content, key=note_obj.key, user_id=user_obj)
                    #note_obj.save()
                messages.success(request, 'Your note has been Updated!')
                return redirect(f'/note/{id}/')

        else:
            note=Note.objects.get(id=id)
            user = User.objects.get(id=request.user.id)
            dec_note = decrypt_single_note(note,user)
            context = { 'note':dec_note }
            return render(request, 'note/note_update.html', context)
    else:
        messages.warning(request, 'Login to Update')
        return redirect('login')

def note_delete(request, id):
    if request.method == 'POST':
        note_obj = Note.objects.get(id=id)
        note_obj.delete()
        messages.warning(request, 'Note Deleted Successfully!')
        return redirect('home')
    else:
        return render(request, 'note/note_delete.html')

def note_search(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        print(query)
        if query == '':
            messages.warning(request, 'No query text')
            return redirect('home')
        else:
            user_notes = Note.objects.filter(user_id=request.user.id).select_related()
            new_notelist = []
            
            for note in user_notes:
                key = bytes(note.key)# convert the memoryview type to bytes
                f = Fernet(key)
                title = f.decrypt(bytes(note.title)).decode()# convert the memoryview type to bytes
                content = f.decrypt(bytes(note.content)).decode()# convert the memoryview type to bytes
                query = query.lower()
                

                if title is  None:
                    whole_note = content.lower()
                    if whole_note.find(query) == -1 :
                        pass
                    else:
                        new_notelist.append(note)
                elif content is None:
                    whole_note = title.lower()
                    if whole_note.find(query) == -1 :
                        pass
                    else:
                        new_notelist.append(note)
                else:
                    whole_note = title.lower() + ' ' + content.lower()
                    if whole_note.find(query) == -1 :
                        pass
                    else:
                        new_notelist.append(note)

            if len(new_notelist) == 0:# if query does not found
                print('its not none')
                messages.warning(request, 'No Results Found!')
                return redirect('home')
            else:
                dec_notelist = decrypt_note(new_notelist, request.user.id)
                context = { 'notes' : dec_notelist}       
                return render(request, 'note/search_result.html', context)

def about(request):
    return render(request, 'note/about.html')