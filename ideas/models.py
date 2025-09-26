from django.db import models

from model_utils.fields import StatusField
from model_utils import Choices


class Idea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField("date published", auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # added status choices and StatusField with default
    STATUS = Choices('new', 'in_progress', 'done', 'archived')
    status = StatusField(default=STATUS.new)
    
    # added main picture (nullable for existing rows)
    # todo: set up media serving in dev and prod
    main_picture = models.ImageField(upload_to='ideas/main_pictures/', null=True, blank=True)


