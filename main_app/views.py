from typing import Any, Dict
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views import View
from .models import Artist, Song, Playlist
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["playlists"] = Playlist.objects.all()
        return context
    
class About(TemplateView):
    template_name = "about.html"

class SongList(TemplateView):
    template_name = "song_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["songs"] = Song.objects.all()
        return context 

# class Song:
#     def __init__(self, title, artist):
#         self.title = title
#         self.artist = artist  

class ArtistList(TemplateView):
    template_name = "artist_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # to get the query parameter we have to acccess it in the request.GET dictionary object        
        name = self.request.GET.get("name")
        # If a query exists we will filter by name 
        if name != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["artists"] = Artist.objects.filter(name__icontains=name)
            context["header"] = f"searching for {name}"
        else:
            context["artists"] = Artist.objects.all()
            context["header"] = "All trending artists"
        return context
    
class ArtistCreate(CreateView):
    model = Artist
    fields = ['name', 'img', 'bio', 'verified_artist']
    template_name = "artist_create.html"
    success_url = "/artists/"

class ArtistDetail(DetailView):
    model = Artist
    template_name = "artist_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playlists'] = Playlist.objects.all()
        return context

class ArtistUpdate(UpdateView):
    model = Artist
    fields = ['name', 'img', 'bio', 'verified_artist']
    template_name = "artist_update.html"
    success_url = "/artists/"

class ArtistDelete(DeleteView):
    model = Artist
    template_name = "artist_delete_confirmation.html"
    success_url = "/artists/"

class SongCreate(View):

    def post(self, request, pk):
        title = request.POST.get("title")
        length = request.POST.get("length")
        artist = Artist.objects.get(pk=pk)
        Song.objects.create(title=title, length=length, artist=artist)
        return redirect('artist_detail', pk=pk)

class PlaylistSongAssoc(View):

    def get(self, request, pk, song_pk):
        assoc = request.GET.get('assoc')
        if assoc == "remove":
            Playlist.objects.get(pk=pk).songs.remove(song_pk)
        if assoc == "add":
            Playlist.objects.get(pk=pk).songs.add(song_pk)
        return redirect('home')

# songs = [
#     Song("Lost", "hayd"),
#     Song("Never Ending Song", "Connor Gray"),
# ]

