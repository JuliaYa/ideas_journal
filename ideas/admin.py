from django.contrib import admin

from .models import Idea, NoteEntry, NoteImage


class NoteImageInline(admin.TabularInline):
    model = NoteImage
    extra = 0


@admin.register(NoteEntry)
class NoteEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'idea', 'note_type', 'created_at']
    list_filter = ['note_type', 'created_at']
    inlines = [NoteImageInline]


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'created_at']
    list_filter = ['status']
