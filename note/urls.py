from django.urls import path
from . import views


urlpatterns =[
    path('', views.home, name='home'),
    path('note/<uuid:id>/', views.note_detail, name='note-detail'),
    path('note/create/', views.note_create, name='note-create'),
    path('note/update/<uuid:id>/', views.note_update, name='note-update'),
    path('note/delete/<uuid:id>/', views.note_delete, name='note-delete'),
    path('note/search_results/', views.note_search, name='note-search'),
    path('about/', views.about, name='about')

]

