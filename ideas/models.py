from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField


class Idea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField('date published', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # added status choices and StatusField with default
    STATUS = Choices('new', 'in_progress', 'done', 'archived')
    status = StatusField(default=STATUS.new)

    # added main picture (nullable for existing rows)
    # todo: set up media serving in dev and prod
    main_picture = models.ImageField(upload_to='ideas/main_pictures/', null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']


class NoteEntry(models.Model):
    NOTE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('audio', 'Audio'),
    ]

    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='notes')
    note_type = models.CharField(max_length=5, choices=NOTE_TYPE_CHOICES)
    text = models.TextField(null=True, blank=True)
    audio_file = models.FileField(upload_to='ideas/notes/audio/', null=True, blank=True)
    transcription = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class NoteImage(models.Model):
    note = models.ForeignKey(NoteEntry, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ideas/notes/images/')
    created_at = models.DateTimeField(auto_now_add=True)
