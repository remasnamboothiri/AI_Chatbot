from django.shortcuts import render
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import ChatHistory
from gtts import gTTS
import os
import requests
from decouple import config

NOVITA_API_KEY = config("NOVITA_API_KEY")
MODEL_ID = "qwen/qwen2.5-7b-instruct"
BASE_URL = "https://api.novita.ai/v3/openai"

def chat_view(request):
    answer_text = ""
    audio_url = ""
    image_url = ""
    question = ""

    if request.method == "POST":
        question = request.POST.get("question")

        custom_prompt = f"Answer this question in simple English in less than 10 short sentences:\n{question}"
        
        # Ensure the question is not empty
        if not question:
            return render(request, "chatbot/chat.html", {
                "question": "",
                "answer": "⚠️ No input received. Please try again.",
                "audio_url": "",
                "image_url": "",
            })


        headers = {
            "Authorization": f"Bearer {config('NOVITA_API_KEY')}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": custom_prompt},
            ],
        }

        try:
            response = requests.post(BASE_URL + "/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            answer_text = response.json()["choices"][0]["message"]["content"]

            ChatHistory.objects.create(question=question, answer=answer_text)

            # Generate voice in English instead of Malayalam
            tts = gTTS(text=answer_text, lang="en")
            audio_path = "chatbot/audio/response.mp3"
            audio_file = ContentFile(b"")
            tts.write_to_fp(audio_file)
            file_name = default_storage.save(audio_path, audio_file)
            audio_url = default_storage.url(file_name)

            if "picture" in question.lower() or "image" in question.lower():
                image_url = "https://via.placeholder.com/200?text=Image+Not+Supported"

        except requests.exceptions.RequestException as e:
            answer_text = f"⚠️ Error getting response from Novita API: {str(e)}"

    return render(request, "chatbot/chat.html", {
        "question": question,
        "answer": answer_text,
        "audio_url": audio_url,
        "image_url": image_url,
    })































# from django.shortcuts import render
# from django.conf import settings
# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
# from .models import ChatHistory
# from gtts import gTTS
# import os
# import requests
# from decouple import config

# NOVITA_API_KEY = config("NOVITA_API_KEY")
# MODEL_ID = "qwen/qwen2.5-7b-instruct"
# BASE_URL = "https://api.novita.ai/v3/openai"

# def chat_view(request):
#     answer_text = ""
#     audio_url = ""
#     image_url = ""
    
#     if request.method == "POST":
#         question = request.POST.get("question")
        
#         custom_prompt = f"Answer this question in simple English in only 10 short lines:\n{question}"

#         headers = {
#             "Authorization": f"Bearer {NOVITA_API_KEY}",
#             "Content-Type": "application/json",
#         }

#         payload = {
#             "model": MODEL_ID,
#             "messages": [
#                 {"role": "system", "content": "You are a helpful assistant. "},
#                 {"role": "user", "content": custom_prompt},
#             ],
#         }

#         try:
#             response = requests.post(BASE_URL + "/chat/completions", json=payload, headers=headers)
#             response.raise_for_status()
#             answer_text = response.json()["choices"][0]["message"]["content"]

#             # Save to chat history
#             ChatHistory.objects.create(question=question, answer=answer_text)

#             # Generate voice (TTS)
#             tts = gTTS(text=answer_text, lang="ml")
#             audio_path = "chatbot/audio/response.mp3"
#             audio_file = ContentFile(b"")
#             tts.write_to_fp(audio_file)
#             file_name = default_storage.save(audio_path, audio_file)
#             audio_url = default_storage.url(file_name)

#             # Optional image generation if keyword found
#             if "picture" in question.lower() or "image" in question.lower():
#                 image_url = "https://via.placeholder.com/200?text=Image+Not+Supported"

#         except requests.exceptions.RequestException as e:
#             answer_text = "⚠️ Error getting response from Novita API."

#     return render(request, "chatbot/chat.html", {
#         "question": question if request.method == "POST" else "",
#         "answer": answer_text,
#         "audio_url": audio_url,
#         "image_url": image_url,
#     })





        
        
        
        
        
        
        
        
    




