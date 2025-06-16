from django.db import models


class ChatHistory(models.Model):
    question = models.TextField()
    answer = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    audio_file = models.FileField(upload_to='chatbot/audio/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
# Create your models here.
