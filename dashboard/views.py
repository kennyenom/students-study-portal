from django.shortcuts import redirect, render
from django.views.generic import ListView,DetailView,DeleteView,CreateView,UpdateView
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
import requests
from youtubesearchpython import VideosSearch
import wikipedia
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'dashboard/home.html')

def note(request):
    if request.method == 'POST':
        form = CreateNoteForm(request.POST)
        if form.is_valid():
            instnce = form.save(commit=False)
            instnce.user = request.user
            instnce.save()
            return redirect('notes')
    else:
        form = CreateNoteForm()
    note = Notes.objects.filter(user=request.user)
    return render(request,'dashboard/notes.html',{'note':note,'form':form})

class CreateNote(CreateView):
    form_class = CreateNoteForm
    template_name = 'dashboard/notes.html'
    success_url = reverse_lazy('notes')
    message_success_url ='created succesfully'
    
    def form_valid(self,form,*args,**kwargs):
        self.object= form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return super().form_valid(form)
    

class DeleteNote(DeleteView):
    model = Notes
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('notes')
    success_message_url = 'delited succesfully'

class NoteDetail(DetailView):
    model = Notes
    template_name = 'dashboard/notes_detail.html'
    context_object_name ='note'


def homework(request,*args,**kwargs):
    if request.method == 'POST':
        form = CreateHomeWork(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            # username = form.cleaned_data(instance=request.user)
            messages.success(request,f"homework succesfully created by ")
            return redirect('homework')

    else:
        form = CreateHomeWork()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done= False

    context = {
        'form':form,
        'home':homework,
        'homework_done':homework_done,

    }
    return render(request,'dashboard/homework.html',context)


class DeleteHomework(DeleteView):
    model = Homework
    template_name = 'dashboard/confirm_delete2.html'
    success_url = reverse_lazy('homework')

def updateHomework(request,pk):
    homework = Homework.objects.get(pk=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def youtube(request):
    if request.method == 'POST':
        form = YoutubeForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list,
            }
            return render(request,'dashboard/youtube.html',context)
    else:
        form = YoutubeForm()
    context = {
        'form':form
    }
    return render(request,'dashboard/youtube.html',context)

def todo(request):
    if request.method == 'POST':
        todo = TodoForm(request.POST)
        if todo.is_valid():
            instance = todo.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('todo')
    else:
        todo = TodoForm()

    todos = Todo.objects.filter(user=request.user)
    if len(todos) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'todo':todo,
        'todos':todos,
        'todo_done':todo_done,
        
    }
    return render(request,'dashboard/todo.html',context)

class TodoDelete(DeleteView):
    model = Todo
    template_name = 'dashboard/confirm_delete3.html'
    success_url = reverse_lazy('todo')

def book(request):
    if request.method == 'POST':
        form = YoutubeForm(request.POST)
        text = request.POST['text']
        url = 'https://www.googleapis.com/books/v1/volumes?q='+ text
        r = requests.get(url)
        i= r.json()
        result_list = []
        for k in range(10):
            result_dict = {
                'title':i['items'][k]['volumeInfo']['title'],
                'sub':i['items'][k]['volumeInfo'].get('subtitle'),
                'desc':i['items'][k]['volumeInfo'].get('description'),
                'count':i['items'][k]['volumeInfo'].get('pageCount'),
                'rating':i['items'][k]['volumeInfo'].get('pagerating'),
                'categories':i['items'][k]['volumeInfo'].get('categories'),
                'thumbnail':i['items'][k]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':i['items'][k]['volumeInfo'].get('previewLink'),
               
            }
            result_list.append(result_dict)
            context ={
                'results':result_list,
                'form':form
            }
            return render(request,'dashboard/books.html',context)
        
    else:
        form = YoutubeForm(request.POST)

    context = {
        'form':form

    }
    return render(request,'dashboard/books.html',context)

def dictionary(request):
    if request.method == 'POST':
        form = YoutubeForm(request.POST)
        text = request.POST['text']
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en/'+ text
        r = requests.get(url)
        i = r.json()
        try:
            phonetics =i[0]['phonetics'][0]['text']
            audio =i[0]['phonetics'][0]['audio']
            definition =i[0]['meanings'][0]['definitions'][0]['definition']
            example =i[0]['meanings'][0]['definitions'][0]['example']
            synoyms=i[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'def':definition,
                'eg':example,
                'sy':synoyms

            }
        except:
            context = {
                'form':form,
                'input':''
            
                   }
        return render(request,'dashboard/dictionary.html',context)
    else:
        form = YoutubeForm()
        context = {
            'form':form
        }
    return render(request,'dashboard/dictionary.html',context)





def dic(request):
    form = YoutubeForm()
    return render(request,'dashboard/dictionary.html',{'form':form})

def Wikipedia(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = YoutubeForm(request.POST)
        serach = wikipedia.page(text)
        context ={
            'form':form,
            'title':serach.title,
            'link':serach.url,
            'details':serach.summary,
        }
        return render(request,'dashboard/wiki.html',context)

    else:
        form = YoutubeForm()
        context={
            'form':form,
            
        }
    return render(request,'dashboard/wiki.html',context)


def register(request):
    if request.method == 'POST': 
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()
        context = {
            'form':form
        }
    return render(request,'dashboard/register.html',context)

def conversion(request):
    return render(request,'dashboard/conversion.html')