from google.api_core import retry as google_retry
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
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="Provide tour guidance and information."
)


retry_on_429_or_503 = google_retry.Retry(
    predicate=lambda e: isinstance(e, genai.errors.APIError) and e.code in {429, 503},
    initial=1.0,  # seconds before first retry
    maximum=10.0, # max delay between retries
    multiplier=2.0,  # exponential backoff
    deadline=30.0  # total timeout
)

is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})


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
            # Retry the entire interaction
            @retry_on_429_or_503
            def send_message_with_retry():
                chat_session = model.start_chat(history=[{"role": "user", "parts": [user_message]}])
                return chat_session.send_message(user_message)

            response = send_message_with_retry()

            reply = response.text.strip() if response and response.text else "Sorry, I couldn't respond."
            return JsonResponse({'reply': reply})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)