from django.contrib.auth.backends import ModelBackend
from chatbot.models import CustomUser

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)  # Use email instead of username
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
