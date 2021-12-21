from django.shortcuts import render
from .forms import TranscribeForm
from .models import Transcript
from google.cloud import speech_v1p1beta1 as speech


def index(request):
    """ A request to transcribe an audio file. The audio file is received in request body """

    transcript = None
    if request.method == 'POST':
        # We execute the request only if the request is a POST request

        form = TranscribeForm(request.POST, request.FILES)

        # Check if the form is valid:
        if form.is_valid():

            # Retrieving the audio file from transcribe request that form has submitted
            audio_file = request.FILES['audio_file']
            is_multiple_speakers = form['multiple_speakers'].value()

            # We have received the file and its ready for transcription

            client = speech.SpeechClient()

            language_code = "en-US"

            # Setting encoding according to file types
            # Providing encoding is optional for flac and wav files

            if audio_file.name.endswith(".ogg"):
                encoding = speech.RecognitionConfig.AudioEncoding.OGG_OPUS
            elif audio_file.name.endswith(".flac"):
                encoding = speech.RecognitionConfig.AudioEncoding.FLAC
            elif audio_file.name.endswith(".wav"):
                encoding = speech.RecognitionConfig.AudioEncoding.MULAW
            elif audio_file.name.endswith(".opus"):
                encoding = speech.RecognitionConfig.AudioEncoding.OGG_OPUS

            # Configuration for multiple speakers
            multiple_speakers = speech.SpeakerDiarizationConfig(
                enable_speaker_diarization=is_multiple_speakers,
                min_speaker_count=2
            )

            # Setting configuration options for the transcription
            # Try to provide as much options as possible as it results in better quality
            config = {
                "encoding": encoding,
                "language_code": language_code,
                "diarization_config": multiple_speakers,
                "enable_automatic_punctuation": True,
                "profanity_filter": True
            }

            content = audio_file.read()
            audio = {"content": content}

            response = client.recognize(request={"config": config, "audio": audio})

            transcript = ""

            if is_multiple_speakers:

                # Each word in the transcription object contains a speaker tag.
                # We need to separate each speaker's transcript using this tag. The result for
                # multiple speakers is stored in the last result.
                result = response.results[-1]

                all_words = result.alternatives[0].words

                curr_tag = None

                speaker_counter = 1
                speakers = {}

                # Adding speaker tags to each speaker's transcription
                for word in all_words:

                    if not curr_tag:
                        curr_tag = word.speaker_tag
                        speakers[curr_tag] = speaker_counter
                        speaker_counter += 1
                        transcript += "Speaker " + str(speakers[curr_tag]) + ": "

                    transcript += word.word + " "
            else:

                # Multiple speakers do not need to be checked
                for result in response.results:
                    transcript += result.alternatives[0].transcript + " "

            transcript = Transcript(transcript=transcript)

            # Transcript is saved so that it can be used later if needed
            transcript.save()



    else:
        # If the request method is not POST, we simply display the form
        form = TranscribeForm()

    context = {
        'form': form,
        'transcript': transcript
    }

    return render(request, 'index.html', context)
