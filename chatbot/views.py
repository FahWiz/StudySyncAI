
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
import wikipediaapi
import re
import random
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Initialize Wikipedia API
wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent="StudySyncAI/1.0 (contact: shaikhfarheen101@gmail.com)"
)

# Predefined Responses
greeting_responses = ["Hello!", "Hi there!", "Hey!", "Hello! How can I assist you today?"]
farewell_responses = ["Goodbye!", "See you later!", "Take care!", "Bye! Have a great day!"]
about_bot_responses = [
    "I am StudySync AI, your learning assistant. I help students with study-related queries.",
    "StudySync AI is designed to assist students in organizing their study schedules and answering academic questions."
]
thanks_responses=["Glad I could help!","You're welcome!",
"Glad to help!","Anytime! Let me know if you need anything else.","Happy to assist!","No problem! Have a great day!",
"You're always welcome!"," It’s my pleasure! Let me know if you need more help.","No worries! Keep learning and growing!",
"That’s what I’m here for!",
"You're welcome! Hope you found it useful."]

# Extract keywords from question
def extract_keywords(question):
    words = question.lower()
    words = re.sub(r"[^\w\s]", "", words)  # Remove punctuation
    common_words = {"what", "who", "is", "are", "how", "does", "the", "a", "an", "in", "on", "to", "of", "for"}
    keywords = [word for word in words.split() if word not in common_words]
    return " ".join(keywords) if keywords else question  

# Get Wikipedia summary
def get_wikipedia_summary(query):
    page = wiki.page(query)
    return page.summary.split("\n")[0] if page.exists() else None



def assistant_page(request):
    return render(request, 'chatbot/assistant.html')  # Ensure this template exists



# Chatbot API
#from django.views.decorators.csrf import csrf_protect

#@csrf_protect
@api_view(['POST'])
def chatbot_api(request):

    user_input = request.data.get("query", "").strip().lower()  # Convert input to lowercase

    if not user_input:
        return Response({"error": "Empty query received"}, status=400)

    # Handle Greetings
    if user_input in ["hi", "hello", "hey"]:
        return Response({"response": random.choice(greeting_responses)})  

    # Handle Farewell
    if user_input in ["bye", "goodbye", "see you", "exit"]:
        return Response({"response": random.choice(farewell_responses)})  

    # Handle Questions About StudySync AI
    if "studysync ai" in user_input or "yourself" in user_input:
        return Response({"response": about_bot_responses[0]})

    if user_input in ["thanks", "thank you", "thanks for help", "thank you so much", "thankful to you"]:
        return Response({"response": random.choice(thanks_responses)})

    # Wikipedia Search
    keyword_query = extract_keywords(user_input)
    response = get_wikipedia_summary(keyword_query)

    if response:
        return Response({"response": response})  
    else:
        google_search_url = f"https://www.google.com/search?q={keyword_query.replace(' ', '+')}"
        return Response ({
            "response": f'I couldn\'t find the answer. Try searching <a href="{google_search_url}" target="_blank">here</a>.'
        })


def home_page(request):
    return render(request, 'chatbot/home.html')  #Link to Home page

def auth_page(request):
    return render(request, 'chatbot/auth.html')   #link to authentication page

def schedule_page(request):
    return render(request, 'chatbot/study_scheduler.html')   #link to schedular page

from .models import StudyPlan, StudyPlanDetail

@login_required(login_url="login")
def dashboard(request):
    incomplete_plans = StudyPlan.objects.filter(user=request.user, details__is_completed=False).distinct()
    completed_plans = StudyPlan.objects.filter(user=request.user, details__is_completed=True).distinct() 
    
    latest_study_plan = StudyPlan.objects.filter(user=request.user).order_by('-created_at').first()

    if latest_study_plan:
        total_tasks = StudyPlanDetail.objects.filter(study_plan=latest_study_plan).count()
        completed_tasks = StudyPlanDetail.objects.filter(study_plan=latest_study_plan, is_completed=True).count()
    else:
        total_tasks, completed_tasks = 0, 0  # No active plan, reset progress

    progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0  # Avoid division by zero
    return render(request, "chatbot/dashboard.html", {
        "incomplete_plans": incomplete_plans,
        "completed_plans": completed_plans,
        "progress": progress
    })



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import StudyPlan, StudyPlanDetail

@login_required
def profile_view(request):
    user = request.user  # Get logged-in user
    
    # Get user's study plans
    study_plans = StudyPlan.objects.filter(user=user)
    
    # Extract subjects covered
    subjects = set()
    for plan in study_plans:
        subjects.update(StudyPlanDetail.objects.filter(study_plan=plan).values_list('subject', flat=True))

    # Get the next study session
    next_session = StudyPlanDetail.objects.filter(study_plan__user=user, is_completed=False).order_by('date').first()

    # Calculate task progress
    total_tasks = StudyPlanDetail.objects.filter(study_plan__user=user).count()
    completed_tasks = StudyPlanDetail.objects.filter(study_plan__user=user, is_completed=True).count()
    
    progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    context = {
        "user": user,
        "subjects": ", ".join(subjects) if subjects else "No subjects yet",
        "next_session": next_session.date.strftime('%B %d, %Y | %I:%M %p') if next_session else "No upcoming sessions",
        "completed_tasks": completed_tasks,
        "remaining_tasks": total_tasks - completed_tasks,
        "progress_percentage": progress_percentage,
    }
    return render(request, "chatbot/profile.html", context)


# Registration View

from django.contrib.auth import get_user_model

User = get_user_model()  # Get the correct user model dynamically

from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.shortcuts import render, redirect

CustomUser = get_user_model()  # Ensure you're using the custom user model

def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')

        # Check if email is already registered
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # Create and save user
        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.save()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Auto-login after registration
        messages.success(request, "Registration successful!")
        return redirect('dashboard')  # Change to your homepage

    return render(request, 'chatbot/auth.html')


# Login View
from django.contrib.auth import authenticate, login, get_user_model

User = get_user_model()  # Get the correct user model dynamically

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from chatbot.models import CustomUser  # Ensure you import your custom user model

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid email or password")
    
    return render(request, "chatbot/auth.html")  # Stay on login page if login fails



# Logout View
def logout_user(request):
    logout(request)
    return redirect("login")

from django.http import JsonResponse
import json
from .models import StudyPlan, StudyPlanDetail
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

 # Remove this if you're handling CSRF properly with tokens
def save_study_plan(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error":"User not authenticated"}, status=401)
        
        data = json.loads(request.body)
        study_plan_data = data.get("study_plan", [])
        title=data.get("title","Untitled Plan")
        
        if not study_plan_data:
            return JsonResponse({"error": "No study plan data received"}, status=400)

        # Extract general study plan details (using the first entry)
        first_entry = study_plan_data[0]
        preferred_time = first_entry["time"]

        # Create a new StudyPlan entry
        study_plan = StudyPlan.objects.create(
            user=request.user,
            title=title,
            study_hours_per_day=first_entry["duration"],
            preferred_time=preferred_time,
            deadline_days=len(set(entry["date"] for entry in study_plan_data))
        )

        progress=0
        # Store each study session in StudyPlanDetail
        for entry in study_plan_data:
            StudyPlanDetail.objects.create(
                study_plan=study_plan,
                date=datetime.strptime(entry["date"], "%a %b %d %Y").date(),
                subject=entry["subject"],
                topic=entry["topic"],
                duration=entry["duration"]
            )

        return JsonResponse({"message": "Study plan saved successfully!", "study_plan_id": study_plan.id,"progress":progress})

    return JsonResponse({"error": "Invalid request"}, status=400)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import StudyPlanDetail

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import StudyPlanDetail, StudyPlan

@login_required
def mark_as_complete(request, detail_id):
    if request.method == "POST":
        study_detail = get_object_or_404(StudyPlanDetail, id=detail_id, study_plan__user=request.user)
        study_detail.is_completed = True
        study_detail.save(update_fields=['is_completed'])

        # Get the latest study plan (assuming the latest is the active one)
        latest_study_plan = StudyPlan.objects.filter(user=request.user).order_by('-created_at').first()

        if latest_study_plan:
            total_tasks = StudyPlanDetail.objects.filter(study_plan=latest_study_plan).count()
            completed_tasks = StudyPlanDetail.objects.filter(study_plan=latest_study_plan, is_completed=True).count()
        else:
            total_tasks, completed_tasks = 0, 0

        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return JsonResponse({"message": "Task marked as complete!", "progress": progress})

    return JsonResponse({"error": "Invalid request"}, status=400)

 


