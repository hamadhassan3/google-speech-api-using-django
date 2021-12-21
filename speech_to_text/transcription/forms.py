import os

from django.core.exceptions import ValidationError
from django import forms


class TranscribeForm(forms.Form):
    """ A form that takes input for audio file and shows transcription when input is complete """

    audio_file = forms.FileField()
    multiple_speakers = forms.BooleanField(required=False)

    ALLOWED_EXTENSIONS = ['.wav', '.flac', '.opus', '.ogg']

    def clean_audio_file(self):
        """ Checks that a file is selected """

        file = self.cleaned_data['audio_file']

        if not file.name.lower().endswith(tuple(self.ALLOWED_EXTENSIONS)):
            raise ValidationError('Only .wav, .flac, .opus and .ogg(opus encoded) are allowed')

        if not file:
            raise ValidationError('Audio file was not provided.')

        return file
