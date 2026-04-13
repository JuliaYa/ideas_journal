from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Idea, NoteEntry, NoteImage


def _delete_file(field_file):
    """Delete a file from storage if it exists."""
    if field_file and field_file.storage.exists(field_file.name):
        field_file.storage.delete(field_file.name)


# --- Idea.main_picture ---

@receiver(pre_save, sender=Idea)
def delete_old_main_picture(sender, instance, **kwargs):
    """Remove old main_picture file when it's replaced or cleared."""
    if not instance.pk:
        return
    try:
        old = Idea.objects.get(pk=instance.pk)
    except Idea.DoesNotExist:
        return
    if old.main_picture and old.main_picture != instance.main_picture:
        _delete_file(old.main_picture)


@receiver(post_delete, sender=Idea)
def delete_main_picture_on_idea_delete(sender, instance, **kwargs):
    _delete_file(instance.main_picture)


# --- NoteImage.image ---

@receiver(post_delete, sender=NoteImage)
def delete_note_image_file(sender, instance, **kwargs):
    _delete_file(instance.image)


# --- NoteEntry.audio_file ---

@receiver(post_delete, sender=NoteEntry)
def delete_note_audio_file(sender, instance, **kwargs):
    _delete_file(instance.audio_file)
