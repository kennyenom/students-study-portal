from re import template
from django.urls import path
from .import  views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='home'),
    # path('notes/',views.CreateNote.as_view(),name='notes'),
    path('note/',views.note,name='notes'),
    path('homework/',views.homework,name='homework'),
    path('todo/',views.todo,name='todo'),
    path('wiki/',views.Wikipedia,name='wiki'),
    path('conversion/',views.conversion,name='conversion'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='dashboard/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='dashboard/logout.html'),name='logout'),
    path('book/',views.book,name='book'),
    path('dic/',views.dictionary,name='dictionary'),
    path('tododel/<int:pk>/',views.TodoDelete.as_view(),name='todo-delete'),
    path('youtube/',views.youtube,name='youtube'),
    path('updatehw/<int:pk>/',views.updateHomework,name='update-hw'),
    path('deleten<int:pk>/',views.DeleteNote.as_view(),name='delete-notes'),
    path('deleteh<int:pk>/',views.DeleteHomework.as_view(),name='delete-homework'),
    path('note-detail<int:pk>/',views.NoteDetail.as_view(),name='note-detail'),
]