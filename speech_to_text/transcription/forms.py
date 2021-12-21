import os

from django.core.exceptions import ValidationError
from django.forms import forms


class TranscribeForm(forms.Form):
    """ A form that takes input for audio file and shows transcription when input is complete """

    audio_file = forms.FileField(help_text="Choose a file.")

    def clean_audio_file(self):
        """ Checks that a file is selected """

        file = self.cleaned_data['audio_file']

        if not file:
            raise ValidationError('Audio file was not provided.')

        return file
