from django.urls import path, include
from chatbot.views import home_page  # Import home_page view

urlpatterns = [
    path('', home_page, name='home'),  # Home page as the default page
  #  path('chatbot/', assistant_page, name='chatbot'),  # Chatbot page URL
   path('api/', include('chatbot.urls')),  # Keep API routes
]
