from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
import json
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import RegisrationForm, PromptForm
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.html import strip_tags
import openai

def register(request):
    if request.method == 'POST':
        form = RegisrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get['email']
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(email=email, username= username, password= password )
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisrationForm()
    return render(request, 'registration/register.html', locals())


def write(request):
    API_KEY = settings.OPENAI_API_KEY
    openai.api_key = API_KEY

    if request.method == 'POST':            
        form = PromptForm(request.POST) 
        if form.is_valid():
            prompt = form.cleaned_data.get('prompt').strip()
            if not prompt:
                return JsonResponse({'error': 'Prompt is required'})
            
            prompt = strip_tags(prompt)  # Remove HTML tags
            prompt = prompt.replace('\n', '')  # Remove newlines
            
            try:
                print('Start')
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {'role': 'system', 'content': "You are an expert and helpful voiceover writer assistant."},
                    {'role': 'user', 'content': f'Write a short YouTube Shorts voice over based on, : "{prompt}", it must be 200 words or less'},
                ],
                temperature = 0.5,
                top_p=0.9,
                max_tokens=1300,
                frequency_penalty=0,
                presence_penalty=0
                )
                result =  { 'text' : f'{response.choices[0].message.content}'}
                print(result)

                return JsonResponse(result)

            except Exception as e:
                print('Error')
                return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid Request'})


def speech(request):

    ELEVENLABS_API_KEY = settings.ELEVENLABS_API_KEY
    
    if request.method == 'POST':
        # Get the text to synthesize speech from
        # text = request.body.decode('utf-8')
        data = json.loads(request.body)

        # Get the voice to use
        text = data.get('text').strip()
        voice = data.get('voice')

        # Synthesize speech from the text using the specified voice

        response = polly_client.synthesize_speech(VoiceId=voice,
                OutputFormat='mp3',
                Text=text)

        # Set the filename for the downloaded file
        filename = 'SHORTOVER_synthesized_voice_over.mp3'

        # Create the HTTP response with the synthesized audio data and the Content-Disposition header
        http_response = HttpResponse(response['AudioStream'].read(), content_type='audio/mpeg')
        http_response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return http_response
    else:
        # Return an HTTP 400 bad request response if the request method is not POST
        return HttpResponseBadRequest('Only POST requests are allowed.')


def voice(request):return render(request, 'voice.html')




def index(request):                 
    return render(request,'index.html')  




    
def error_404(request, exception):
    return render(request,'error.html')
def error_500(request):
    return render(request,'error.html')  
