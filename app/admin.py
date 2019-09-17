from django.contrib import admin

# Register your models here.
from app.models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'release_time', 'country', 'length', 'mark', 'director']