from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
import google.generativeai as genai
import json , os
from pytube import YouTube
import openai
import assemblyai as aai
import yt_dlp
import markdown
from bs4 import BeautifulSoup
from dotenv import load_dotenv
# Create your views here.
@login_required
def index(request):
    return render(request,'index.html')


# def yt_title(link):

#     yt = YouTube(link)
#     title = yt.title
#     return title


def yt_title(link):
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return info.get("title", "Title not found")
    except Exception as e:
        return f"Error: {str(e)}"


@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            yt_link = data['link']
            
            
        except (KeyError, json.JSONDecodeError):

            return JsonResponse({'error' :'Invalid data send'},status = 400)
        
       

        
        
        # get transcript
        title = yt_title(yt_link)
        transcription = get_transcription(yt_link)
        
        if not transcription:

            return JsonResponse({'error':'Failed to get transcript'},status = 500)
        # user Open AI to generate the blog
        
        blog_content = generated_blog_from_transcription(transcription)
        if not blog_content:
            return  JsonResponse({'error':'Failed to generate blog article'},status = 500)
        # save blog article ti database
        

        # return blog article as a resonse
        return JsonResponse({'content':blog_content})  
    else:
        return JsonResponse({'error' :'Invalid request method'},status = 405)
    




# def download_audio(link):

#     yt = YouTube(link)
#     video = yt.streams.filter(only_audio=True).first()
#     out_file = video.download(output_path=settings.MEDIA_ROOT)
#     base, ext = os.path.splittext(out_file)
#     new_file = base + '.mp3'
#     os.rename(out_file,new_file)

#     return new_file

def download_audio(link):
    try:
        output_path = settings.MEDIA_ROOT  # Define the output path

        ydl_opts = {
            'format': 'bestaudio/best',  # Get the best audio quality
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Save with video title
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Convert to MP3
                'preferredquality': '192',  # Set quality
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info)  # Original filename before conversion
            mp3_filename = filename.rsplit('.', 1)[0] + '.mp3'  # Change extension to .mp3
            
            return mp3_filename  # Return the final MP3 file path

    except Exception as e:
        return f"Error: {str(e)}"
    

def get_transcription(link):
    
    audio_file = download_audio(link)
    aai.settings.api_key = os.getenv("AAI_API_KEY")

    transcriber = aai.Transcriber()
    transcript  = transcriber.transcribe(audio_file)

    return transcript.text

def clean_markdown(text):
    """Convert Markdown to plain text by first converting it to HTML, then stripping tags."""
    html = markdown.markdown(text)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

genai.configure(api_key=os.getenv("GENAI_API_KEY"))
def generated_blog_from_transcription(transcription):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Prompt to generate a blog from the YouTube link
        prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article display point wise and easy to undersand for readers. :\n\n{transcription}\n\nArticle:"


        response = model.generate_content(prompt)

        clean_text = clean_markdown(response.text)  # Remove markdown formatting
        return clean_text   # Return the generated blog content

          
    except Exception as e:
        return f"Error: {str(e)}"



# def generated_blog_from_transcription(transcription):
#     openai.api_key = "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"
    
#     prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"

#     response = openai.Completion.create(
#         model="gpt-3.5-turbo",
#         prompt=prompt,
#         max_tokens=1000
#     )
    
#     generated_content = response.choices[0].text.strip()

#     return generated_content
def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/')


        else:

            error_message = 'Invalid Username or Password'

            return render(request,'login.html',{'error_message':error_message})
    return render(request,'login.html')


def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error creating account'
                return render(request, 'signup.html', {'error_message':error_message})
        else:
            error_message = 'Password do not match'
            return render(request, 'signup.html', {'error_message':error_message})
        
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')