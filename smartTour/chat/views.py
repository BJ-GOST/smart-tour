from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
import json

# Configure the Gemini API with the API key from settings
genai.configure(api_key=settings.API_KEY)

# Define the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the GenerativeModel with the specified configuration
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="Provide tour guidance and information."
)


# Create your views here.
@login_required(login_url='login')
def home(request):
    template_name = 'home.html'
    return render(request, template_name)

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        try:
            # Start a chat session with the user's message
            chat_session = model.start_chat(history=[{"role": "user", "parts": [user_message]}])
            response = chat_session.send_message(user_message)

            # Extract the response text
            reply = response.text.strip() if response and response.text else "Sorry, I couldn't respond."
            return JsonResponse({'reply': reply})

        except Exception as e:
            # Return a JSON response with the error message
            return JsonResponse({'error': str(e)}, status=500)

    else:
        # Return a 405 Method Not Allowed if the request is not POST
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)