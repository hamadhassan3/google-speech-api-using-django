from django.shortcuts import render
from .forms import TranscribeForm
from .models import Transcript


def index(request):
    """ A request to transcribe an audio file. The audio file is received in request body """

    transcript = None
    if request.method == 'POST':
        # We execute the request only if the request is a POST request

        form = TranscribeForm(request.POST, request.FILES)
        print("HERE3")
        print(form.is_valid())

        # Check if the form is valid:
        if form.is_valid():
            print("HERE2")

            # Retrieving the audio file from transcribe request that form has submitted
            audio_file = request.FILES['audio_file']

            print(audio_file.name)
            # We need to transcribe now

            transcript = Transcript(transcript="This is the transcript")

    else:
        # If the request method is not POST, we simply display the form
        form = TranscribeForm()

    context = {
        'form': form,
        'transcript': transcript
    }

    return render(request, 'index.html', context)
