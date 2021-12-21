from django.db import models

# Create your models here.
from django.urls import reverse


class Transcript(models.Model):
    """ A model representing transcription of an audio file """

    transcript = models.CharField(max_length=20, help_text='Transcription of an audio file')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    # Metadata for the model
    class Meta:
        pass

    def get_absolute_url(self):
        """ Url to access a transcript """
        return reverse('transcript-detail-view', args=[str(self.id)])

    def __str__(self):
        """ String to represent an object of Transcript """
        return "Transcript " + str(self.id)
