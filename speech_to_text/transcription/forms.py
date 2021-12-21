import os

from django.core.exceptions import ValidationError
<<<<<<< HEAD
from django import forms
=======
from django.forms import forms
>>>>>>> 5cbe19cb7620306dfc1d36bd168615aed0ac95ea


class TranscribeForm(forms.Form):
    """ A form that takes input for audio file and shows transcription when input is complete """

<<<<<<< HEAD
    audio_file = forms.FileField()
    multiple_speakers = forms.BooleanField(required=False)

    ALLOWED_EXTENSIONS = ['.wav', '.flac', '.opus', '.ogg']
=======
    audio_file = forms.FileField(help_text="Choose a file.")
>>>>>>> 5cbe19cb7620306dfc1d36bd168615aed0ac95ea

    def clean_audio_file(self):
        """ Checks that a file is selected """

        file = self.cleaned_data['audio_file']

<<<<<<< HEAD
        if not file.name.lower().endswith(tuple(self.ALLOWED_EXTENSIONS)):
            raise ValidationError('Only .wav, .flac, .opus and .ogg(opus encoded) are allowed')

=======
>>>>>>> 5cbe19cb7620306dfc1d36bd168615aed0ac95ea
        if not file:
            raise ValidationError('Audio file was not provided.')

        return file
