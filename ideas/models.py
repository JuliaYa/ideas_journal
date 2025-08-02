from django.db import models

class Status(models.Model):
    name = models.CharField()
    description = models.TextField()

class Idea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField("date published")
    updated_at = models.DateTimeField()
    status = Status

# как устанавливать дефолтные статусы? Я хочу добавлять сама типы статусов по моим идеям.
# Но по умолчанию должно быть сразу три доступных (New, In Progress, Done)

