from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        # Intenta obtener el usuario por el email
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        # Verifica la contraseña
        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
